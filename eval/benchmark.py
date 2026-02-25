"""
EntropyHunter — Model Benchmark Script

Evaluates fine-tuned model on structure, physics knowledge, and calculation accuracy.
Runs via ollama (local) or any OpenAI-compatible endpoint.

Usage:
    python benchmark.py                           # Default: ollama entropy-hunter
    python benchmark.py --model entropy-hunter     # Specific ollama model
    python benchmark.py --compare qwen2.5:7b       # Compare fine-tuned vs base
    python benchmark.py --quick                     # 5 tests only (fast check)
"""

import argparse
import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# ============================================================
# TEST CASES — diverse equipment × analysis types
# ============================================================

TEST_CASES = [
    # --- BASIC EXERGY (known-answer tests) ---
    {
        "id": "basic-compressor-01",
        "category": "basic_exergy",
        "equipment": "compressor",
        "difficulty": "easy",
        "prompt": """Perform a complete exergy analysis for a screw compressor.

Operating conditions:
- Electrical power input: 55 kW
- Air inlet temperature: 25°C
- Inlet pressure: 1.013 bar (atmospheric)
- Discharge pressure: 8 bar
- Isentropic efficiency: 75%
- Volume flow rate (FAD at inlet conditions): 8.2 m³/min
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_T2s_calc": True,
            "T2s_K_approx": 543,  # T1 * (P2/P1)^((gamma-1)/gamma) = 298.15 * 7.9^0.286
            "efficiency_range": (15, 60),  # exergy efficiency typical for compressors
            "has_summary_table": True,
            "has_json_block": True,
            "has_recommendations": True,
        }
    },
    {
        "id": "basic-boiler-01",
        "category": "basic_exergy",
        "equipment": "boiler",
        "difficulty": "medium",
        "prompt": """Perform a complete exergy analysis for a fire-tube steam boiler.

Operating conditions:
- Thermal capacity: 1000 kW
- Fuel: natural gas
- Steam operating pressure: 10 bar
- Stack temperature: 180°C
- Feedwater temperature: 60°C
- Thermal (first-law) efficiency: 88%
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "efficiency_range": (15, 45),  # boiler exergy efficiency is low (combustion irreversibility)
            "has_waste_streams": True,
            "has_summary_table": True,
            "has_json_block": True,
        }
    },
    {
        "id": "basic-hx-01",
        "category": "basic_exergy",
        "equipment": "heat_exchanger",
        "difficulty": "medium",
        "prompt": """Perform a complete exergy analysis for a shell and tube heat exchanger.

Operating conditions:
- Hot side: water, inlet 90°C → outlet 55°C, flow rate 2.5 kg/s
- Cold side: water, inlet 15°C → outlet 45°C, flow rate 3.8 kg/s
- Pressure drop (hot side): 0.3 bar
- Pressure drop (cold side): 0.2 bar
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_energy_balance": True,
            "efficiency_range": (20, 80),
            "has_summary_table": True,
            "has_json_block": True,
        }
    },
    {
        "id": "basic-pump-01",
        "category": "basic_exergy",
        "equipment": "pump",
        "difficulty": "easy",
        "prompt": """Perform a complete exergy analysis for a centrifugal pump.

Operating conditions:
- Volume flow rate: 50 m³/h
- Total head: 30 m
- Motor electrical power: 7.5 kW
- Pump hydraulic efficiency: 72%
- Motor efficiency: 92%
- Fluid: water at 25°C
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "efficiency_range": (40, 85),
            "has_summary_table": True,
            "has_json_block": True,
        }
    },
    {
        "id": "basic-turbine-01",
        "category": "basic_exergy",
        "equipment": "steam_turbine",
        "difficulty": "hard",
        "prompt": """Perform a complete exergy analysis for a back-pressure steam turbine.

Operating conditions:
- Inlet steam pressure: 40 bar
- Inlet steam temperature: 400°C (superheated)
- Outlet pressure: 4 bar
- Steam mass flow rate: 5 kg/s
- Isentropic efficiency: 78%
- Generator efficiency: 95%
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_steam_tables": True,
            "efficiency_range": (50, 90),
            "has_summary_table": True,
            "has_json_block": True,
        }
    },

    # --- EXERGOECONOMIC ---
    {
        "id": "exergoecon-chiller-01",
        "category": "exergoeconomic",
        "equipment": "chiller",
        "difficulty": "hard",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a centrifugal chiller.

Operating conditions:
- Cooling capacity: 500 kW
- Evaporator temperature: 5°C
- Condenser temperature: 35°C
- COP: 4.2
- Refrigerant: R134a
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €85,000
- Installation factor: 1.65
- Interest rate: 8%
- Equipment lifetime: 20 years
- Maintenance cost factor: 4% of TCI/year
- Annual operating hours: 6000 h/year
- Energy cost (electricity): 0.12 EUR/kWh

Calculate: PEC → TCI → CRF → Ż → Ċ_D → f-factor → r-factor → optimization strategy.""",
        "expected": {
            "has_dead_state": True,
            "has_crf_calc": True,
            "has_cost_rate": True,
            "has_f_factor": True,
            "f_factor_range": (0.0, 1.0),
            "has_json_block": True,
        }
    },

    # --- ENTROPY GENERATION ---
    {
        "id": "egm-compressor-01",
        "category": "entropy_generation",
        "equipment": "compressor",
        "difficulty": "medium",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a centrifugal compressor.

Operating conditions:
- Electrical power input: 150 kW
- Air inlet temperature: 30°C
- Discharge pressure: 10 bar
- Isentropic efficiency: 80%
- Volume flow rate (FAD): 20.0 m³/min
- Operating mode: full_load

Focus on:
1. Total entropy generation rate (Ṡ_gen) via Gouy-Stodola theorem
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (heat transfer vs friction vs mixing)
4. Recommendations for reduction""",
        "expected": {
            "has_dead_state": True,
            "has_entropy_gen": True,
            "has_bejan_number": True,
            "has_grade": True,
            "has_mechanism_decomposition": True,
            "has_json_block": True,
        }
    },

    # --- WHAT-IF ---
    {
        "id": "whatif-boiler-01",
        "category": "whatif_comparison",
        "equipment": "boiler",
        "difficulty": "medium",
        "prompt": """Perform a what-if exergy comparison for a water-tube steam boiler.

**Scenario:** Economizer installation — installing a flue gas economizer to recover waste heat

### BASELINE
- Thermal capacity: 2000 kW
- Fuel: natural gas
- Operating pressure: 15 bar
- Stack temperature: 250°C
- Feedwater temperature: 40°C
- Thermal efficiency: 85%
- Operating mode: full_load

### MODIFIED SCENARIO
- Stack temperature: 180°C (reduced by economizer)
- Thermal efficiency: 91% (improved)
- All other parameters unchanged

Energy cost: 0.05 EUR/kWh
Annual operating hours: 6000 h/year

Perform exergy analysis for BOTH conditions, present comparison table, calculate annual savings.""",
        "expected": {
            "has_dead_state": True,
            "has_baseline_analysis": True,
            "has_scenario_analysis": True,
            "has_comparison_table": True,
            "has_annual_savings": True,
            "has_json_block": True,
        }
    },

    # --- HOTSPOT ---
    {
        "id": "hotspot-factory-01",
        "category": "hotspot_detection",
        "equipment": "factory",
        "difficulty": "hard",
        "prompt": """Perform a factory-level exergy hotspot analysis for a Food & Beverage Processing Plant.

The facility has the following 3 equipment items:

**Equipment 1: fire-tube steam boiler**
- Thermal capacity: 500 kW
- Fuel: natural gas
- Operating pressure: 8 bar
- Thermal efficiency: 86%
- Stack temperature: 200°C

**Equipment 2: screw compressor**
- Electrical power: 37 kW
- Discharge pressure: 8 bar
- Isentropic efficiency: 74%
- FAD: 5.5 m³/min

**Equipment 3: plate heat exchanger**
- Hot side: water, 85°C → 50°C, 1.5 kg/s
- Cold side: water, 12°C → 40°C, 2.3 kg/s

For each equipment calculate exergy metrics, then present ranking table and top 3 recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_multiple_equipment": True,
            "has_ranking_table": True,
            "has_recommendations": True,
            "has_json_block": True,
        }
    },

    # --- AVOIDABLE/UNAVOIDABLE ---
    {
        "id": "avun-pump-01",
        "category": "avoidable_unavoidable",
        "equipment": "pump",
        "difficulty": "hard",
        "prompt": """Perform an Avoidable/Unavoidable exergy destruction analysis for a centrifugal pump.

Operating conditions:
- Volume flow rate: 100 m³/h
- Total head: 50 m
- Motor power: 22 kW
- Pump efficiency: 65%
- Motor efficiency: 90%
- Fluid: water at 25°C

Reference (Best Available Technology): Grundfos CRE IE5
  - pump efficiency: 88%
  - motor efficiency: 97%

Calculate total exergy destruction, unavoidable component (BAT reference), avoidable component, and improvement priority.""",
        "expected": {
            "has_dead_state": True,
            "has_avoidable_calc": True,
            "has_unavoidable_calc": True,
            "has_avoidable_ratio": True,
            "has_json_block": True,
        }
    },
]

