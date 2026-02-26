"""
EntropyHunter — Training Data Preparation

Converts QC-passed generation outputs into clean fine-tuning format.
Supports: Alpaca (generic), ChatML (Qwen2.5), ShareGPT (axolotl).

Usage:
    # Basic: convert merged results to training format
    python prepare_training.py --input data/v0.1/batch_results_merged.jsonl

    # Multiple inputs (merge batches)
    python prepare_training.py --input data/v0.1/batch1.jsonl data/v0.1/batch2.jsonl

    # Custom split ratio
    python prepare_training.py --input data/v0.1/*.jsonl --val-ratio 0.1

    # Specific format
    python prepare_training.py --input data/v0.1/merged.jsonl --format chatml
"""

import argparse
import json
import random
import hashlib
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


# ============================================================
# INFERENCE SYSTEM PROMPT — short, for the student model
# (NOT the teacher prompt which has JSON rules, quality instructions etc.)
# ============================================================

INFERENCE_SYSTEM_PROMPT = """You are EntropyHunter, an expert thermodynamic analysis assistant specializing in exergy (second-law) analysis of industrial equipment.

Your expertise covers:
- Exergy analysis (basic, advanced, exergoeconomic)
- Entropy generation minimization (EGM / Bejan method)
- Avoidable/unavoidable exergy destruction decomposition
- What-if scenario comparison with savings calculations
- Factory-level hotspot detection and prioritization

For every analysis you:
1. Start with a JSON summary block containing key results
2. State the dead state (T₀, P₀) explicitly
3. Show step-by-step calculations with units
4. Present results in clear summary tables
5. Calculate thermodynamic perfection grade with numerical value
6. Decompose entropy generation by mechanism with kW/K values
7. Provide actionable engineering recommendations

Equipment coverage: compressors, boilers, heat exchangers, chillers, pumps, steam turbines, dryers, and multi-equipment facilities."""


# ============================================================
# FORMAT CONVERTERS
# ============================================================

def to_alpaca(instruction: str, output: str, system: str = "") -> dict:
    """Alpaca format: instruction/input/output."""
    return {
        "instruction": instruction,
        "input": "",
        "output": output,
    }


