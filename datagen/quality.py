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

    # 1. Energy balance check
    values = extract_numeric_values(output_text)
    if values.get("exergy_in") and values.get("exergy_out") and values.get("exergy_destroyed"):
        balance = abs(values["exergy_in"] - values["exergy_out"] - values["exergy_destroyed"])
        tolerance = QUALITY["energy_balance_tolerance_pct"] / 100 * values["exergy_in"]
        checks["energy_balance"] = balance <= tolerance
        if not checks["energy_balance"]:
            errors.append(
                f"Energy balance violation: |{values['exergy_in']:.1f} - {values['exergy_out']:.1f} "
                f"- {values['exergy_destroyed']:.1f}| = {balance:.1f} > {tolerance:.1f}"
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
    Uses regex patterns to find common output patterns.
    """
    values = {}

    patterns = {
        "exergy_in": [
            r"[Ee]xergy\s+(?:in|input)\s*[=:]\s*([\d,.]+)\s*kW",
            r"Ex_in\s*[=:]\s*([\d,.]+)",
        ],
        "exergy_out": [
            r"[Ee]xergy\s+(?:out|output)\s*[=:]\s*([\d,.]+)\s*kW",
            r"Ex_out\s*[=:]\s*([\d,.]+)",
        ],
        "exergy_destroyed": [
            r"[Ee]xergy\s+(?:destroyed|destruction)\s*[=:]\s*([\d,.]+)\s*kW",
            r"Ex_(?:d|destroyed)\s*[=:]\s*([\d,.]+)",
            r"I_(?:dot|total)\s*[=:]\s*([\d,.]+)",
        ],
        "efficiency": [
            r"[Ee]xergy\s+efficiency\s*[=:]\s*([\d,.]+)\s*%",
            r"η_?(?:ex|II)\s*[=:]\s*([\d,.]+)",
        ],
        "entropy_generation": [
            r"S_gen\s*[=:]\s*([\d,.]+)\s*kW/K",
        ],
        "bejan_number": [
            r"N_s\s*[=:]\s*([\d,.]+)",
            r"Bejan\s+number\s*[=:]\s*([\d,.]+)",
        ],
        "f_factor": [
            r"f[_-]?factor\s*[=:]\s*([\d,.]+)",
            r"f\s*[=:]\s*([\d,.]+)",
        ],
        "avoidable": [
            r"[Aa]voidable\s*[=:]\s*([\d,.]+)\s*kW",
            r"I_AV\s*[=:]\s*([\d,.]+)",
        ],
        "unavoidable": [
            r"[Uu]navoidable\s*[=:]\s*([\d,.]+)\s*kW",
            r"I_UN\s*[=:]\s*([\d,.]+)",
        ],
    }

    for key, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    values[key] = float(match.group(1).replace(",", "."))
                except ValueError:
                    pass
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