QUICK_TESTS = ["basic-compressor-01", "basic-boiler-01", "exergoecon-chiller-01",
               "egm-compressor-01", "hotspot-factory-01"]


# ============================================================
# STRUCTURAL CHECKS
# ============================================================

@dataclass
class BenchmarkResult:
    test_id: str
    category: str
    equipment: str
    difficulty: str
    model: str
    passed_checks: int = 0
    total_checks: int = 0
    checks: dict = field(default_factory=dict)
    response_time_s: float = 0
    response_length: int = 0
    output_preview: str = ""
    errors: list = field(default_factory=list)


def check_structure(output: str, expected: dict) -> dict:
    """Run structural and physics checks on model output."""
    checks = {}
    text = output.lower()

    # --- Universal structural checks ---

    # Dead state mentioned
    if expected.get("has_dead_state"):
        checks["dead_state"] = any(x in text for x in [
            "dead state", "t₀", "t0", "298.15", "25°c", "reference state"
        ])

    # Summary table
    if expected.get("has_summary_table"):
        checks["summary_table"] = ("|" in output and "---" in output) or \
                                   ("summary" in text and "|" in output)

    # JSON block
    if expected.get("has_json_block"):
        json_match = re.search(r'```json\s*[\{\[].+?[\}\]]\s*```', output, re.DOTALL)
        checks["json_block"] = json_match is not None
        if json_match:
            try:
                block = json_match.group()
                clean = block.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean)
                checks["json_parseable"] = True
                # Check for required keys
                if isinstance(parsed, dict):
                    checks["json_has_exergy_in"] = "exergy_in_kW" in parsed
                    checks["json_has_efficiency"] = "efficiency_pct" in parsed
                elif isinstance(parsed, list) and len(parsed) > 0:
                    checks["json_has_exergy_in"] = any("exergy_in_kW" in item for item in parsed if isinstance(item, dict))
                    checks["json_has_efficiency"] = any("efficiency_pct" in item for item in parsed if isinstance(item, dict))
            except (json.JSONDecodeError, TypeError):
                checks["json_parseable"] = False

    # Recommendations
    if expected.get("has_recommendations"):
        checks["recommendations"] = any(x in text for x in [
            "recommend", "suggestion", "improvement", "action", "measure"
        ])

    # --- Physics checks ---

    # Efficiency range
    if "efficiency_range" in expected:
        lo, hi = expected["efficiency_range"]
        # Try to extract from JSON first
        eff = None
        json_match = re.search(r'```json\s*[\{\[].+?[\}\]]\s*```', output, re.DOTALL)
        if json_match:
            try:
                clean = json_match.group().replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean)
                if isinstance(parsed, dict):
                    eff = parsed.get("efficiency_pct")
                elif isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict) and "efficiency_pct" in item:
                            eff = item["efficiency_pct"]
                            break
            except (json.JSONDecodeError, TypeError):
                pass
        # Fallback: regex
        if eff is None:
            m = re.search(r'(?:exergy|second.law)\s*efficiency.*?(\d+\.?\d*)\s*%', text)
            if m:
                eff = float(m.group(1))
        if eff is not None:
            checks["efficiency_physical"] = lo <= eff <= hi
            checks["efficiency_value"] = eff
        else:
            checks["efficiency_physical"] = None

    # T2s calculation (compressor)
    if expected.get("has_T2s_calc"):
        checks["T2s_mentioned"] = any(x in text for x in ["t₂s", "t2s", "isentropic temperature", "isentropic discharge"])

    # Steam tables reference (turbine)
    if expected.get("has_steam_tables"):
        checks["steam_tables"] = any(x in text for x in [
            "steam table", "enthalpy", "h₁", "h1", "h₂", "h2", "kj/kg"
        ])

    # Energy balance (HX)
    if expected.get("has_energy_balance"):
        checks["energy_balance"] = any(x in text for x in [
            "energy balance", "q_hot", "q_cold", "heat duty", "q ="
        ])

    # Waste streams (boiler)
    if expected.get("has_waste_streams"):
        checks["waste_streams"] = any(x in text for x in [
            "flue gas", "stack", "radiation", "waste", "exhaust"
        ])

    # --- Exergoeconomic checks ---
    if expected.get("has_crf_calc"):
        checks["crf_calc"] = any(x in text for x in ["crf", "capital recovery", "annuity"])
    if expected.get("has_cost_rate"):
        checks["cost_rate"] = any(x in text for x in ["ż", "z_dot", "cost rate", "eur/h", "€/h"])
    if expected.get("has_f_factor"):
        checks["f_factor"] = any(x in text for x in ["f-factor", "f factor", "exergoeconomic factor"])
    if "f_factor_range" in expected:
        m = re.search(r'f.?factor.*?(\d+\.?\d*)', text)
        if m:
            val = float(m.group(1))
            lo, hi = expected["f_factor_range"]
            checks["f_factor_valid"] = lo <= val <= hi

    # --- EGM checks ---
    if expected.get("has_entropy_gen"):
        checks["entropy_gen"] = any(x in text for x in ["ṡ_gen", "s_gen", "entropy generation", "entropy production"])
    if expected.get("has_bejan_number"):
        checks["bejan_number"] = any(x in text for x in ["bejan", "n_s", "entropy generation number"])
    if expected.get("has_grade"):
        checks["grade"] = any(x in text for x in ["grade a", "grade b", "grade c", "grade d", "grade e", "grade f"])
    if expected.get("has_mechanism_decomposition"):
        checks["mechanism_decomp"] = any(x in text for x in ["heat transfer", "friction", "pressure drop", "mixing"])

    # --- What-if checks ---
    if expected.get("has_baseline_analysis"):
        checks["baseline"] = any(x in text for x in ["baseline", "current", "existing"])
    if expected.get("has_scenario_analysis"):
        checks["scenario"] = any(x in text for x in ["scenario", "modified", "proposed", "improved"])
    if expected.get("has_comparison_table"):
        checks["comparison_table"] = any(x in text for x in ["delta", "change", "saving"]) and "|" in output
    if expected.get("has_annual_savings"):
        checks["annual_savings"] = any(x in text for x in ["annual", "eur/year", "€/year", "kwh/year"])

    # --- Hotspot checks ---
    if expected.get("has_multiple_equipment"):
        checks["multi_equipment"] = sum(1 for x in ["equipment 1", "equipment 2", "equipment 3"] if x in text) >= 2
    if expected.get("has_ranking_table"):
        checks["ranking"] = any(x in text for x in ["rank", "priority", "hotspot", "#1"])

    # --- AV/UN checks ---
    if expected.get("has_avoidable_calc"):
        checks["avoidable"] = any(x in text for x in ["avoidable", "ex_d,av", "ex_d_av"])
    if expected.get("has_unavoidable_calc"):
        checks["unavoidable"] = any(x in text for x in ["unavoidable", "ex_d,un", "ex_d_un", "bat", "best available"])
    if expected.get("has_avoidable_ratio"):
        checks["avoidable_ratio"] = any(x in text for x in ["avoidable ratio", "ar =", "improvement potential"])

    return checks


