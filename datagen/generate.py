"""
EntropyHunter — Synthetic Data Generation Script (v5 — Scaffold)

CHANGE LOG v4→v5:
- Output directory: data/v0.2 → data/v0.4
- ANALYSIS_WEIGHTS rebalanced for v0.4 (more whatif/AV-UN/hotspot)
- Metadata includes scaffold_version and data_version tags
- Imports from system_prompts (v5) and quality (v5) automatically

Generates training examples by:
1. Creating random prompts from templates (Family A-F)
2. Sending to Claude API (teacher model) — sync or batch
3. Running quality checks (scaffold-aware parser)
4. Saving approved examples to JSONL

Usage:
    # === SYNC MODE (real-time, for testing) ===
    python generate.py --count 5 --equipment compressor
    python generate.py --count 5 --equipment boiler --analysis exergoeconomic
    python generate.py --count 6 --analysis all

    # === BATCH MODE (50% cheaper, async) ===
    # Step 1: Prepare & submit batch
    python generate.py --count 800 --analysis all --batch

    # Step 2: Check status
    python generate.py --batch-status msgbatch_xxxx

    # Step 3: Download & quality-check results
    python generate.py --batch-download msgbatch_xxxx

    # === OTHER ===
    python generate.py --dry-run --count 3 --analysis all    # Test prompts only
    python generate.py --batch-prepare --count 800            # Prepare JSONL without submitting
"""

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from system_prompts import build_system_prompt
from quality import check_example
from config import (
    TEACHER_MODEL,
    TEACHER_API_KEY,
    DATA_V01_DIR,
    DATA_REJECTED_DIR,
    MAX_RETRIES,
    TIMEOUT_SECONDS,
    REQUEST_DELAY_SECONDS,
    KNOWLEDGE_DIR,
    SKILLS_DIR,
)

# v0.4: Override output directory to data/v0.4
DATA_V04_DIR = Path("data/v0.4")
DATA_V01_DIR = DATA_V04_DIR  # Redirect all references

# ============================================================
# FAMILY IMPORTS
# ============================================================

from templates.family_a_basic_exergy import (
    generate_prompt as gen_a, TEMPLATE_MAP as EQUIPMENT_TYPES_A,
)
from templates.family_b_exergoeconomic import (
    generate_prompt as gen_b, TEMPLATE_MAP_B as EQUIPMENT_TYPES_B,
)
from templates.family_c_entropy_generation import (
    generate_prompt as gen_c, TEMPLATE_MAP_C as EQUIPMENT_TYPES_C,
)
from templates.family_d_whatif import (
    generate_prompt as gen_d, PARAM_GENERATORS as EQUIPMENT_TYPES_D,
)
from templates.family_e_avoidable_unavoidable import (
    generate_prompt as gen_e, TEMPLATE_MAP_E as EQUIPMENT_TYPES_E,
)
from templates.family_f_hotspot import (
    generate_prompt as gen_f,
)

FAMILY_DISPATCH = {
    "basic_exergy":            (gen_a, EQUIPMENT_TYPES_A),
    "exergoeconomic":          (gen_b, EQUIPMENT_TYPES_B),
    "entropy_generation":      (gen_c, EQUIPMENT_TYPES_C),
    "whatif_comparison":        (gen_d, EQUIPMENT_TYPES_D),
    "avoidable_unavoidable":   (gen_e, EQUIPMENT_TYPES_E),
    "hotspot_detection":       (gen_f, None),
}

ALL_EQUIPMENT_TYPES = list(EQUIPMENT_TYPES_A.keys())

## v0.4 weights: rebalanced for Calculation Summary scaffold
# All families now have scaffold templates → more even distribution
# whatif/AV-UN/hotspot increased (were under-represented in v0.2)
# Total: 1200 examples target
ANALYSIS_WEIGHTS = {
    "basic_exergy":          250,
    "exergoeconomic":        250,
    "entropy_generation":    250,
    "whatif_comparison":      150,
    "avoidable_unavoidable":  150,
    "hotspot_detection":      100,
}


# ============================================================
# KNOWLEDGE / SKILL LOADING
# ============================================================