def to_chatml(instruction: str, output: str, system: str = "") -> dict:
    """
    ChatML / Qwen2.5 format: messages array.
    This is what Qwen2.5 natively expects for fine-tuning.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": instruction})
    messages.append({"role": "assistant", "content": output})
    return {"messages": messages}


def to_sharegpt(instruction: str, output: str, system: str = "") -> dict:
    """
    ShareGPT format: conversations array (used by axolotl, FastChat).
    """
    conversations = []
    if system:
        conversations.append({"from": "system", "value": system})
    conversations.append({"from": "human", "value": instruction})
    conversations.append({"from": "gpt", "value": output})
    return {"conversations": conversations}


FORMATTERS = {
    "alpaca": to_alpaca,
    "chatml": to_chatml,
    "sharegpt": to_sharegpt,
}


# ============================================================
# DEDUPLICATION
# ============================================================

def content_hash(instruction: str, output: str) -> str:
    """Hash for deduplication — based on first 200 chars of each."""
    content = instruction[:200] + output[:200]
    return hashlib.md5(content.encode()).hexdigest()


# ============================================================
# MAIN PIPELINE
# ============================================================

def load_examples(input_paths: list[str]) -> list[dict]:
    """Load and merge examples from multiple JSONL files."""
    examples = []
    seen_hashes = set()

    for path_str in input_paths:
        path = Path(path_str)
        if not path.exists():
            # Try glob
            parent = path.parent
            matches = list(parent.glob(path.name))
            if not matches:
                print(f"  ⚠️  Not found: {path_str}")
                continue
            paths = matches
        else:
            paths = [path]

        for p in paths:
            count = 0
            dupes = 0
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    ex = json.loads(line)

                    # Skip if no output (dry runs)
                    if not ex.get("output") or ex["output"].startswith("[DRY RUN"):
                        continue

                    # Skip if QC failed (shouldn't be in passed file, but safety check)
                    meta = ex.get("metadata", {})
                    if meta.get("quality_passed") is False:
                        continue

                    # Deduplicate
                    h = content_hash(ex.get("instruction", ""), ex.get("output", ""))
                    if h in seen_hashes:
                        dupes += 1
                        continue
                    seen_hashes.add(h)

                    examples.append(ex)
                    count += 1

            print(f"  📄 {p.name}: {count} examples loaded" +
                  (f" ({dupes} duplicates skipped)" if dupes else ""))

    return examples


def split_train_val(examples: list[dict], val_ratio: float = 0.10,
                    seed: int = 42) -> tuple[list, list]:
    """
    Stratified split by analysis_type to ensure val has all families.
    """
    random.seed(seed)

    # Group by analysis type
    by_type = {}
    for ex in examples:
        atype = ex.get("metadata", {}).get("analysis_type", "unknown")
        by_type.setdefault(atype, []).append(ex)

    train = []
    val = []

    for atype, group in by_type.items():
        random.shuffle(group)
        n_val = max(1, int(len(group) * val_ratio))  # at least 1 per type
        val.extend(group[:n_val])
        train.extend(group[n_val:])

    # Shuffle final sets
    random.shuffle(train)
    random.shuffle(val)

    return train, val


def prepare_training(
    input_paths: list[str],
    output_dir: str = None,
    format_name: str = "chatml",
    val_ratio: float = 0.10,
    include_system: bool = True,
    seed: int = 42,
):
    """Main pipeline: load → dedupe → split → format → save."""

    # Setup output
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = Path("data/v0.2/training")
    out_dir.mkdir(parents=True, exist_ok=True)

    formatter = FORMATTERS[format_name]
    system = INFERENCE_SYSTEM_PROMPT if include_system else ""

    # Step 1: Load & dedupe
    print(f"\n📚 Loading examples...")
    examples = load_examples(input_paths)
    print(f"   Total unique examples: {len(examples)}")

    if not examples:
        print("❌ No examples found!")
        return

    # Step 2: Split
    print(f"\n✂️  Splitting (val_ratio={val_ratio}, seed={seed})...")
    train, val = split_train_val(examples, val_ratio, seed)
    print(f"   Train: {len(train)}, Val: {len(val)}")

    # Step 3: Convert & save
    print(f"\n📝 Converting to {format_name} format...")

    train_path = out_dir / f"train.jsonl"
    val_path = out_dir / f"val.jsonl"

    for split_name, split_data, split_path in [
        ("train", train, train_path),
        ("val", val, val_path),
    ]:
        with open(split_path, "w", encoding="utf-8") as f:
            for ex in split_data:
                instruction = ex.get("instruction", "")
                output = ex.get("output", "")
                formatted = formatter(instruction, output, system)
                f.write(json.dumps(formatted, ensure_ascii=False) + "\n")

    # Step 4: Statistics
    print(f"\n📊 Generating manifest...")

    # Analysis type distribution
    train_dist = Counter(ex.get("metadata", {}).get("analysis_type", "?") for ex in train)
    val_dist = Counter(ex.get("metadata", {}).get("analysis_type", "?") for ex in val)

    # Equipment distribution
    train_equip = Counter(ex.get("metadata", {}).get("equipment_type", "?") for ex in train)
    val_equip = Counter(ex.get("metadata", {}).get("equipment_type", "?") for ex in val)

    # Token estimates (rough: 1 token ≈ 4 chars)
    total_chars = sum(len(ex.get("instruction", "")) + len(ex.get("output", ""))
                      for ex in train + val)
    est_tokens = total_chars / 4

    # Teacher model distribution
    teachers = Counter(ex.get("metadata", {}).get("teacher_model", "?") for ex in train + val)

    manifest = {
        "created_at": datetime.utcnow().isoformat(),
        "format": format_name,
        "include_system_prompt": include_system,
        "seed": seed,
        "val_ratio": val_ratio,
        "total_examples": len(examples),
        "train_examples": len(train),
        "val_examples": len(val),
        "estimated_tokens": int(est_tokens),
        "teacher_models": dict(teachers),
        "train_by_analysis": dict(train_dist.most_common()),
        "val_by_analysis": dict(val_dist.most_common()),
        "train_by_equipment": dict(train_equip.most_common()),
        "val_by_equipment": dict(val_equip.most_common()),
        "source_files": input_paths,
        "system_prompt_preview": INFERENCE_SYSTEM_PROMPT[:200] + "..." if include_system else None,
    }

    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Step 5: Print summary
    print(f"\n{'='*55}")
    print(f"📊 Training Data Summary")
    print(f"{'='*55}")
    print(f"   Format:     {format_name}")
    print(f"   System:     {'included' if include_system else 'excluded'}")
    print(f"   Train:      {len(train)} examples")
    print(f"   Val:        {len(val)} examples")
    print(f"   Est tokens: {est_tokens:,.0f}")
    print(f"   Teachers:   {dict(teachers)}")

    print(f"\n   Train by analysis:")
    for k, v in train_dist.most_common():
        print(f"     {k:30s} {v:4d}")

    print(f"\n   Train by equipment:")
    for k, v in train_equip.most_common():
        print(f"     {k:20s} {v:4d}")

    print(f"\n   📁 {train_path}")
    print(f"   📁 {val_path}")
    print(f"   📁 {manifest_path}")
    print()

    # Step 6: Sanity check — print 1 example
    print(f"{'='*55}")
    print(f"🔍 Sample (first train example):")
    print(f"{'='*55}")
    sample = train[0]
    sample_formatted = formatter(
        sample.get("instruction", ""),
        sample.get("output", ""),
        system
    )
    preview = json.dumps(sample_formatted, indent=2, ensure_ascii=False)
    # Show first 600 chars + last 300 chars
    if len(preview) > 1000:
        print(preview[:600])
        print(f"\n  ... ({len(preview)} chars total) ...\n")
        print(preview[-300:])
    else:
        print(preview)
    print()


# ============================================================
# DPO PREPARATION (for future use with rejected examples)
# ============================================================

def prepare_dpo(
    chosen_path: str,
    rejected_path: str,
    output_dir: str = None,
):
    """
    Prepare DPO pairs from chosen (passed) and rejected (failed) examples.
    Matches by instruction (same prompt, different outputs).

    For now: placeholder. Will be used after re-generating rejected prompts.
    """
    if output_dir is None:
        output_dir = "data/v0.1/training"
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load chosen
    chosen_map = {}
    with open(chosen_path) as f:
        for line in f:
            ex = json.loads(line)
            key = ex["instruction"][:200]  # match by prompt prefix
            chosen_map[key] = ex

    # Load rejected and match
    pairs = []
    with open(rejected_path) as f:
        for line in f:
            ex = json.loads(line)
            key = ex["instruction"][:200]
            if key in chosen_map:
                pairs.append({
                    "prompt": ex["instruction"],
                    "chosen": chosen_map[key]["output"],
                    "rejected": ex["output"],
                    "metadata": {
                        "equipment_type": ex.get("metadata", {}).get("equipment_type"),
                        "analysis_type": ex.get("metadata", {}).get("analysis_type"),
                        "rejection_reason": ex.get("metadata", {}).get("quality_errors", []),
                    }
                })

    dpo_path = out_dir / "dpo_pairs.jsonl"
    with open(dpo_path, "w") as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"\n📊 DPO Pairs: {len(pairs)}")
    print(f"   (Need re-generation of rejected prompts for full coverage)")
    print(f"   📁 {dpo_path}")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EntropyHunter Training Data Preparation")

    parser.add_argument("--input", "-i", nargs="+", required=True,
                        help="Input JSONL file(s) with QC-passed examples")
    parser.add_argument("--output-dir", "-o", type=str, default=None,
                        help="Output directory (default: data/v0.1/training)")
    parser.add_argument("--format", "-f", type=str, default="chatml",
                        choices=list(FORMATTERS.keys()),
                        help="Output format (default: chatml for Qwen2.5)")
    parser.add_argument("--val-ratio", type=float, default=0.10,
                        help="Validation split ratio (default: 0.10)")
    parser.add_argument("--no-system", action="store_true",
                        help="Exclude system prompt from training data")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducible splits")

    # DPO mode
    parser.add_argument("--dpo", action="store_true",
                        help="Prepare DPO pairs instead of SFT data")
    parser.add_argument("--rejected", type=str, default=None,
                        help="Rejected JSONL for DPO pair matching")

    args = parser.parse_args()

    if args.dpo:
        if not args.rejected:
            print("❌ --dpo requires --rejected path")
            sys.exit(1)
        prepare_dpo(
            chosen_path=args.input[0],
            rejected_path=args.rejected,
            output_dir=args.output_dir,
        )
    else:
        prepare_training(
            input_paths=args.input,
            output_dir=args.output_dir,
            format_name=args.format,
            val_ratio=args.val_ratio,
            include_system=not args.no_system,
            seed=args.seed,
        )