# ============================================================
# MODEL RUNNER
# ============================================================

def run_ollama(model: str, prompt: str, timeout: int = 600) -> tuple:
    """Run ollama and return (output, elapsed_seconds)."""
    start = time.time()
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start
        return result.stdout.strip(), elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return f"[TIMEOUT after {timeout}s]", elapsed
    except FileNotFoundError:
        return "[ERROR: ollama not found]", 0


# ============================================================
# BENCHMARK RUNNER
# ============================================================

def run_benchmark(
    model: str = "entropy-hunter",
    test_ids: list = None,
    quick: bool = False,
    output_dir: str = None,
) -> list:
    """Run all benchmark tests and return results."""

    if quick:
        tests = [t for t in TEST_CASES if t["id"] in QUICK_TESTS]
    elif test_ids:
        tests = [t for t in TEST_CASES if t["id"] in test_ids]
    else:
        tests = TEST_CASES

    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = Path("eval/benchmark")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"🧪 EntropyHunter Benchmark")
    print(f"{'='*60}")
    print(f"   Model: {model}")
    print(f"   Tests: {len(tests)}")
    print(f"   Output: {out_dir}")
    print()

    results = []

    for i, test in enumerate(tests):
        test_id = test["id"]
        print(f"[{i+1}/{len(tests)}] {test_id} ({test['category']}/{test['equipment']})...", end="", flush=True)

        # Run model
        output, elapsed = run_ollama(model, test["prompt"])

        # Check structure
        checks = check_structure(output, test["expected"])
        passed = sum(1 for v in checks.values() if v is True)
        total = sum(1 for v in checks.values() if v is True or v is False)
        passed = sum(1 for v in checks.values() if v is True)

        result = BenchmarkResult(
            test_id=test_id,
            category=test["category"],
            equipment=test["equipment"],
            difficulty=test["difficulty"],
            model=model,
            passed_checks=passed,
            total_checks=total,
            checks=checks,
            response_time_s=round(elapsed, 1),
            response_length=len(output),
            output_preview=output[:200],
        )
        results.append(result)

        pct = f"{passed}/{total}" if total > 0 else "N/A"
        print(f" {pct} checks | {elapsed:.0f}s | {len(output):,} chars")

        # Save individual response
        resp_path = out_dir / f"{test_id}_{model.replace(':', '_')}.md"
        with open(resp_path, "w") as f:
            f.write(f"# {test_id}\n")
            f.write(f"Model: {model}\n")
            f.write(f"Time: {elapsed:.1f}s\n")
            f.write(f"Checks: {pct}\n\n")
            f.write(output)

    return results