def load_knowledge_context(equipment_type: str) -> str:
    knowledge_path = KNOWLEDGE_DIR / equipment_type
    if not knowledge_path.exists():
        return ""
    context_parts = []
    for f in sorted(knowledge_path.glob("*.md"))[:3]:
        try:
            content = f.read_text(encoding="utf-8")
            context_parts.append(f"### {f.stem}\n{content[:2000]}")
        except Exception:
            pass
    return "\n\n".join(context_parts)


def load_skill_context(equipment_type: str) -> str:
    skill_path = SKILLS_DIR / "equipment"
    if not skill_path.exists():
        return ""
    for f in skill_path.glob("*.md"):
        if equipment_type in f.stem.lower():
            try:
                return f.read_text(encoding="utf-8")[:3000]
            except Exception:
                pass
    return ""


# ============================================================
# SYNC API CALL
# ============================================================

def call_claude_api(system_prompt: str, user_prompt: str) -> str:
    if not HAS_ANTHROPIC:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")
    if not TEACHER_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set.")

    client = anthropic.Anthropic(api_key=TEACHER_API_KEY)

    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=TEACHER_MODEL,
                max_tokens=10240,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.7,
            )
            return response.content[0].text
        except anthropic.RateLimitError:
            wait = (attempt + 1) * 10
            print(f"  ⏳ Rate limited, waiting {wait}s...")
            time.sleep(wait)
        except anthropic.APIError as e:
            print(f"  ❌ API error (attempt {attempt+1}/{MAX_RETRIES}): {e}")
            time.sleep(5)

    raise RuntimeError(f"Failed after {MAX_RETRIES} attempts")


# ============================================================
# PROMPT GENERATION (shared between sync & batch)
# ============================================================

def pick_analysis_type() -> str:
    types = list(ANALYSIS_WEIGHTS.keys())
    weights = list(ANALYSIS_WEIGHTS.values())
    return random.choices(types, weights=weights, k=1)[0]


def generate_prompt_and_system(
    equipment_type: str = None,
    analysis_type: str = "basic_exergy",
) -> tuple:
    """
    Generate user prompt + system prompt + metadata.
    Returns (user_prompt, system_prompt, metadata).
    """
    gen_fn, equip_map = FAMILY_DISPATCH[analysis_type]

    if analysis_type == "hotspot_detection":
        prompt_data = gen_fn()
        equip_list = prompt_data["metadata"].get("equipment_list", [])
        knowledge_eq = equip_list[0]["equipment_type"] if equip_list else "boiler"
    else:
        prompt_data = gen_fn(equipment_type)
        knowledge_eq = equipment_type

    user_prompt = prompt_data["instruction"]
    metadata = prompt_data["metadata"]

    knowledge = load_knowledge_context(knowledge_eq)
    skill = load_skill_context(knowledge_eq)
    full_knowledge = skill + "\n\n" + knowledge if skill else knowledge
    system_prompt = build_system_prompt(analysis_type, full_knowledge)

    return user_prompt, system_prompt, metadata


# ============================================================
# SYNC MODE
# ============================================================

def generate_single_example(
    equipment_type: str = None,
    analysis_type: str = "basic_exergy",
    dry_run: bool = False,
) -> dict:
    user_prompt, system_prompt, metadata = generate_prompt_and_system(
        equipment_type, analysis_type
    )

    if dry_run:
        return {
            "instruction": user_prompt,
            "input": "",
            "output": "[DRY RUN — no API call]",
            "metadata": {
                **metadata,
                "system_prompt_length": len(system_prompt),
                "knowledge_loaded": bool(load_knowledge_context(
                    metadata.get("equipment_type", "")
                )),
            },
        }

    print(f"  📡 Calling {TEACHER_MODEL}...")
    start = time.time()
    output = call_claude_api(system_prompt, user_prompt)
    elapsed = time.time() - start
    print(f"  ✅ Response received ({elapsed:.1f}s, {len(output)} chars)")

    example = {"instruction": user_prompt, "input": "", "output": output}
    qr = check_example(example)

    return {
        "instruction": user_prompt,
        "input": "",
        "output": output,
        "metadata": {
            **metadata,
            "teacher_model": TEACHER_MODEL,
            "scaffold_version": "v5",
            "data_version": "v0.4",
            "generation_time_s": round(elapsed, 1),
            "quality_passed": qr.passed,
            "quality_checks": qr.checks,
            "quality_errors": qr.errors,
            "quality_warnings": qr.warnings,
            "generated_at": datetime.utcnow().isoformat(),
        }
    }


