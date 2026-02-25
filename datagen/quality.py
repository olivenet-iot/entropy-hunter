"""
EntropyHunter — Thermodynamic Quality Control

Every generated example must pass these checks before
being included in the training dataset.

Based on ExergyLab engine constraints and second law requirements.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional
from config import QUALITY, DEAD_STATE


@dataclass
class QualityResult:
    passed: bool
    checks: dict[str, bool]
    errors: list[str]
    warnings: list[str]


def check_example(example: dict) -> QualityResult:
    """
    Run all quality checks on a generated example.
    Returns QualityResult with pass/fail and details.
    """
    checks = {}
    errors = []
    warnings = []
    output_text = example.get("output", "")

    # 1. Energy balance check (Ex_in = Ex_out + Ex_waste + Ex_destroyed)
    values = extract_numeric_values(output_text)
    if values.get("exergy_in") and values.get("exergy_out") and values.get("exergy_destroyed"):
        ex_waste = values.get("exergy_waste", 0.0)  # 0 if no waste streams
        balance = abs(values["exergy_in"] - values["exergy_out"] - ex_waste - values["exergy_destroyed"])
        tolerance = QUALITY["energy_balance_tolerance_pct"] / 100 * values["exergy_in"]
        checks["energy_balance"] = balance <= tolerance
        if not checks["energy_balance"]:
            errors.append(
                f"Energy balance violation: |{values['exergy_in']:.1f} - {values['exergy_out']:.1f} "
                f"- {ex_waste:.1f}(waste) - {values['exergy_destroyed']:.1f}| = {balance:.1f} > {tolerance:.1f}"
            )
    else:
        checks["energy_balance"] = None  # cannot verify
        warnings.append("Could not extract exergy values for balance check")

    # 2. Efficiency range
    if values.get("efficiency"):
        eff = values["efficiency"]
        checks["efficiency_range"] = QUALITY["min_efficiency_pct"] < eff < QUALITY["max_efficiency_pct"]
        if not checks["efficiency_range"]:
            errors.append(f"Efficiency {eff:.1f}% outside valid range")
    else:
        checks["efficiency_range"] = None

    # 3. Second law (non-negative exergy destruction)
    if values.get("exergy_destroyed") is not None:
        checks["second_law"] = values["exergy_destroyed"] >= QUALITY["min_exergy_destroyed_kW"]
        if not checks["second_law"]:
            errors.append(f"Second law violation: Ex_destroyed = {values['exergy_destroyed']:.2f} < 0")
    else:
        checks["second_law"] = None

    # 4. Gouy-Stodola consistency
    if values.get("exergy_destroyed") and values.get("entropy_generation"):
        T0 = DEAD_STATE["T0_K"]
        gouy_stodola = T0 * values["entropy_generation"]
        deviation = abs(gouy_stodola - values["exergy_destroyed"])
        tolerance = QUALITY["gouy_stodola_tolerance_pct"] / 100 * values["exergy_destroyed"]
        checks["gouy_stodola"] = deviation <= tolerance
        if not checks["gouy_stodola"]:
            errors.append(
                f"Gouy-Stodola mismatch: T₀×S_gen = {gouy_stodola:.2f} vs "
                f"Ex_d = {values['exergy_destroyed']:.2f} (Δ = {deviation:.2f})"
            )
    else:
        checks["gouy_stodola"] = None

    # 5. Bejan number range
    if values.get("bejan_number") is not None:
        Ns = values["bejan_number"]
        lo, hi = QUALITY["bejan_number_range"]
        checks["bejan_range"] = lo <= Ns <= hi
        if not checks["bejan_range"]:
            errors.append(f"Bejan number N_s = {Ns:.3f} outside [{lo}, {hi}]")
    else:
        checks["bejan_range"] = None

    # 6. SPECO factors range
    if values.get("f_factor") is not None:
        f = values["f_factor"]
        lo, hi = QUALITY["f_factor_range"]
        checks["f_factor_range"] = lo <= f <= hi
        if not checks["f_factor_range"]:
            errors.append(f"f-factor = {f:.3f} outside [{lo}, {hi}]")
    else:
        checks["f_factor_range"] = None

    # 7. Dead state consistency
    if "298.15" in output_text or "25°C" in output_text or "25 °C" in output_text:
        checks["dead_state"] = True
    else:
        checks["dead_state"] = None
        warnings.append("Dead state reference not found in output")

    # 8. Avoidable/Unavoidable split consistency
    if values.get("avoidable") and values.get("unavoidable") and values.get("exergy_destroyed"):
        split_sum = values["avoidable"] + values["unavoidable"]
        deviation = abs(split_sum - values["exergy_destroyed"])
        tolerance = 0.01 * values["exergy_destroyed"]
        checks["av_un_split"] = deviation <= tolerance
        if not checks["av_un_split"]:
            errors.append(f"AV+UN = {split_sum:.2f} ≠ Ex_d = {values['exergy_destroyed']:.2f}")
    else:
        checks["av_un_split"] = None

    # Determine overall pass/fail
    verified_checks = {k: v for k, v in checks.items() if v is not None}
    passed = all(verified_checks.values()) if verified_checks else False

    return QualityResult(
        passed=passed,
        checks=checks,
        errors=errors,
        warnings=warnings,
    )


def extract_numeric_values(text: str) -> dict[str, Optional[float]]:
    """
    Extract key numeric values from generated analysis text.
    
    STRATEGY (priority order):
    1. JSON summary block (machine-readable, most reliable)
    2. Markdown table extraction with unit validation
    3. Inline pattern extraction with physical validity filtering
    
    Falls back gracefully: if JSON is missing/truncated, regex takes over.
    """
    # === PHASE 0: Try JSON summary block first ===
    values = _extract_from_json_block(text)
    if values:
        # JSON found — but still check if any keys are missing (null in JSON)
        # Don't bother with regex for null values, they genuinely weren't calculated
        return values

    # === PHASE 1+2: Regex fallback (for pre-JSON examples or truncated responses) ===
    return _extract_from_regex(text)


def _extract_from_json_block(text: str) -> dict[str, Optional[float]]:
    """
    Extract values from the machine-readable JSON block at end of response.
    Returns empty dict if no valid JSON block found.
    """
    # JSON key → internal key mapping
    key_map = {
        "exergy_in_kW": "exergy_in",
        "exergy_out_kW": "exergy_out",
        "exergy_waste_kW": "exergy_waste",
        "exergy_destroyed_kW": "exergy_destroyed",
        "efficiency_pct": "efficiency",
        "entropy_generation_kW_K": "entropy_generation",
        "bejan_number": "bejan_number",
        "avoidable_kW": "avoidable",
        "unavoidable_kW": "unavoidable",
        "f_factor": "f_factor",
    }

    # Find JSON block: look for ```json ... ``` at the end of text
    # Allow some trailing whitespace/newlines after the block
    pattern = r'```json\s*\n?\s*(\{[^}]+\})\s*\n?\s*```\s*$'
    match = re.search(pattern, text, re.DOTALL)
    
    if not match:
        # Try without code fence (bare JSON at end)
        pattern = r'(\{"exergy_in_kW"[^}]+\})\s*$'
        match = re.search(pattern, text, re.DOTALL)
    
    if not match:
        return {}

    try:
        raw = json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return {}

    # Map JSON keys to internal keys, skip nulls
    values = {}
    for json_key, internal_key in key_map.items():
        val = raw.get(json_key)
        if val is not None and isinstance(val, (int, float)):
            values[internal_key] = float(val)

    # Sanity check: need at least 3 core values to trust the JSON
    core_keys = {"exergy_in", "exergy_out", "exergy_destroyed", "efficiency"}
    if len(core_keys & set(values.keys())) < 3:
        return {}  # JSON block is incomplete/corrupt, fall back to regex

    return values


def _extract_from_regex(text: str) -> dict[str, Optional[float]]:
    """
    Regex-based extraction (fallback for pre-JSON examples or truncated responses).
    
    3-phase strategy:
    1. Strict kW table patterns
    2. Other table patterns (%, dimensionless)
    3. Inline patterns with physical validity filtering
    """
    values = {}

    # Physical validity ranges for sanity checking
    # NOTE: extraction ranges are WIDER than quality check ranges.
    # We want to EXTRACT physically questionable values so quality checks can FLAG them.
    valid_ranges = {
        "exergy_in": (0.01, 100000),      # kW
        "exergy_out": (0.01, 100000),      # kW
        "exergy_destroyed": (-1000, 100000), # kW, allow negative for 2nd law check to catch
        "efficiency": (0.0, 200.0),         # %, wider range so quality check can flag >100%
        "entropy_generation": (0.0001, 1000),  # kW/K
        "bejan_number": (0.0, 1.0),        # dimensionless, MUST be 0-1
        "f_factor": (0.0, 1.0),            # dimensionless
        "avoidable": (0.0, 100000),        # kW
        "unavoidable": (0.0, 100000),      # kW
    }

    # === PHASE 1: Try summary table extraction first ===
    # Look for the LAST markdown table in the text (most likely the summary)
    # For kW values: match rows where unit column contains "kW"
    # CRITICAL: "Exergy destruction ratio" must NOT match "Exergy destruction"
    
    table_patterns_kw = {
        # These patterns require "kW" in the unit column to avoid catching percentages or dimensionless numbers
        "exergy_in": r"\|\s*(?:[Ee]xergy\s+[Ii]nput|[Ee]lectrical\s+power\s+input)[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
        "exergy_out": r"\|\s*(?:[Ee]xergy\s+(?:[Oo]utput|[Pp]roduct)|[Ff]low\s+exergy\s+increase|[Uu]seful\s+exergy\s+output)[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
        "exergy_destroyed": r"\|\s*[Ee]xergy\s+[Dd]estruction\s*\([^)]*\)\s*\|\s*(-?[\d,.]+)\s*\|\s*kW\s*\|",
        "entropy_generation": r"\|\s*[Ee]ntropy\s+[Gg]eneration[^|]*\|\s*([\d,.]+)\s*\|\s*kW/K\s*\|",
        "avoidable": r"\|\s*[Aa]voidable\s+(?:exergy\s+)?(?:destruction\s*)?\(?[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
        "unavoidable": r"\|\s*[Uu]navoidable\s+(?:exergy\s+)?(?:destruction\s*)?\(?[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
    }
    
    table_patterns_other = {
        # These don't need kW - they match % or dimensionless
        "efficiency": r"\|\s*[Ee]xergy\s+[Ee]fficiency[^|]*\|\s*([\d,.]+)\s*\|\s*%\s*\|",
        # N_s (exergy destruction ratio) — NOT Bejan number (Be) which is a different quantity
        "bejan_number": r"\|\s*(?:[Ee]xergy\s+[Dd]estruction\s+ratio|[Dd]imensionless\s+entropy|[Ee]ntropy\s+generation\s+number)\s*[^|]*\|\s*([\d,.]+)\s*\|\s*[—–-]\s*\|",
        "f_factor": r"\|\s*[Ee]xergoeconomic\s+[Ff]actor[^|]*\|\s*([\d,.]+)\s*\|",
    }

    # Try kW patterns first (most reliable)
    for key, pattern in table_patterns_kw.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            try:
                val = float(matches[-1].group(1).replace(",", "."))
                lo, hi = valid_ranges.get(key, (0, 1e9))
                if lo <= val <= hi:
                    values[key] = val
            except ValueError:
                pass

    # Then try non-kW patterns
    for key, pattern in table_patterns_other.items():
        if key in values:
            continue
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            try:
                val = float(matches[-1].group(1).replace(",", "."))
                lo, hi = valid_ranges.get(key, (0, 1e9))
                if lo <= val <= hi:
                    values[key] = val
            except ValueError:
                pass

    # Fallback: looser table patterns (no unit check) for values not yet found
    table_patterns_loose = {
        "exergy_in": r"\|\s*(?:[Ee]xergy\s+[Ii]nput|[Ee]lectrical\s+power\s+input)[^|]*\|\s*([\d,.]+)\s*\|",
        "exergy_out": r"\|\s*(?:[Ee]xergy\s+(?:[Oo]utput|[Pp]roduct)|[Ff]low\s+exergy\s+increase|[Uu]seful\s+exergy\s+output)[^|]*\|\s*([\d,.]+)\s*\|",
        "exergy_destroyed": r"\|\s*[Ee]xergy\s+[Dd]estruction(?!\s+ratio)[^|]*\|\s*(-?[\d,.]+)\s*\|",
        "efficiency": r"\|\s*[Ee]xergy\s+[Ee]fficiency[^|]*\|\s*([\d,.]+)\s*\|",
        "bejan_number": r"\|\s*(?:[Ee]xergy\s+[Dd]estruction\s+ratio|[Dd]imensionless\s+entropy|[Ee]ntropy\s+generation\s+number)[^|]*\|\s*([\d,.]+)\s*\|",
        "entropy_generation": r"\|\s*[Ee]ntropy\s+[Gg]eneration[^|]*\|\s*([\d,.]+)\s*\|",
        "avoidable": r"\|\s*[Aa]voidable[^|]*\|\s*([\d,.]+)\s*\|\s*kW",
        "unavoidable": r"\|\s*[Uu]navoidable[^|]*\|\s*([\d,.]+)\s*\|\s*kW",
    }
    
    for key, pattern in table_patterns_loose.items():
        if key in values:
            continue
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            try:
                val = float(matches[-1].group(1).replace(",", "."))
                lo, hi = valid_ranges.get(key, (0, 1e9))
                if lo <= val <= hi:
                    values[key] = val
            except ValueError:
                pass

    # === PHASE 2: Inline extraction for values not found in tables ===
    inline_patterns = {
        "exergy_in": [
            r"Ėx_in\s*=\s*([\d,.]+)\s*kW",
            r"Ex_in\s*=\s*([\d,.]+)\s*kW",
            r"[Ee]lectrical\s+power\s+input\s*=\s*([\d,.]+)\s*kW",
        ],
        "exergy_out": [
            r"Ėx_out\s*=\s*([\d,.]+)\s*kW",
            r"Ex_out\s*=\s*([\d,.]+)\s*kW",
        ],
        "exergy_destroyed": [
            r"Ėx_d\s*=\s*(-?[\d,.]+)\s*kW",
            r"Ex_d\s*=\s*(-?[\d,.]+)\s*kW",
        ],
        "efficiency": [
            r"η_?ex\s*=\s*([\d,.]+)\s*%",
            r"[Ee]xergy\s+[Ee]fficiency\s*=\s*([\d,.]+)\s*%",
        ],
        "entropy_generation": [
            # Direct: Ṡ_gen = 0.05316 kW/K
            r"[SṠ]_gen\s*=\s*([\d,.]+)\s*kW/K",
            r"Ṡ_gen\s*=\s*([\d,.]+)\s*kW/K",
            # Multi-step: Ṡ_gen = Ėx_d / T₀ = 527.72 / 298.15 = 1.7700 kW/K
            # Greedy .* grabs everything, then backtracks to find last = <number> kW/K
            r"[SṠ]_gen.*=\s*([\d,.]+)\s*kW/K",
        ],
        "bejan_number": [
            # Direct: N_s = 0.504 (not followed by division)
            r"N_s\s*=\s*([\d,.]+)(?:\s*$|\s+[^/]|\s*\n)",
            # Multi-step: N_s = 527.72 / 1046.40 = 0.504
            r"N_s\s*=\s*[\d,.]+\s*/\s*[\d,.]+\s*=\s*([\d,.]+)",
        ],
        "f_factor": [
            r"f[_-]?factor\s*=\s*([\d,.]+)(?:\s|$|\n)",
        ],
        "avoidable": [
            r"I_AV\s*=\s*([\d,.]+)\s*kW",
            r"Ėx_d,AV\s*=\s*([\d,.]+)\s*kW",
        ],
        "unavoidable": [
            r"I_UN\s*=\s*([\d,.]+)\s*kW",
            r"Ėx_d,UN\s*=\s*([\d,.]+)\s*kW",
        ],
    }

    for key, pattern_list in inline_patterns.items():
        if key in values:
            continue  # Already found in table

        lo, hi = valid_ranges.get(key, (0, 1e9))
        
        for pattern in pattern_list:
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
            # Filter to physically valid matches
            valid_matches = []
            for m in matches:
                try:
                    val = float(m.group(1).replace(",", "."))
                    if lo <= val <= hi:
                        valid_matches.append(val)
                except ValueError:
                    pass
            
            if valid_matches:
                # Take the LAST valid match (most likely the final calculated result)
                values[key] = valid_matches[-1]
                break

    return values


def batch_quality_check(dataset_path: str) -> dict:
    """
    Run quality checks on an entire dataset file.
    Returns summary statistics.
    """
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = {
        "total": len(dataset),
        "passed": 0,
        "failed": 0,
        "unverifiable": 0,
        "errors_by_type": {},
    }

    for i, example in enumerate(dataset):
        qr = check_example(example)
        if qr.passed:
            results["passed"] += 1
        elif any(v is False for v in qr.checks.values()):
            results["failed"] += 1
            for err in qr.errors:
                err_type = err.split(":")[0]
                results["errors_by_type"][err_type] = results["errors_by_type"].get(err_type, 0) + 1
        else:
            results["unverifiable"] += 1

    results["pass_rate"] = results["passed"] / results["total"] * 100 if results["total"] > 0 else 0

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        summary = batch_quality_check(sys.argv[1])
        print(f"\n📊 Quality Check Summary for {sys.argv[1]}")
        print(f"   Total examples: {summary['total']}")
        print(f"   ✅ Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   ❓ Unverifiable: {summary['unverifiable']}")
        if summary["errors_by_type"]:
            print(f"\n   Error breakdown:")
            for err_type, count in sorted(summary["errors_by_type"].items(), key=lambda x: -x[1]):
                print(f"     {err_type}: {count}")
    else:
        print("Usage: python quality.py <dataset.json>")