def print_summary(results: list, model: str):
    """Print benchmark summary with scorecard."""
    print(f"\n{'='*60}")
    print(f"📊 Benchmark Results: {model}")
    print(f"{'='*60}\n")

    # Per-test results
    print(f"{'Test ID':<30s} {'Category':<20s} {'Checks':>8s} {'Time':>6s} {'Len':>8s}")
    print("-" * 75)

    total_passed = 0
    total_checks = 0

    for r in results:
        pct = f"{r.passed_checks}/{r.total_checks}"
        print(f"{r.test_id:<30s} {r.category:<20s} {pct:>8s} {r.response_time_s:>5.0f}s {r.response_length:>7,}")
        total_passed += r.passed_checks
        total_checks += r.total_checks

    # Category scores
    print(f"\n{'='*60}")
    print(f"📈 Scores by Category")
    print(f"{'='*60}")

    categories = {}
    for r in results:
        cat = r.category
        if cat not in categories:
            categories[cat] = {"passed": 0, "total": 0, "count": 0}
        categories[cat]["passed"] += r.passed_checks
        categories[cat]["total"] += r.total_checks
        categories[cat]["count"] += 1

    for cat, stats in sorted(categories.items()):
        score = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"  {cat:<25s} {bar} {score:5.1f}% ({stats['passed']}/{stats['total']})")

    # Check-level breakdown
    print(f"\n{'='*60}")
    print(f"🔍 Check-Level Pass Rates")
    print(f"{'='*60}")

    check_stats = {}
    for r in results:
        for check_name, value in r.checks.items():
            if isinstance(value, bool):
                if check_name not in check_stats:
                    check_stats[check_name] = {"passed": 0, "total": 0}
                check_stats[check_name]["total"] += 1
                if value:
                    check_stats[check_name]["passed"] += 1

    for name, stats in sorted(check_stats.items(), key=lambda x: x[1]["passed"]/max(x[1]["total"],1)):
        rate = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        icon = "✅" if rate >= 80 else "⚠️" if rate >= 50 else "❌"
        print(f"  {icon} {name:<30s} {stats['passed']}/{stats['total']} ({rate:.0f}%)")

    # Overall score
    overall = total_passed / total_checks * 100 if total_checks > 0 else 0
    print(f"\n{'='*60}")
    grade = "A" if overall >= 90 else "B" if overall >= 75 else "C" if overall >= 60 else "D" if overall >= 40 else "F"
    print(f"🏆 Overall Score: {overall:.1f}% (Grade: {grade})")
    print(f"   {total_passed}/{total_checks} checks passed")

    avg_time = sum(r.response_time_s for r in results) / len(results) if results else 0
    print(f"   Average response time: {avg_time:.1f}s")
    print(f"{'='*60}\n")

    return overall


