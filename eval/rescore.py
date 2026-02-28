"""
EntropyHunter — Re-score existing benchmark outputs with fixed checks.

Reads the .md model output files from a previous benchmark run and
re-applies check_structure with the fixed efficiency_physical regex
and expanded avoidable_ratio keywords.

NO NEW INFERENCES NEEDED — just re-scoring existing outputs.

Usage:
    python rescore.py --results-json eval/benchmark/results_entropy-hunter-v02_t07_x3_20260227_084106.json
    python rescore.py --md-dir eval/benchmark --model entropy-hunter-v02 --runs 3
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Import check_structure and TEST_CASES from fixed benchmark
# (place this script in the same directory as benchmark_v03.py)
try:
    from benchmark_v03 import check_structure, TEST_CASES, _extract_exergy_efficiency
except ImportError:
    print("❌ benchmark_v03.py not found in current directory or PYTHONPATH")
    print("   Place this script alongside benchmark_v03.py (the fixed version)")
    sys.exit(1)


def find_md_files(md_dir: Path, model: str, test_id: str, runs: int = 3):
    """Find .md output files for a given test and model."""
    model_slug = model.replace(":", "_").replace("/", "_")
    files = []

    for run in range(1, runs + 1):
        # Pattern: {test_id}_{model}_run{N}.md
        pattern1 = md_dir / f"{test_id}_{model_slug}_run{run}.md"
        # Pattern without run suffix (single run)
        pattern2 = md_dir / f"{test_id}_{model_slug}.md"

        if pattern1.exists():
            files.append((run, pattern1))
        elif run == 1 and pattern2.exists():
            files.append((1, pattern2))

    return files


def read_md_output(path: Path) -> str:
    """Read model output from .md file.
    
    The header (# test_id, Model:, Time:, Checks:) doesn't contain
    any check keywords, so we return the full text to avoid
    accidentally stripping content.
    """
    return path.read_text(encoding="utf-8")


def rescore_from_json(results_json: Path, md_dir: Path):
    """
    Re-score by loading original results JSON, finding corresponding .md files,
    and re-running check_structure on the raw outputs.
    """
    with open(results_json) as f:
        original = json.load(f)

    model = original["model"]
    model_slug = model.replace(":", "_").replace("/", "_")

    # Build test lookup
    test_lookup = {t["id"]: t for t in TEST_CASES}

    new_results = []
    old_passed_total = 0
    old_checks_total = 0
    new_passed_total = 0
    new_checks_total = 0

    changes = []

    for r in original["results"]:
        test_id = r["test_id"]
        run = r.get("run_number", 1)

        # Find .md file
        if run > 1:
            md_path = md_dir / f"{test_id}_{model_slug}_run{run}.md"
        else:
            md_path = md_dir / f"{test_id}_{model_slug}.md"
            if not md_path.exists():
                md_path = md_dir / f"{test_id}_{model_slug}_run1.md"

        if not md_path.exists():
            print(f"  ⚠️  {test_id} run {run}: .md not found at {md_path}")
            new_results.append(r)  # keep original
            continue

        # Read raw output
        output = read_md_output(md_path)

        # Get expected checks from test definition
        test_def = test_lookup.get(test_id)
        if not test_def:
            print(f"  ⚠️  {test_id}: not found in TEST_CASES")
            new_results.append(r)
            continue

        # Re-score with fixed check_structure
        new_checks = check_structure(output, test_def["expected"])

        # Count (excluding json_block)
        old_scored = {k: v for k, v in r["checks"].items()
                      if k != "json_block" and isinstance(v, bool)}
        new_scored = {k: v for k, v in new_checks.items()
                      if k != "json_block" and isinstance(v, bool)}

        old_p = sum(1 for v in old_scored.values() if v)
        old_t = len(old_scored)
        new_p = sum(1 for v in new_scored.values() if v)
        new_t = len(new_scored)

        old_passed_total += old_p
        old_checks_total += old_t
        new_passed_total += new_p
        new_checks_total += new_t

        # Track changes
        for check in set(list(old_scored.keys()) + list(new_scored.keys())):
            old_val = old_scored.get(check)
            new_val = new_scored.get(check)
            if old_val != new_val:
                changes.append({
                    "test_id": test_id,
                    "run": run,
                    "check": check,
                    "old": old_val,
                    "new": new_val,
                })

        # Build new result
        new_r = dict(r)
        new_r["checks"] = new_checks
        new_r["passed_checks"] = new_p
        new_r["total_checks"] = new_t
        new_results.append(new_r)

    # Report
    print(f"\n{'=' * 60}")
    print(f"📊 Re-score Results: {model}")
    print(f"{'=' * 60}")

    old_pct = old_passed_total / old_checks_total * 100 if old_checks_total > 0 else 0
    new_pct = new_passed_total / new_checks_total * 100 if new_checks_total > 0 else 0
    delta = new_pct - old_pct

    print(f"\n  Old score: {old_passed_total}/{old_checks_total} = {old_pct:.1f}%")
    print(f"  New score: {new_passed_total}/{new_checks_total} = {new_pct:.1f}%")
    print(f"  Delta:     {delta:+.1f}%")

    if changes:
        print(f"\n  Changes ({len(changes)} check flips):")
        # Group by check
        by_check = defaultdict(list)
        for c in changes:
            by_check[c["check"]].append(c)

        for check, items in sorted(by_check.items()):
            gained = sum(1 for i in items if i["new"] is True and i["old"] is not True)
            lost = sum(1 for i in items if i["old"] is True and i["new"] is not True)
            new_null = sum(1 for i in items if i["old"] is not None and i["new"] is None)
            old_null = sum(1 for i in items if i["old"] is None and i["new"] is not None)
            print(f"    {check:<25s}  +{gained} gained  -{lost} lost  ({len(items)} total changes)")
    else:
        print(f"\n  No changes detected.")

    # Save new results
    out_path = results_json.parent / f"rescored_{results_json.name}"
    new_data = dict(original)
    new_data["results"] = new_results
    new_data["rescored"] = True
    new_data["rescore_changes"] = len(changes)
    with open(out_path, "w") as f:
        json.dump(new_data, f, indent=2)
    print(f"\n  📁 Saved: {out_path}")

    return new_pct, delta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-score benchmark with fixed checks")
    parser.add_argument("--results-json", "-r", required=True,
                        help="Original results JSON file")
    parser.add_argument("--md-dir", "-d", default=None,
                        help="Directory with .md output files (default: same as JSON)")

    args = parser.parse_args()

    results_path = Path(args.results_json)
    md_dir = Path(args.md_dir) if args.md_dir else results_path.parent

    rescore_from_json(results_path, md_dir)