def run_generation(
    count: int,
    equipment_type: str = None,
    analysis_type: str = "basic_exergy",
    output_path: str = None,
    dry_run: bool = False,
):
    if output_path:
        out_path = Path(output_path)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        DATA_V01_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DATA_V01_DIR / f"batch_{timestamp}.jsonl"

    DATA_REJECTED_DIR.mkdir(parents=True, exist_ok=True)
    reject_path = DATA_REJECTED_DIR / f"rejected_{out_path.stem}.jsonl"

    if analysis_type == "hotspot_detection":
        equipment_types = ["factory"]
    elif equipment_type:
        equipment_types = [equipment_type]
    else:
        equipment_types = ALL_EQUIPMENT_TYPES

    print(f"\n🔥 EntropyHunter Data Generation (SYNC)")
    print(f"   Model: {TEACHER_MODEL}")
    print(f"   Count: {count}")
    print(f"   Analysis: {analysis_type}")
    print(f"   Equipment: {', '.join(equipment_types)}")
    print(f"   Output: {out_path}")
    print(f"   Dry run: {dry_run}")
    print()

    results = {"passed": 0, "failed": 0, "errors": 0}
    examples = []

    for i in range(count):
        if analysis_type == "all":
            current_analysis = pick_analysis_type()
        else:
            current_analysis = analysis_type

        if current_analysis == "hotspot_detection":
            eq_type = None
            label = "factory"
        elif equipment_type:
            eq_type = equipment_type
            label = eq_type
        else:
            eq_type = equipment_types[i % len(equipment_types)]
            label = eq_type

        print(f"[{i+1}/{count}] {label} ({current_analysis})...", end="")

        try:
            example = generate_single_example(
                equipment_type=eq_type,
                analysis_type=current_analysis,
                dry_run=dry_run,
            )

            meta = example.get("metadata", {})
            passed = meta.get("quality_passed", None)

            if passed:
                results["passed"] += 1
                examples.append(example)
                print(f" ✅ passed")
            elif passed is False:
                results["failed"] += 1
                with open(reject_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(example, ensure_ascii=False) + "\n")
                errors = meta.get("quality_errors", [])
                print(f" ❌ failed: {errors[0] if errors else 'unknown'}")
            else:
                results["passed"] += 1
                examples.append(example)
                warnings = meta.get("quality_warnings", [])
                print(f" ⚠️  unverifiable: {warnings[0] if warnings else ''}")

            if not dry_run:
                time.sleep(REQUEST_DELAY_SECONDS)

        except Exception as e:
            results["errors"] += 1
            print(f" 💥 error: {e}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    total = results["passed"] + results["failed"] + results["errors"]
    print(f"\n{'='*50}")
    print(f"📊 Generation Summary")
    print(f"   Total attempts: {total}")
    print(f"   ✅ Passed: {results['passed']}")
    print(f"   ❌ Failed: {results['failed']}")
    print(f"   💥 Errors: {results['errors']}")
    if total > 0:
        print(f"   Pass rate: {results['passed']/total*100:.1f}%")
    print(f"\n   📁 Output: {out_path}")
    if results["failed"] > 0:
        print(f"   📁 Rejected: {reject_path}")
    print()
    return results


# ============================================================
# BATCH MODE — 50% cost savings, async processing
# ============================================================

def batch_prepare(
    count: int,
    equipment_type: str = None,
    analysis_type: str = "all",
    output_path: str = None,
) -> Path:
    """
    Step 1: Generate all prompts and save as batch request JSONL + metadata sidecar.
    Returns path to the requests file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_dir = DATA_V01_DIR / "batches"
    batch_dir.mkdir(parents=True, exist_ok=True)

    requests_path = batch_dir / f"requests_{timestamp}.jsonl"
    meta_path = batch_dir / f"metadata_{timestamp}.jsonl"

    if analysis_type == "hotspot_detection":
        equipment_types = ["factory"]
    elif equipment_type:
        equipment_types = [equipment_type]
    else:
        equipment_types = ALL_EQUIPMENT_TYPES

    print(f"\n📦 Preparing Batch Requests")
    print(f"   Count: {count}")
    print(f"   Analysis: {analysis_type}")
    print(f"   Equipment: {', '.join(equipment_types)}")
    print()

    # Track distribution
    dist = {}

    with open(requests_path, "w") as req_f, open(meta_path, "w") as meta_f:
        for i in range(count):
            if analysis_type == "all":
                current_analysis = pick_analysis_type()
            else:
                current_analysis = analysis_type

            if current_analysis == "hotspot_detection":
                eq_type = None
            elif equipment_type:
                eq_type = equipment_type
            else:
                eq_type = equipment_types[i % len(equipment_types)]

            user_prompt, system_prompt, metadata = generate_prompt_and_system(
                eq_type, current_analysis
            )

            custom_id = f"eh-{i:04d}-{metadata['analysis_type']}-{metadata.get('equipment_type','factory')}"

            # Batch API request format
            request = {
                "custom_id": custom_id,
                "params": {
                    "model": TEACHER_MODEL,
                    "max_tokens": 10240,
                    "temperature": 0.7,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_prompt}],
                }
            }
            req_f.write(json.dumps(request, ensure_ascii=False) + "\n")

            # Sidecar: metadata keyed by custom_id (for reassembly later)
            sidecar = {
                "custom_id": custom_id,
                "instruction": user_prompt,
                "metadata": metadata,
            }
            meta_f.write(json.dumps(sidecar, ensure_ascii=False) + "\n")

            # Track
            dist[current_analysis] = dist.get(current_analysis, 0) + 1

            if (i + 1) % 100 == 0:
                print(f"  Prepared {i+1}/{count}...")

    print(f"\n✅ Batch prepared: {count} requests")
    print(f"   📄 Requests: {requests_path}")
    print(f"   📄 Metadata: {meta_path}")
    print(f"\n   Distribution:")
    for atype, cnt in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"     {atype:30s} {cnt:4d} ({cnt/count*100:.0f}%)")
    return requests_path


def batch_submit(requests_path: Path) -> str:
    """
    Step 2: Submit prepared batch to Anthropic Batch API.
    Returns batch_id.
    """
    if not HAS_ANTHROPIC:
        raise ImportError("anthropic package not installed.")
    if not TEACHER_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set.")

    client = anthropic.Anthropic(api_key=TEACHER_API_KEY)

    # Read requests
    requests = []
    with open(requests_path) as f:
        for line in f:
            requests.append(json.loads(line))

    print(f"\n🚀 Submitting batch: {len(requests)} requests")
    print(f"   Model: {TEACHER_MODEL}")
    print(f"   Estimated cost: ~${len(requests) * 0.14:.0f} (batch pricing)")

    batch = client.messages.batches.create(requests=requests)

    print(f"\n✅ Batch submitted!")
    print(f"   Batch ID: {batch.id}")
    print(f"   Status: {batch.processing_status}")
    print(f"   Expires: {batch.expires_at}")
    print(f"\n   Next steps:")
    print(f"   python generate.py --batch-status {batch.id}")
    print(f"   python generate.py --batch-download {batch.id}")

    # Save batch_id → metadata mapping
    tracking_path = requests_path.parent / "active_batches.txt"
    with open(tracking_path, "a") as f:
        meta_name = requests_path.name.replace("requests_", "metadata_")
        f.write(f"{batch.id}  {meta_name}  {datetime.now().isoformat()}\n")

    return batch.id


def batch_status(batch_id: str):
    """Check status of a submitted batch."""
    if not HAS_ANTHROPIC:
        raise ImportError("anthropic package not installed.")

    client = anthropic.Anthropic(api_key=TEACHER_API_KEY)
    batch = client.messages.batches.retrieve(batch_id)

    counts = batch.request_counts
    total = counts.processing + counts.succeeded + counts.errored + counts.canceled + counts.expired

    print(f"\n📊 Batch Status: {batch_id}")
    print(f"   Status: {batch.processing_status}")
    print(f"   Created: {batch.created_at}")
    if batch.ended_at:
        print(f"   Ended: {batch.ended_at}")
    print(f"   Expires: {batch.expires_at}")
    print(f"\n   Requests: {total} total")
    print(f"     ⏳ Processing: {counts.processing}")
    print(f"     ✅ Succeeded:  {counts.succeeded}")
    print(f"     ❌ Errored:    {counts.errored}")
    print(f"     🚫 Canceled:   {counts.canceled}")
    print(f"     ⏰ Expired:    {counts.expired}")

    if batch.processing_status == "ended":
        print(f"\n   🎉 Batch complete! Run:")
        print(f"   python generate.py --batch-download {batch_id}")

    return batch


def batch_download(batch_id: str, meta_path: str = None):
    """
    Step 3: Download batch results, match with metadata, run quality checks.
    """
    if not HAS_ANTHROPIC:
        raise ImportError("anthropic package not installed.")

    client = anthropic.Anthropic(api_key=TEACHER_API_KEY)

    # Check status first
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        print(f"⏳ Batch not finished yet. Status: {batch.processing_status}")
        counts = batch.request_counts
        print(f"   Succeeded so far: {counts.succeeded} / Processing: {counts.processing}")
        return

    # Find metadata sidecar
    batch_dir = DATA_V01_DIR / "batches"
    if meta_path:
        meta_file = Path(meta_path)
    else:
        meta_file = _find_metadata_file(batch_dir, batch_id)

    # Load metadata sidecar
    metadata_map = {}
    if meta_file and meta_file.exists():
        with open(meta_file) as f:
            for line in f:
                entry = json.loads(line)
                metadata_map[entry["custom_id"]] = entry
        print(f"   Loaded metadata: {len(metadata_map)} entries")
    else:
        print(f"   ⚠️  No metadata sidecar found — results will lack prompt/metadata")

    # Download results
    print(f"\n📥 Downloading results for {batch_id}...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = DATA_V01_DIR / f"batch_results_{timestamp}.jsonl"
    reject_path = DATA_REJECTED_DIR / f"rejected_batch_{timestamp}.jsonl"
    DATA_REJECTED_DIR.mkdir(parents=True, exist_ok=True)

    results = {"succeeded": 0, "passed": 0, "failed": 0, "errored": 0}

    with open(out_path, "w") as out_f, open(reject_path, "w") as rej_f:
        for result in client.messages.batches.results(batch_id):
            custom_id = result.custom_id

            if result.result.type == "succeeded":
                results["succeeded"] += 1
                output_text = result.result.message.content[0].text

                # Retrieve original prompt + metadata from sidecar
                sidecar = metadata_map.get(custom_id, {})
                instruction = sidecar.get("instruction", "")
                metadata = sidecar.get("metadata", {"custom_id": custom_id})

                # Quality check
                example = {"instruction": instruction, "input": "", "output": output_text}
                qr = check_example(example)

                full_example = {
                    "instruction": instruction,
                    "input": "",
                    "output": output_text,
                    "metadata": {
                        **metadata,
                        "teacher_model": TEACHER_MODEL,
                        "scaffold_version": "v5",
                        "data_version": "v0.4",
                        "batch_id": batch_id,
                        "custom_id": custom_id,
                        "quality_passed": qr.passed,
                        "quality_checks": qr.checks,
                        "quality_errors": qr.errors,
                        "quality_warnings": qr.warnings,
                        "generated_at": datetime.utcnow().isoformat(),
                    }
                }

                if qr.passed:
                    results["passed"] += 1
                    out_f.write(json.dumps(full_example, ensure_ascii=False) + "\n")
                else:
                    results["failed"] += 1
                    rej_f.write(json.dumps(full_example, ensure_ascii=False) + "\n")

                # Progress
                if results["succeeded"] % 50 == 0:
                    print(f"  Processed {results['succeeded']}...")

            else:
                results["errored"] += 1
                error_info = {
                    "custom_id": custom_id,
                    "result_type": result.result.type,
                    "error": str(getattr(result.result, "error", None)),
                }
                rej_f.write(json.dumps(error_info) + "\n")

    total = results["succeeded"] + results["errored"]
    print(f"\n{'='*50}")
    print(f"📊 Batch Results Summary")
    print(f"   Total responses: {total}")
    print(f"   ✅ API succeeded: {results['succeeded']}")
    print(f"   💥 API errored:   {results['errored']}")
    print(f"   ✅ QC passed:     {results['passed']}")
    print(f"   ❌ QC failed:     {results['failed']}")
    if results["succeeded"] > 0:
        print(f"   Pass rate: {results['passed']/results['succeeded']*100:.1f}%")
    print(f"\n   📁 Output: {out_path} ({results['passed']} examples)")
    if results["failed"] > 0 or results["errored"] > 0:
        print(f"   📁 Rejected: {reject_path}")
    print()


def _find_metadata_file(batch_dir: Path, batch_id: str) -> Path:
    """Find the metadata sidecar from the active_batches tracking file."""
    tracking = batch_dir / "active_batches.txt"
    if tracking.exists():
        with open(tracking) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2 and parts[0] == batch_id:
                    meta_name = parts[1]
                    meta_file = batch_dir / meta_name
                    if meta_file.exists():
                        return meta_file

    # Fallback: most recent metadata file
    meta_files = sorted(batch_dir.glob("metadata_*.jsonl"), reverse=True)
    if meta_files:
        print(f"   ⚠️  Using most recent metadata file: {meta_files[0].name}")
        return meta_files[0]
    return None


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    all_analysis_types = list(FAMILY_DISPATCH.keys()) + ["all"]

    parser = argparse.ArgumentParser(description="EntropyHunter Data Generation")

    # Common
    parser.add_argument("--count", "-n", type=int, default=5)
    parser.add_argument("--equipment", "-e", type=str, default=None,
                        choices=ALL_EQUIPMENT_TYPES)
    parser.add_argument("--analysis", "-a", type=str, default="basic_exergy",
                        choices=all_analysis_types)
    parser.add_argument("--output", "-o", type=str, default=None)

    # Sync mode
    parser.add_argument("--test", action="store_true",
                        help="3 dry-run examples")
    parser.add_argument("--dry-run", action="store_true",
                        help="Prompts only, no API call")

    # Batch mode
    parser.add_argument("--batch", action="store_true",
                        help="Prepare + submit batch (50%% cheaper)")
    parser.add_argument("--batch-prepare", action="store_true",
                        help="Prepare batch JSONL only, don't submit")
    parser.add_argument("--batch-status", type=str, default=None,
                        metavar="BATCH_ID")
    parser.add_argument("--batch-download", type=str, default=None,
                        metavar="BATCH_ID")
    parser.add_argument("--batch-meta", type=str, default=None,
                        metavar="META_PATH",
                        help="Explicit metadata sidecar path")

    args = parser.parse_args()

    # --- Batch status ---
    if args.batch_status:
        batch_status(args.batch_status)
        sys.exit(0)

    # --- Batch download ---
    if args.batch_download:
        batch_download(args.batch_download, args.batch_meta)
        sys.exit(0)

    # --- Batch prepare + submit ---
    if args.batch or args.batch_prepare:
        analysis = args.analysis if args.analysis != "basic_exergy" else "all"
        requests_path = batch_prepare(
            count=args.count,
            equipment_type=args.equipment,
            analysis_type=analysis,
        )
        if args.batch:
            batch_submit(requests_path)
        else:
            print(f"\n   To submit later:")
            print(f"   python -c \"import json, anthropic; c=anthropic.Anthropic(); "
                  f"reqs=[json.loads(l) for l in open('{requests_path}')]; "
                  f"print(c.messages.batches.create(requests=reqs).id)\"")
        sys.exit(0)

    # --- Test / dry-run ---
    if args.test:
        args.count = 3
        args.dry_run = True

    # --- Sync generation ---
    run_generation(
        count=args.count,
        equipment_type=args.equipment,
        analysis_type=args.analysis,
        output_path=args.output,
        dry_run=args.dry_run,
    )