def save_results(results: list, model: str, output_dir: str = None):
    """Save benchmark results to JSON."""
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = Path("eval/benchmark")
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = out_dir / f"results_{model.replace(':', '_')}_{timestamp}.json"

    data = {
        "model": model,
        "timestamp": timestamp,
        "num_tests": len(results),
        "results": [
            {
                "test_id": r.test_id,
                "category": r.category,
                "equipment": r.equipment,
                "difficulty": r.difficulty,
                "passed_checks": r.passed_checks,
                "total_checks": r.total_checks,
                "checks": {k: v for k, v in r.checks.items()},
                "response_time_s": r.response_time_s,
                "response_length": r.response_length,
            }
            for r in results
        ]
    }

    with open(results_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📁 Results saved: {results_path}")


# ============================================================
# COMPARISON MODE
# ============================================================

def run_comparison(models: list, quick: bool = False):
    """Run benchmark on multiple models and compare."""
    all_results = {}

    for model in models:
        print(f"\n{'#'*60}")
        print(f"# Running: {model}")
        print(f"{'#'*60}")
        results = run_benchmark(model=model, quick=quick)
        all_results[model] = results
        save_results(results, model)

    # Comparison table
    print(f"\n{'='*60}")
    print(f"📊 Model Comparison")
    print(f"{'='*60}\n")

    header = f"{'Test ID':<30s}"
    for model in models:
        header += f" {model:>15s}"
    print(header)
    print("-" * (30 + 16 * len(models)))

    test_ids = [r.test_id for r in all_results[models[0]]]
    for tid in test_ids:
        row = f"{tid:<30s}"
        for model in models:
            r = next((r for r in all_results[model] if r.test_id == tid), None)
            if r:
                row += f" {r.passed_checks}/{r.total_checks:>10s}"
            else:
                row += f" {'N/A':>15s}"
        print(row)

    print()
    for model in models:
        results = all_results[model]
        total_p = sum(r.passed_checks for r in results)
        total_c = sum(r.total_checks for r in results)
        pct = total_p / total_c * 100 if total_c > 0 else 0
        print(f"  {model:<20s} {pct:.1f}% ({total_p}/{total_c})")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EntropyHunter Model Benchmark")
    parser.add_argument("--model", "-m", type=str, default="entropy-hunter",
                        help="Ollama model name")
    parser.add_argument("--compare", "-c", nargs="+", default=None,
                        help="Compare multiple models (e.g. --compare entropy-hunter qwen2.5:7b)")
    parser.add_argument("--quick", "-q", action="store_true",
                        help="Run only 5 key tests")
    parser.add_argument("--output-dir", "-o", type=str, default=None)
    parser.add_argument("--test", "-t", nargs="+", default=None,
                        help="Run specific test IDs")

    args = parser.parse_args()

    if args.compare:
        run_comparison(args.compare, quick=args.quick)
    else:
        results = run_benchmark(
            model=args.model,
            test_ids=args.test,
            quick=args.quick,
            output_dir=args.output_dir,
        )
        overall = print_summary(results, args.model)
        save_results(results, args.model, args.output_dir)
