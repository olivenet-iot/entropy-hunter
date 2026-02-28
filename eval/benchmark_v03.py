"""
EntropyHunter — Phase A Comprehensive Benchmark (v0.3)

40 test cases × N runs × temperature sweep = full capability map of v0.2

Changes from benchmark.py:
  - 40 tests (was 10) — every family has 4-12 tests
  - Multi-run: --runs 3 → mean ± std per test
  - Temperature sweep: --sweep → test at 0.1, 0.3, 0.5, 0.7
  - Ollama HTTP API (not subprocess) — allows per-request temp override
  - --exclude-checks json_block → removes known-failed checks from scoring
  - GCE GPU compatible (ollama API works same on GPU)
  - Backward compatible: still works with --model entropy-hunter-v02

Usage:
    # Single run (quick check)
    python benchmark_v03.py --model entropy-hunter-v02

    # Full Phase A: 3 runs per test
    python benchmark_v03.py --model entropy-hunter-v02 --runs 3

    # Temperature sweep (mevcut testler, 4 temp × 3 run)
    python benchmark_v03.py --model entropy-hunter-v02 --sweep --runs 3

    # Exclude json_block from scoring
    python benchmark_v03.py --model entropy-hunter-v02 --runs 3 --exclude-checks json_block

    # Compare models
    python benchmark_v03.py --compare entropy-hunter-v02 qwen2.5:7b --runs 3

    # Quick mode (10 original tests only)
    python benchmark_v03.py --model entropy-hunter-v02 --quick

    # Run specific category
    python benchmark_v03.py --model entropy-hunter-v02 --category entropy_generation --runs 5
"""

import argparse
import json
import math
import re
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# ============================================================
# TEST CASES — 40 tests across 6 analysis families
# ============================================================

TEST_CASES = [

    # ================================================================
    # BASIC EXERGY — 12 tests (5 existing + 7 new)
    # ================================================================
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
            "efficiency_range": (15, 60),
            "has_summary_table": True,
            "has_json_block": True,
            "has_recommendations": True,
        }
    },
    {
        "id": "basic-compressor-02",
        "category": "basic_exergy",
        "equipment": "compressor",
        "difficulty": "medium",
        "prompt": """Perform a complete exergy analysis for a two-stage reciprocating air compressor with intercooler.

Operating conditions:
- Total electrical power input: 110 kW
- Air inlet temperature: 30°C
- Inlet pressure: 1.013 bar (atmospheric)
- Intercooler outlet temperature: 40°C
- Intermediate pressure: 4 bar
- Final discharge pressure: 16 bar
- Overall isentropic efficiency: 70%
- Volume flow rate (FAD): 12.0 m³/min
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_T2s_calc": True,
            "efficiency_range": (15, 55),
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
            "efficiency_range": (15, 45),
            "has_waste_streams": True,
            "has_summary_table": True,
            "has_json_block": True,
        }
    },
    {
        "id": "basic-boiler-02",
        "category": "basic_exergy",
        "equipment": "boiler",
        "difficulty": "hard",
        "prompt": """Perform a complete exergy analysis for a condensing gas boiler used in a district heating system.

Operating conditions:
- Thermal capacity: 3000 kW
- Fuel: natural gas (LHV = 36.6 MJ/m³, chemical exergy factor = 1.04)
- Supply water temperature: 80°C
- Return water temperature: 50°C
- Flue gas exit temperature: 55°C (below dew point — condensing mode)
- Thermal (first-law) efficiency: 96% (LHV basis)
- Water flow rate: 23.9 kg/s
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "efficiency_range": (15, 50),
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
        "id": "basic-hx-02",
        "category": "basic_exergy",
        "equipment": "heat_exchanger",
        "difficulty": "hard",
        "prompt": """Perform a complete exergy analysis for a plate heat exchanger used in waste heat recovery.

Operating conditions:
- Hot side: flue gas (Cp = 1.05 kJ/kgK), inlet 220°C → outlet 120°C, flow rate 3.2 kg/s
- Cold side: thermal oil (Cp = 2.1 kJ/kgK), inlet 60°C → outlet 150°C, flow rate 1.8 kg/s
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_energy_balance": True,
            "efficiency_range": (30, 85),
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
        "id": "basic-pump-02",
        "category": "basic_exergy",
        "equipment": "pump",
        "difficulty": "medium",
        "prompt": """Perform a complete exergy analysis for a multistage centrifugal boiler feedwater pump.

Operating conditions:
- Volume flow rate: 30 m³/h
- Suction pressure: 2 bar
- Discharge pressure: 25 bar
- Motor electrical power: 35 kW
- Pump isentropic efficiency: 68%
- Motor efficiency: 94%
- Fluid: water at 105°C (subcooled, from deaerator)
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "efficiency_range": (35, 80),
            "has_summary_table": True,
            "has_json_block": True,
            "has_recommendations": True,
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
            "has_T2s_calc": True,
            "efficiency_range": (50, 90),
            "has_summary_table": True,
            "has_json_block": True,
        }
    },
    {
        "id": "basic-turbine-02",
        "category": "basic_exergy",
        "equipment": "steam_turbine",
        "difficulty": "hard",
        "prompt": """Perform a complete exergy analysis for a condensing steam turbine.

Operating conditions:
- Inlet steam pressure: 60 bar
- Inlet steam temperature: 480°C (superheated)
- Condenser pressure: 0.08 bar
- Steam mass flow rate: 12 kg/s
- Isentropic efficiency: 82%
- Generator efficiency: 97%
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_steam_tables": True,
            "has_T2s_calc": True,
            "efficiency_range": (50, 92),
            "has_summary_table": True,
            "has_json_block": True,
        }
    },
    {
        "id": "basic-chiller-01",
        "category": "basic_exergy",
        "equipment": "chiller",
        "difficulty": "medium",
        "prompt": """Perform a complete exergy analysis for an air-cooled screw chiller.

Operating conditions:
- Cooling capacity: 200 kW
- Chilled water supply temperature: 7°C
- Chilled water return temperature: 12°C
- Ambient (condenser air inlet) temperature: 35°C
- COP: 2.8
- Refrigerant: R410A
- Compressor electrical power: 71.4 kW
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "efficiency_range": (10, 50),
            "has_summary_table": True,
            "has_json_block": True,
            "has_recommendations": True,
        }
    },
    {
        "id": "basic-dryer-01",
        "category": "basic_exergy",
        "equipment": "dryer",
        "difficulty": "medium",
        "prompt": """Perform a complete exergy analysis for a rotary drum dryer.

Operating conditions:
- Product: wood chips
- Wet feed rate: 2.0 t/h
- Moisture content in: 50% (wet basis)
- Moisture content out: 12% (wet basis)
- Hot gas inlet temperature: 350°C
- Hot gas outlet temperature: 90°C
- Gas flow rate: 5.0 kg/s
- Thermal input: 800 kW
- Operating mode: full_load

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations.""",
        "expected": {
            "has_dead_state": True,
            "efficiency_range": (10, 50),
            "has_summary_table": True,
            "has_json_block": True,
            "has_recommendations": True,
        }
    },

    # ================================================================
    # EXERGOECONOMIC — 7 tests (1 existing + 6 new)
    # ================================================================
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
    {
        "id": "exergoecon-compressor-01",
        "category": "exergoeconomic",
        "equipment": "compressor",
        "difficulty": "medium",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a screw air compressor.

Operating conditions:
- Electrical power input: 75 kW
- Air inlet temperature: 25°C
- Discharge pressure: 10 bar
- Isentropic efficiency: 72%
- Volume flow rate (FAD): 10.5 m³/min
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €28,000
- Installation factor: 1.45
- Interest rate: 6%
- Equipment lifetime: 15 years
- Maintenance cost factor: 5% of TCI/year
- Annual operating hours: 7000 h/year
- Energy cost (electricity): 0.10 EUR/kWh

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
    {
        "id": "exergoecon-boiler-01",
        "category": "exergoeconomic",
        "equipment": "boiler",
        "difficulty": "hard",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a water-tube steam boiler.

Operating conditions:
- Thermal capacity: 2000 kW
- Fuel: natural gas
- Steam pressure: 12 bar
- Stack temperature: 190°C
- Feedwater temperature: 80°C
- Thermal efficiency: 87%
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €145,000
- Installation factor: 1.80
- Interest rate: 7%
- Equipment lifetime: 25 years
- Maintenance cost factor: 3% of TCI/year
- Annual operating hours: 8000 h/year
- Fuel cost: 0.035 EUR/kWh (natural gas)

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
    {
        "id": "exergoecon-hx-01",
        "category": "exergoeconomic",
        "equipment": "heat_exchanger",
        "difficulty": "medium",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a plate heat exchanger in a district heating substation.

Operating conditions:
- Hot side: district heating water, inlet 85°C → outlet 45°C, flow rate 4.0 kg/s
- Cold side: building heating water, inlet 30°C → outlet 60°C, flow rate 4.5 kg/s
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €12,000
- Installation factor: 1.40
- Interest rate: 5%
- Equipment lifetime: 20 years
- Maintenance cost factor: 2% of TCI/year
- Annual operating hours: 5000 h/year
- Heat cost (from district network): 0.06 EUR/kWh

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
    {
        "id": "exergoecon-pump-01",
        "category": "exergoeconomic",
        "equipment": "pump",
        "difficulty": "easy",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a centrifugal process pump.

Operating conditions:
- Volume flow rate: 80 m³/h
- Total head: 40 m
- Motor electrical power: 15 kW
- Pump hydraulic efficiency: 75%
- Motor efficiency: 93%
- Fluid: water at 25°C
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €4,500
- Installation factor: 1.50
- Interest rate: 6%
- Equipment lifetime: 15 years
- Maintenance cost factor: 6% of TCI/year
- Annual operating hours: 8000 h/year
- Energy cost (electricity): 0.11 EUR/kWh

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
    {
        "id": "exergoecon-turbine-01",
        "category": "exergoeconomic",
        "equipment": "steam_turbine",
        "difficulty": "hard",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a back-pressure steam turbine.

Operating conditions:
- Inlet steam: 30 bar, 350°C (superheated)
- Outlet pressure: 3 bar
- Steam mass flow rate: 8 kg/s
- Isentropic efficiency: 76%
- Generator efficiency: 96%
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €320,000
- Installation factor: 2.00
- Interest rate: 8%
- Equipment lifetime: 30 years
- Maintenance cost factor: 3% of TCI/year
- Annual operating hours: 7500 h/year
- Steam cost (from boiler): 0.025 EUR/kWh

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
    {
        "id": "exergoecon-dryer-01",
        "category": "exergoeconomic",
        "equipment": "dryer",
        "difficulty": "hard",
        "prompt": """Perform a complete exergoeconomic (SPECO) analysis for a spray dryer in a dairy plant.

Operating conditions:
- Product: milk powder
- Evaporation rate: 1500 kg/h water removed
- Hot air inlet temperature: 200°C
- Hot air outlet temperature: 90°C
- Air mass flow rate: 8.5 kg/s
- Thermal input: 1200 kW (from natural gas burner)
- Operating mode: full_load

Economic data:
- Purchase equipment cost (PEC): €380,000
- Installation factor: 1.90
- Interest rate: 7%
- Equipment lifetime: 20 years
- Maintenance cost factor: 4% of TCI/year
- Annual operating hours: 6500 h/year
- Fuel cost (natural gas): 0.04 EUR/kWh

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

    # ================================================================
    # ENTROPY GENERATION (EGM) — 7 tests (1 existing + 6 new)
    # ================================================================
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
    {
        "id": "egm-compressor-02",
        "category": "entropy_generation",
        "equipment": "compressor",
        "difficulty": "hard",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a screw air compressor operating at part load.

Operating conditions:
- Nominal electrical power: 90 kW (full load)
- Current electrical power: 65 kW (part load ~72%)
- Air inlet temperature: 35°C (summer operation)
- Discharge pressure: 8 bar
- Isentropic efficiency at part load: 68%
- Volume flow rate (FAD): 9.0 m³/min
- Operating mode: part_load

Focus on:
1. Total entropy generation rate (Ṡ_gen) via Gouy-Stodola theorem
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (heat transfer vs friction vs mixing)
4. Part-load penalty analysis
5. Recommendations for reduction""",
        "expected": {
            "has_dead_state": True,
            "has_entropy_gen": True,
            "has_bejan_number": True,
            "has_grade": True,
            "has_mechanism_decomposition": True,
            "has_json_block": True,
        }
    },
    {
        "id": "egm-boiler-01",
        "category": "entropy_generation",
        "equipment": "boiler",
        "difficulty": "medium",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a fire-tube steam boiler.

Operating conditions:
- Thermal capacity: 1500 kW
- Fuel: natural gas (adiabatic flame temperature ~1950°C)
- Steam pressure: 10 bar (saturation temperature: 179.9°C)
- Feedwater temperature: 60°C
- Stack temperature: 200°C
- Thermal efficiency: 86%
- Operating mode: full_load

Focus on:
1. Total entropy generation rate (Ṡ_gen) — identify combustion irreversibility
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (combustion, heat transfer across ΔT, stack losses)
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
    {
        "id": "egm-hx-01",
        "category": "entropy_generation",
        "equipment": "heat_exchanger",
        "difficulty": "medium",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a shell-and-tube heat exchanger.

Operating conditions:
- Hot side: process water, inlet 95°C → outlet 50°C, flow rate 3.0 kg/s
- Cold side: cooling water, inlet 20°C → outlet 40°C, flow rate 5.0 kg/s
- Pressure drop hot side: 0.4 bar
- Pressure drop cold side: 0.25 bar
- Operating mode: full_load

Focus on:
1. Total entropy generation rate (Ṡ_gen)
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (heat transfer across ΔT vs pressure drop/friction)
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
    {
        "id": "egm-pump-01",
        "category": "entropy_generation",
        "equipment": "pump",
        "difficulty": "easy",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a centrifugal cooling water pump.

Operating conditions:
- Volume flow rate: 120 m³/h
- Total head: 25 m
- Motor electrical power: 12 kW
- Pump hydraulic efficiency: 70%
- Motor efficiency: 91%
- Fluid: water at 28°C
- Operating mode: full_load

Focus on:
1. Total entropy generation rate (Ṡ_gen) via Gouy-Stodola theorem
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (fluid friction vs mechanical losses)
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
    {
        "id": "egm-turbine-01",
        "category": "entropy_generation",
        "equipment": "steam_turbine",
        "difficulty": "hard",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a back-pressure steam turbine.

Operating conditions:
- Inlet steam: 25 bar, 350°C (superheated)
- Outlet pressure: 5 bar
- Steam mass flow rate: 3 kg/s
- Isentropic efficiency: 75%
- Generator efficiency: 94%
- Operating mode: full_load

Focus on:
1. Total entropy generation rate (Ṡ_gen) using actual vs isentropic enthalpy
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (blade friction, tip leakage, moisture losses)
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
    {
        "id": "egm-chiller-01",
        "category": "entropy_generation",
        "equipment": "chiller",
        "difficulty": "medium",
        "prompt": """Perform an Entropy Generation Minimization (EGM) analysis for a water-cooled centrifugal chiller.

Operating conditions:
- Cooling capacity: 350 kW
- Evaporator temperature: 4°C
- Condenser temperature: 38°C
- COP: 5.0
- Compressor electrical power: 70 kW
- Refrigerant: R134a
- Operating mode: full_load

Focus on:
1. Total entropy generation rate (Ṡ_gen) comparing actual COP vs Carnot COP
2. Bejan number (N_s) with grade assignment
3. Decomposition by mechanism (compressor, evaporator ΔT, condenser ΔT, expansion valve)
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

    # ================================================================
    # WHAT-IF COMPARISON — 5 tests (1 existing + 4 new)
    # ================================================================
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
    {
        "id": "whatif-compressor-01",
        "category": "whatif_comparison",
        "equipment": "compressor",
        "difficulty": "medium",
        "prompt": """Perform a what-if exergy comparison for a screw air compressor.

**Scenario:** Variable Speed Drive (VSD) installation

### BASELINE
- Electrical power input: 55 kW (load/unload control)
- Air inlet temperature: 25°C
- Discharge pressure: 8 bar
- Isentropic efficiency: 72%
- Average load factor: 65% (significant unloaded running)
- Operating mode: part_load

### MODIFIED SCENARIO (with VSD)
- Electrical power input: 38 kW (speed-matched to demand)
- Isentropic efficiency at part load: 74% (improved at reduced speed)
- Average load factor: 95% (minimal unloaded time)
- All other parameters unchanged

Energy cost: 0.11 EUR/kWh
Annual operating hours: 7500 h/year

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
    {
        "id": "whatif-hx-01",
        "category": "whatif_comparison",
        "equipment": "heat_exchanger",
        "difficulty": "medium",
        "prompt": """Perform a what-if exergy comparison for a shell-and-tube heat exchanger.

**Scenario:** Fouling removal — cleaning heat exchanger tubes to restore design performance

### BASELINE (fouled condition)
- Hot side: process fluid (Cp = 2.5 kJ/kgK), inlet 120°C → outlet 80°C, flow rate 2.0 kg/s
- Cold side: water, inlet 20°C → outlet 50°C, flow rate 3.2 kg/s
- Operating mode: degraded

### MODIFIED SCENARIO (cleaned condition)
- Hot side: inlet 120°C → outlet 65°C (better heat transfer), flow rate 2.0 kg/s
- Cold side: inlet 20°C → outlet 58°C (higher outlet temp), flow rate 3.2 kg/s
- All other parameters unchanged

Energy cost: 0.08 EUR/kWh (thermal)
Annual operating hours: 8000 h/year

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
    {
        "id": "whatif-pump-01",
        "category": "whatif_comparison",
        "equipment": "pump",
        "difficulty": "easy",
        "prompt": """Perform a what-if exergy comparison for a centrifugal process pump.

**Scenario:** Impeller trimming — reducing impeller diameter to match actual system requirements

### BASELINE
- Volume flow rate: 60 m³/h (throttled from 80 m³/h by control valve)
- Total head: 35 m (pump provides 50 m, valve drops 15 m)
- Motor power: 18 kW
- Pump efficiency: 68% (at throttled operating point)
- Motor efficiency: 91%
- Fluid: water at 25°C
- Operating mode: full_load

### MODIFIED SCENARIO (trimmed impeller)
- Volume flow rate: 60 m³/h (no throttling needed)
- Total head: 35 m (matched to system)
- Motor power: 11 kW
- Pump efficiency: 76% (at best efficiency point)
- Motor efficiency: 91%

Energy cost: 0.10 EUR/kWh
Annual operating hours: 8000 h/year

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
    {
        "id": "whatif-chiller-01",
        "category": "whatif_comparison",
        "equipment": "chiller",
        "difficulty": "medium",
        "prompt": """Perform a what-if exergy comparison for a centrifugal chiller.

**Scenario:** Raising chilled water supply temperature from 6°C to 9°C

### BASELINE
- Cooling capacity: 400 kW
- Chilled water supply: 6°C
- Chilled water return: 12°C
- Condenser water temperature: 30°C
- COP: 5.5
- Operating mode: full_load

### MODIFIED SCENARIO
- Chilled water supply: 9°C (raised setpoint)
- COP: 6.4 (improved due to smaller temperature lift)
- All other parameters unchanged

Energy cost: 0.12 EUR/kWh
Annual operating hours: 4000 h/year

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

    # ================================================================
    # HOTSPOT DETECTION — 4 tests (1 existing + 3 new)
    # ================================================================
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
    {
        "id": "hotspot-factory-02",
        "category": "hotspot_detection",
        "equipment": "factory",
        "difficulty": "hard",
        "prompt": """Perform a factory-level exergy hotspot analysis for a Chemical Processing Plant.

The facility has the following 4 equipment items:

**Equipment 1: water-tube steam boiler**
- Thermal capacity: 3000 kW
- Fuel: natural gas
- Operating pressure: 15 bar
- Thermal efficiency: 84%
- Stack temperature: 220°C

**Equipment 2: centrifugal compressor (process gas)**
- Electrical power: 200 kW
- Gas inlet temperature: 40°C
- Discharge pressure: 6 bar
- Isentropic efficiency: 77%

**Equipment 3: shell-and-tube heat exchanger (reactor feed preheater)**
- Hot side: reactor effluent, 180°C → 90°C, Cp = 2.3 kJ/kgK, 4.0 kg/s
- Cold side: reactor feed, 25°C → 120°C, Cp = 2.1 kJ/kgK, 3.5 kg/s

**Equipment 4: centrifugal pump (cooling water)**
- Flow rate: 200 m³/h
- Head: 35 m
- Motor power: 30 kW
- Efficiency: 70%

For each equipment calculate exergy metrics, then present ranking table and top 3 recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_multiple_equipment": True,
            "has_ranking_table": True,
            "has_recommendations": True,
            "has_json_block": True,
        }
    },
    {
        "id": "hotspot-factory-03",
        "category": "hotspot_detection",
        "equipment": "factory",
        "difficulty": "hard",
        "prompt": """Perform a building-level exergy hotspot analysis for an HVAC system in a commercial building.

The system has the following 3 equipment items:

**Equipment 1: water-cooled centrifugal chiller**
- Cooling capacity: 500 kW
- COP: 5.2
- Evaporator temp: 5°C
- Condenser temp: 35°C

**Equipment 2: chilled water distribution pump**
- Flow rate: 85 m³/h
- Head: 25 m
- Motor power: 11 kW
- Pump efficiency: 72%

**Equipment 3: air handling unit heating coil (heat exchanger)**
- Hot side: hot water, 70°C → 45°C, 1.8 kg/s
- Cold side: air (Cp = 1.005 kJ/kgK), 5°C → 25°C, 8.0 kg/s

For each equipment calculate exergy metrics, then present ranking table and top 3 recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_multiple_equipment": True,
            "has_ranking_table": True,
            "has_recommendations": True,
            "has_json_block": True,
        }
    },
    {
        "id": "hotspot-factory-04",
        "category": "hotspot_detection",
        "equipment": "factory",
        "difficulty": "hard",
        "prompt": """Perform a factory-level exergy hotspot analysis for a Dairy Processing Plant.

The facility has the following 3 equipment items:

**Equipment 1: fire-tube steam boiler (pasteurization)**
- Thermal capacity: 800 kW
- Fuel: natural gas
- Steam pressure: 6 bar
- Thermal efficiency: 85%
- Stack temperature: 210°C

**Equipment 2: ammonia screw chiller (cold storage)**
- Cooling capacity: 250 kW
- Evaporator temperature: -5°C
- Condenser temperature: 40°C
- COP: 3.2

**Equipment 3: plate heat exchanger (milk pasteurizer — regeneration section)**
- Hot side: pasteurized milk, 72°C → 35°C, 2.5 kg/s, Cp = 3.93 kJ/kgK
- Cold side: raw milk, 4°C → 62°C, 2.5 kg/s, Cp = 3.93 kJ/kgK

For each equipment calculate exergy metrics, then present ranking table and top 3 recommendations.""",
        "expected": {
            "has_dead_state": True,
            "has_multiple_equipment": True,
            "has_ranking_table": True,
            "has_recommendations": True,
            "has_json_block": True,
        }
    },

    # ================================================================
    # AVOIDABLE / UNAVOIDABLE — 5 tests (1 existing + 4 new)
    # ================================================================
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
    {
        "id": "avun-compressor-01",
        "category": "avoidable_unavoidable",
        "equipment": "compressor",
        "difficulty": "hard",
        "prompt": """Perform an Avoidable/Unavoidable exergy destruction analysis for a screw air compressor.

Operating conditions:
- Electrical power input: 55 kW
- Air inlet temperature: 25°C
- Discharge pressure: 8 bar
- Isentropic efficiency: 72%
- Volume flow rate (FAD): 8.0 m³/min
- Operating mode: full_load

Reference (Best Available Technology): Atlas Copco GA VSD+
  - isentropic efficiency: 90%
  - specific energy: 5.8 kW/(m³/min) at 8 bar

Calculate total exergy destruction, unavoidable component (BAT reference), avoidable component, and improvement priority.""",
        "expected": {
            "has_dead_state": True,
            "has_avoidable_calc": True,
            "has_unavoidable_calc": True,
            "has_avoidable_ratio": True,
            "has_json_block": True,
        }
    },
    {
        "id": "avun-boiler-01",
        "category": "avoidable_unavoidable",
        "equipment": "boiler",
        "difficulty": "hard",
        "prompt": """Perform an Avoidable/Unavoidable exergy destruction analysis for a fire-tube steam boiler.

Operating conditions:
- Thermal capacity: 1000 kW
- Fuel: natural gas
- Steam pressure: 10 bar
- Stack temperature: 220°C
- Feedwater temperature: 50°C
- Thermal efficiency: 84%
- Operating mode: full_load

Reference (Best Available Technology): Condensing boiler with economizer
  - Thermal efficiency: 97% (LHV basis)
  - Stack temperature: 55°C
  - Feedwater temperature: 105°C (with economizer + deaerator)

Calculate total exergy destruction, unavoidable component (BAT reference), avoidable component, and improvement priority.""",
        "expected": {
            "has_dead_state": True,
            "has_avoidable_calc": True,
            "has_unavoidable_calc": True,
            "has_avoidable_ratio": True,
            "has_json_block": True,
        }
    },
    {
        "id": "avun-hx-01",
        "category": "avoidable_unavoidable",
        "equipment": "heat_exchanger",
        "difficulty": "medium",
        "prompt": """Perform an Avoidable/Unavoidable exergy destruction analysis for a shell-and-tube heat exchanger.

Operating conditions:
- Hot side: water, inlet 80°C → outlet 50°C, flow rate 2.0 kg/s
- Cold side: water, inlet 15°C → outlet 40°C, flow rate 2.4 kg/s
- LMTD: 37°C
- Operating mode: full_load

Reference (Best Available Technology): Compact plate heat exchanger
  - Hot outlet: 42°C (closer approach temperature)
  - Cold outlet: 48°C
  - LMTD: 22°C

Calculate total exergy destruction, unavoidable component (BAT reference), avoidable component, and improvement priority.""",
        "expected": {
            "has_dead_state": True,
            "has_avoidable_calc": True,
            "has_unavoidable_calc": True,
            "has_avoidable_ratio": True,
            "has_json_block": True,
        }
    },
    {
        "id": "avun-turbine-01",
        "category": "avoidable_unavoidable",
        "equipment": "steam_turbine",
        "difficulty": "hard",
        "prompt": """Perform an Avoidable/Unavoidable exergy destruction analysis for a back-pressure steam turbine.

Operating conditions:
- Inlet steam: 20 bar, 300°C (superheated)
- Outlet pressure: 3 bar
- Steam mass flow rate: 4 kg/s
- Isentropic efficiency: 72%
- Generator efficiency: 93%
- Operating mode: full_load

Reference (Best Available Technology): Modern high-efficiency turbine
  - Isentropic efficiency: 90%
  - Generator efficiency: 98%

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

# Original 10 test IDs for --quick mode
QUICK_TESTS = [
    "basic-compressor-01", "basic-boiler-01", "basic-hx-01",
    "basic-pump-01", "basic-turbine-01", "exergoecon-chiller-01",
    "egm-compressor-01", "whatif-boiler-01", "hotspot-factory-01",
    "avun-pump-01",
]


# ============================================================
# STRUCTURAL CHECKS (same logic as v0.2 benchmark.py)
# ============================================================

@dataclass
class BenchmarkResult:
    test_id: str
    category: str
    equipment: str
    difficulty: str
    model: str
    run_number: int = 1
    temperature: float = 0.7
    passed_checks: int = 0
    total_checks: int = 0
    checks: dict = field(default_factory=dict)
    response_time_s: float = 0
    response_length: int = 0
    output_preview: str = ""
    errors: list = field(default_factory=list)


def _extract_exergy_efficiency(output: str) -> float | None:
    """
    Extract exergy/second-law efficiency from model output.
    
    Multi-strategy approach (v0.3 fix):
    1. JSON block (if present)
    2. Line-level: find lines with "exergy efficiency" + number, EXCLUDE false positives
    3. Table cell: "exergy" row with percentage
    4. Broad fallback (original regex, last resort)
    
    Returns float (percentage) or None if not found.
    """
    text = output.lower()
    
    # --- Strategy 1: JSON block (unchanged) ---
    json_match = re.search(r'```json\s*[\{\[].+?[\}\]]\s*```', output, re.DOTALL)
    if json_match:
        try:
            clean = json_match.group().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(clean)
            if isinstance(parsed, dict):
                eff = parsed.get("efficiency_pct")
                if eff is not None:
                    return float(eff)
            elif isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict) and "efficiency_pct" in item:
                        return float(item["efficiency_pct"])
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    
    # --- Strategy 2: Line-level search (NEW) ---
    # Split into lines, find lines that explicitly say "exergy efficiency" with a number
    # Exclude lines about other efficiency types
    EXCLUDE_KEYWORDS = [
        "isentropic", "first-law", "first law", "thermal efficiency",
        "mechanical", "carnot", "motor efficiency", "hydraulic",
        "generator", "pump efficiency", "volumetric", "cop",
    ]
    
    EXERGY_PATTERNS = [
        # "exergy efficiency = 42.5%" or "exergy efficiency: 42.5%"
        r'exergy\s*(?:\(second[- ]law\))?\s*efficiency\s*[=:≈]\s*(\d+\.?\d*)\s*%',
        # "second-law efficiency = 42.5%" or "second law efficiency: 42.5%"
        r'second[- ]law\s*efficiency\s*[=:≈]\s*(\d+\.?\d*)\s*%',
        # "ε = 42.5%" or "ψ = 42.5%" (exergy efficiency symbols)
        r'[εψ]\s*[=:≈]\s*(\d+\.?\d*)\s*%',
        # "η_ex = 42.5%" or "η_II = 42.5%"
        r'η[_]?\s*(?:ex|ii|exergy|2nd)\s*[=:≈]\s*(\d+\.?\d*)\s*%',
        # "exergetic efficiency = 42.5%"
        r'exergetic\s*efficiency\s*[=:≈]\s*(\d+\.?\d*)\s*%',
    ]
    
    for line in text.split('\n'):
        # Skip lines about other efficiency types
        if any(kw in line for kw in EXCLUDE_KEYWORDS):
            continue
        
        for pattern in EXERGY_PATTERNS:
            m = re.search(pattern, line)
            if m:
                val = float(m.group(1))
                # Sanity: efficiency must be 0-100%
                if 0 < val <= 100:
                    return val
    
    # --- Strategy 3: Table cell extraction ---
    # Look for markdown table rows with "exergy" and a percentage
    table_pattern = r'\|[^|]*exerg[^|]*\|[^|]*?(\d+\.?\d*)\s*%'
    for m in re.finditer(table_pattern, text):
        val = float(m.group(1))
        if 0 < val <= 100:
            return val
    
    # --- Strategy 4: Broad fallback (original, but with >100% filter) ---
    m = re.search(r'(?:exergy|second.law)\s*efficiency.*?(\d+\.?\d*)\s*%', text)
    if m:
        val = float(m.group(1))
        if 0 < val <= 100:
            return val
    
    return None


def check_structure(output: str, expected: dict) -> dict:
    """Run structural and physics checks on model output."""
    checks = {}
    text = output.lower()

    # --- Universal structural checks ---
    if expected.get("has_dead_state"):
        checks["dead_state"] = any(x in text for x in [
            "dead state", "t₀", "t0", "298.15", "25°c", "reference state"
        ])

    if expected.get("has_summary_table"):
        checks["summary_table"] = ("|" in output and "---" in output) or \
                                   ("summary" in text and "|" in output)

    if expected.get("has_json_block"):
        json_match = re.search(r'```json\s*[\{\[].+?[\}\]]\s*```', output, re.DOTALL)
        checks["json_block"] = json_match is not None

    if expected.get("has_recommendations"):
        checks["recommendations"] = any(x in text for x in [
            "recommend", "suggestion", "improvement", "action", "measure"
        ])

    # --- Physics checks ---
    if "efficiency_range" in expected:
        lo, hi = expected["efficiency_range"]
        eff = _extract_exergy_efficiency(output)
        if eff is not None:
            checks["efficiency_physical"] = lo <= eff <= hi
            checks["efficiency_value"] = eff
        else:
            checks["efficiency_physical"] = None

    if expected.get("has_T2s_calc"):
        checks["T2s_mentioned"] = any(x in text for x in [
            "t₂s", "t2s", "isentropic temperature", "isentropic discharge",
            "h₂s", "h2s", "isentropic enthalpy", "isentropic outlet"
        ])

    if expected.get("has_steam_tables"):
        checks["steam_tables"] = any(x in text for x in [
            "steam table", "enthalpy", "h₁", "h1", "h₂", "h2", "kj/kg"
        ])

    if expected.get("has_energy_balance"):
        checks["energy_balance"] = any(x in text for x in [
            "energy balance", "q_hot", "q_cold", "heat duty", "q ="
        ])

    if expected.get("has_waste_streams"):
        checks["waste_streams"] = any(x in text for x in [
            "flue gas", "stack", "radiation", "waste", "exhaust"
        ])

    # --- Exergoeconomic checks ---
    if expected.get("has_crf_calc"):
        has_crf_mention = any(x in text for x in ["crf", "capital recovery", "annuity"])
        has_crf_value = bool(re.search(r'crf\s*=\s*[\d.]+', text))
        checks["crf_calc"] = has_crf_mention
        checks["crf_value"] = has_crf_value
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
        has_grade_value = bool(re.search(r'grade\s*=\s*[\d.]+', text))
        has_grade_letter = any(x in text for x in ["grade a", "grade b", "grade c", "grade d", "grade e", "grade f"])
        checks["grade"] = has_grade_value or has_grade_letter
    if expected.get("has_mechanism_decomposition"):
        has_mechanism_names = any(x in text for x in ["heat transfer", "friction", "pressure drop", "mixing"])
        has_mechanism_values = bool(re.search(r's_gen.*?=\s*[\d.]+\s*kw/k', text))
        checks["mechanism_decomp"] = has_mechanism_names
        checks["mechanism_values"] = has_mechanism_values

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
        checks["avoidable_ratio"] = any(x in text for x in [
            "avoidable ratio", "avoidable fraction", "avoidable share",
            "avoidable percentage", "avoidable portion",
            "avoidable/total", "avoidable/unavoidable",
            "ar =", "ar=",
            "improvement potential", "improvement margin",
            "reduction potential", "savings potential",
            "ėd,av/ėd", "ed,av/ed", "ex_d,av/ex_d",
            "avoidable exergy destruction ratio",
            "% avoidable", "% of total",
        ])

    return checks


# ============================================================
# OLLAMA API RUNNER (supports per-request temperature)
# ============================================================

def run_ollama_api(model: str, prompt: str, temperature: float = 0.7,
                   timeout: int = 900, host: str = "http://localhost:11434") -> tuple:
    """Run model via ollama HTTP API. Returns (output, elapsed_seconds)."""
    url = f"{host}/api/generate"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": 8192,
            "num_predict": 4096,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - start
            return data.get("response", ""), elapsed
    except urllib.error.URLError as e:
        elapsed = time.time() - start
        return f"[ERROR: {e}]", elapsed
    except TimeoutError:
        elapsed = time.time() - start
        return f"[TIMEOUT after {timeout}s]", elapsed


# ============================================================
# BENCHMARK RUNNER
# ============================================================

def run_benchmark(
    model: str = "entropy-hunter-v02",
    test_ids: list = None,
    category: str = None,
    quick: bool = False,
    runs: int = 1,
    temperature: float = 0.7,
    exclude_checks: list = None,
    output_dir: str = None,
    host: str = "http://localhost:11434",
) -> list:
    """Run benchmark tests. Returns list of BenchmarkResult."""

    # Select tests
    if quick:
        tests = [t for t in TEST_CASES if t["id"] in QUICK_TESTS]
    elif test_ids:
        tests = [t for t in TEST_CASES if t["id"] in test_ids]
    elif category:
        tests = [t for t in TEST_CASES if t["category"] == category]
    else:
        tests = TEST_CASES

    if not exclude_checks:
        exclude_checks = []

    out_dir = Path(output_dir) if output_dir else Path("eval/benchmark")
    out_dir.mkdir(parents=True, exist_ok=True)

    total_inferences = len(tests) * runs
    print(f"\n{'='*60}")
    print(f"🧪 EntropyHunter Benchmark v0.3")
    print(f"{'='*60}")
    print(f"   Model: {model}")
    print(f"   Tests: {len(tests)}")
    print(f"   Runs per test: {runs}")
    print(f"   Temperature: {temperature}")
    print(f"   Total inferences: {total_inferences}")
    print(f"   Excluded checks: {exclude_checks or 'none'}")
    print(f"   Output: {out_dir}")
    print()

    all_results = []

    for i, test in enumerate(tests):
        test_id = test["id"]
        for run in range(1, runs + 1):
            run_label = f"run {run}/{runs}" if runs > 1 else ""
            print(f"[{len(all_results)+1}/{total_inferences}] {test_id} {run_label}...", end="", flush=True)

            output, elapsed = run_ollama_api(model, test["prompt"],
                                              temperature=temperature, host=host)

            checks = check_structure(output, test["expected"])

            # Apply exclusions
            scored_checks = {k: v for k, v in checks.items() if k not in exclude_checks}

            passed = sum(1 for v in scored_checks.values() if v is True)
            total = sum(1 for v in scored_checks.values() if v is True or v is False)

            result = BenchmarkResult(
                test_id=test_id,
                category=test["category"],
                equipment=test["equipment"],
                difficulty=test["difficulty"],
                model=model,
                run_number=run,
                temperature=temperature,
                passed_checks=passed,
                total_checks=total,
                checks=checks,  # store ALL checks (including excluded) for analysis
                response_time_s=round(elapsed, 1),
                response_length=len(output),
                output_preview=output[:200],
            )
            all_results.append(result)

            pct = f"{passed}/{total}" if total > 0 else "N/A"
            print(f" {pct} checks | {elapsed:.0f}s | {len(output):,} chars")

            # Save individual response
            suffix = f"_run{run}" if runs > 1 else ""
            resp_path = out_dir / f"{test_id}_{model.replace(':', '_')}{suffix}.md"
            with open(resp_path, "w") as f:
                f.write(f"# {test_id}\n")
                f.write(f"Model: {model} | Run: {run} | Temp: {temperature}\n")
                f.write(f"Time: {elapsed:.1f}s | Checks: {pct}\n\n")
                f.write(output)

    return all_results


# ============================================================
# STATISTICAL ANALYSIS
# ============================================================

def compute_stats(values: list) -> dict:
    """Compute mean, std, min, max for a list of values."""
    if not values:
        return {"mean": 0, "std": 0, "min": 0, "max": 0, "n": 0}
    n = len(values)
    mean = sum(values) / n
    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        std = math.sqrt(variance)
    else:
        std = 0
    return {
        "mean": round(mean, 2),
        "std": round(std, 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
        "n": n,
    }


def print_summary(results: list, model: str, runs: int = 1, exclude_checks: list = None):
    """Print benchmark summary with statistics."""
    if not exclude_checks:
        exclude_checks = []

    print(f"\n{'='*70}")
    print(f"📊 Benchmark Results: {model}")
    print(f"{'='*70}\n")

    # Group by test_id
    test_groups = {}
    for r in results:
        if r.test_id not in test_groups:
            test_groups[r.test_id] = []
        test_groups[r.test_id].append(r)

    # Per-test results
    if runs > 1:
        print(f"{'Test ID':<30s} {'Category':<22s} {'Mean Score':>12s} {'Std':>6s} {'Time':>8s}")
    else:
        print(f"{'Test ID':<30s} {'Category':<22s} {'Score':>12s} {'Time':>8s}")
    print("-" * 80)

    total_passed = 0
    total_checks = 0

    for test_id in dict.fromkeys(r.test_id for r in results):  # preserve order
        group = test_groups[test_id]
        category = group[0].category

        if runs > 1:
            scores = [r.passed_checks / r.total_checks * 100 if r.total_checks > 0 else 0 for r in group]
            times = [r.response_time_s for r in group]
            s = compute_stats(scores)
            t = compute_stats(times)
            print(f"{test_id:<30s} {category:<22s} {s['mean']:>5.1f}%±{s['std']:<4.1f}  {t['mean']:>6.0f}s")
        else:
            r = group[0]
            pct = r.passed_checks / r.total_checks * 100 if r.total_checks > 0 else 0
            print(f"{test_id:<30s} {category:<22s} {r.passed_checks}/{r.total_checks} ({pct:.0f}%) {r.response_time_s:>6.0f}s")

        for r in group:
            total_passed += r.passed_checks
            total_checks += r.total_checks

    # Category scores
    print(f"\n{'='*70}")
    print(f"📈 Scores by Category")
    print(f"{'='*70}")

    categories = {}
    for r in results:
        cat = r.category
        if cat not in categories:
            categories[cat] = []
        score = r.passed_checks / r.total_checks * 100 if r.total_checks > 0 else 0
        categories[cat].append(score)

    for cat in sorted(categories.keys()):
        scores = categories[cat]
        s = compute_stats(scores)
        bar = "█" * int(s["mean"] / 5) + "░" * (20 - int(s["mean"] / 5))
        if runs > 1:
            print(f"  {cat:<25s} {bar} {s['mean']:>5.1f}% ± {s['std']:.1f}%  (n={s['n']})")
        else:
            print(f"  {cat:<25s} {bar} {s['mean']:>5.1f}%  (n={s['n']})")

    # Check-level breakdown
    print(f"\n{'='*70}")
    print(f"🔍 Check-Level Pass Rates (excluding: {exclude_checks or 'none'})")
    print(f"{'='*70}")

    check_stats = {}
    for r in results:
        for check_name, value in r.checks.items():
            if isinstance(value, bool):
                if check_name not in check_stats:
                    check_stats[check_name] = {"passed": 0, "total": 0}
                check_stats[check_name]["total"] += 1
                if value:
                    check_stats[check_name]["passed"] += 1

    for name, stats in sorted(check_stats.items(), key=lambda x: x[1]["passed"]/max(x[1]["total"], 1)):
        rate = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        excluded_mark = " [EXCLUDED]" if name in exclude_checks else ""
        icon = "✅" if rate >= 80 else "⚠️" if rate >= 50 else "❌"
        print(f"  {icon} {name:<30s} {stats['passed']}/{stats['total']} ({rate:.0f}%){excluded_mark}")

    # Overall score
    overall = total_passed / total_checks * 100 if total_checks > 0 else 0
    print(f"\n{'='*70}")
    grade = "A" if overall >= 90 else "B" if overall >= 75 else "C" if overall >= 60 else "D" if overall >= 40 else "F"
    print(f"🏆 Overall Score: {overall:.1f}% (Grade: {grade})")
    print(f"   {total_passed}/{total_checks} checks passed across {len(results)} inferences")

    if runs > 1:
        per_run_scores = []
        for run_num in range(1, runs + 1):
            run_results = [r for r in results if r.run_number == run_num]
            rp = sum(r.passed_checks for r in run_results)
            rc = sum(r.total_checks for r in run_results)
            per_run_scores.append(rp / rc * 100 if rc > 0 else 0)
        s = compute_stats(per_run_scores)
        print(f"   Per-run scores: {s['mean']:.1f}% ± {s['std']:.1f}% (range: {s['min']:.1f}–{s['max']:.1f}%)")

    avg_time = sum(r.response_time_s for r in results) / len(results) if results else 0
    print(f"   Average response time: {avg_time:.1f}s")
    print(f"{'='*70}\n")

    return overall


def save_results(results: list, model: str, temperature: float = 0.7,
                 runs: int = 1, exclude_checks: list = None, output_dir: str = None):
    """Save benchmark results to JSON."""
    out_dir = Path(output_dir) if output_dir else Path("eval/benchmark")
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_str = f"_t{temperature:.1f}".replace(".", "")
    runs_str = f"_x{runs}" if runs > 1 else ""
    filename = f"results_{model.replace(':', '_')}{temp_str}{runs_str}_{timestamp}.json"
    results_path = out_dir / filename

    data = {
        "model": model,
        "timestamp": timestamp,
        "temperature": temperature,
        "runs_per_test": runs,
        "num_tests": len(set(r.test_id for r in results)),
        "num_inferences": len(results),
        "excluded_checks": exclude_checks or [],
        "results": [
            {
                "test_id": r.test_id,
                "category": r.category,
                "equipment": r.equipment,
                "difficulty": r.difficulty,
                "run_number": r.run_number,
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
    return results_path


# ============================================================
# TEMPERATURE SWEEP
# ============================================================

def run_temperature_sweep(model: str, temperatures: list = None,
                          runs: int = 3, quick: bool = True,
                          exclude_checks: list = None,
                          output_dir: str = None,
                          host: str = "http://localhost:11434"):
    """Run benchmark at multiple temperatures to find optimal setting."""
    if temperatures is None:
        temperatures = [0.1, 0.3, 0.5, 0.7]

    print(f"\n{'#'*70}")
    print(f"# Temperature Sweep: {model}")
    print(f"# Temperatures: {temperatures}")
    print(f"# Runs per test per temp: {runs}")
    print(f"{'#'*70}")

    all_sweep_results = {}

    for temp in temperatures:
        print(f"\n{'='*70}")
        print(f"🌡️  Temperature: {temp}")
        print(f"{'='*70}")

        results = run_benchmark(
            model=model,
            quick=quick,
            runs=runs,
            temperature=temp,
            exclude_checks=exclude_checks,
            output_dir=output_dir,
            host=host,
        )
        all_sweep_results[temp] = results
        save_results(results, model, temperature=temp, runs=runs,
                     exclude_checks=exclude_checks, output_dir=output_dir)

    # Sweep summary
    print(f"\n{'='*70}")
    print(f"🌡️  Temperature Sweep Summary: {model}")
    print(f"{'='*70}\n")

    print(f"{'Temp':>6s} {'Score':>10s} {'Std':>8s} {'Avg Time':>10s}")
    print("-" * 40)

    best_temp = None
    best_score = -1

    for temp in temperatures:
        results = all_sweep_results[temp]
        tp = sum(r.passed_checks for r in results)
        tc = sum(r.total_checks for r in results)
        overall = tp / tc * 100 if tc > 0 else 0

        # Per-run variance
        per_run_scores = []
        for run_num in range(1, runs + 1):
            run_results = [r for r in results if r.run_number == run_num]
            rp = sum(r.passed_checks for r in run_results)
            rc = sum(r.total_checks for r in run_results)
            per_run_scores.append(rp / rc * 100 if rc > 0 else 0)
        s = compute_stats(per_run_scores)

        avg_time = sum(r.response_time_s for r in results) / len(results)

        icon = "🏆" if overall > best_score else "  "
        if overall > best_score:
            best_score = overall
            best_temp = temp

        print(f"{icon} {temp:>4.1f}  {s['mean']:>6.1f}% ±{s['std']:>5.1f}  {avg_time:>8.1f}s")

    print(f"\n✅ Optimal temperature: {best_temp} ({best_score:.1f}%)")

    # Per-check sweep breakdown (which checks benefit from lower temp?)
    print(f"\n{'='*70}")
    print(f"🔍 Check Pass Rate by Temperature")
    print(f"{'='*70}\n")

    all_check_names = set()
    for temp_results in all_sweep_results.values():
        for r in temp_results:
            for k, v in r.checks.items():
                if isinstance(v, bool):
                    all_check_names.add(k)

    header = f"{'Check':<25s}"
    for temp in temperatures:
        header += f" {temp:>6.1f}"
    print(header)
    print("-" * (25 + 7 * len(temperatures)))

    for check_name in sorted(all_check_names):
        row = f"{check_name:<25s}"
        for temp in temperatures:
            results = all_sweep_results[temp]
            passed = sum(1 for r in results for k, v in r.checks.items()
                        if k == check_name and v is True)
            total = sum(1 for r in results for k, v in r.checks.items()
                       if k == check_name and isinstance(v, bool))
            rate = passed / total * 100 if total > 0 else 0
            row += f" {rate:>5.0f}%"
        print(row)

    return all_sweep_results


# ============================================================
# COMPARISON MODE
# ============================================================

def run_comparison(models: list, runs: int = 1, temperature: float = 0.7,
                   quick: bool = False, exclude_checks: list = None,
                   output_dir: str = None, host: str = "http://localhost:11434"):
    """Run benchmark on multiple models and compare."""
    all_results = {}

    for model in models:
        print(f"\n{'#'*70}")
        print(f"# Running: {model}")
        print(f"{'#'*70}")
        results = run_benchmark(
            model=model, quick=quick, runs=runs,
            temperature=temperature, exclude_checks=exclude_checks,
            output_dir=output_dir, host=host,
        )
        all_results[model] = results
        save_results(results, model, temperature=temperature, runs=runs,
                     exclude_checks=exclude_checks, output_dir=output_dir)

    # Comparison table
    print(f"\n{'='*70}")
    print(f"📊 Model Comparison (temp={temperature}, runs={runs})")
    print(f"{'='*70}\n")

    header = f"{'Test ID':<30s}"
    for model in models:
        short = model[:15]
        header += f" {short:>15s}"
    print(header)
    print("-" * (30 + 16 * len(models)))

    test_ids = list(dict.fromkeys(r.test_id for r in all_results[models[0]]))
    for tid in test_ids:
        row = f"{tid:<30s}"
        for model in models:
            group = [r for r in all_results[model] if r.test_id == tid]
            if group:
                scores = [r.passed_checks / r.total_checks * 100 if r.total_checks > 0 else 0 for r in group]
                s = compute_stats(scores)
                if runs > 1:
                    row += f" {s['mean']:>5.1f}±{s['std']:<5.1f}"
                else:
                    row += f" {group[0].passed_checks}/{group[0].total_checks:>10s}"
            else:
                row += f" {'N/A':>15s}"
        print(row)

    print()
    for model in models:
        results = all_results[model]
        tp = sum(r.passed_checks for r in results)
        tc = sum(r.total_checks for r in results)
        pct = tp / tc * 100 if tc > 0 else 0
        print(f"  {model:<25s} {pct:.1f}% ({tp}/{tc})")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="EntropyHunter Benchmark v0.3 — Phase A Comprehensive Evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full benchmark, 3 runs per test
  python benchmark_v03.py -m entropy-hunter-v02 --runs 3

  # Temperature sweep (quick tests × 4 temps × 3 runs)
  python benchmark_v03.py -m entropy-hunter-v02 --sweep --runs 3

  # Specific category deep-dive
  python benchmark_v03.py -m entropy-hunter-v02 --category entropy_generation --runs 5

  # Compare two models, exclude json_block
  python benchmark_v03.py --compare entropy-hunter-v02 qwen2.5:7b --runs 3 --exclude-checks json_block
        """,
    )
    parser.add_argument("--model", "-m", type=str, default="entropy-hunter-v02")
    parser.add_argument("--compare", "-c", nargs="+", default=None)
    parser.add_argument("--quick", "-q", action="store_true",
                        help="Run only original 10 tests")
    parser.add_argument("--runs", "-r", type=int, default=1,
                        help="Number of runs per test (default: 1)")
    parser.add_argument("--temperature", "-t", type=float, default=0.7)
    parser.add_argument("--sweep", action="store_true",
                        help="Temperature sweep: 0.1, 0.3, 0.5, 0.7")
    parser.add_argument("--sweep-temps", nargs="+", type=float, default=None,
                        help="Custom temperatures for sweep")
    parser.add_argument("--category", type=str, default=None,
                        help="Run only tests in this category")
    parser.add_argument("--test", nargs="+", default=None,
                        help="Run specific test IDs")
    parser.add_argument("--exclude-checks", nargs="+", default=None,
                        help="Exclude these checks from scoring (e.g., json_block)")
    parser.add_argument("--output-dir", "-o", type=str, default=None)
    parser.add_argument("--host", type=str, default="http://localhost:11434",
                        help="Ollama API host")

    args = parser.parse_args()

    if args.sweep:
        temps = args.sweep_temps or [0.1, 0.3, 0.5, 0.7]
        run_temperature_sweep(
            model=args.model,
            temperatures=temps,
            runs=args.runs,
            quick=args.quick,
            exclude_checks=args.exclude_checks,
            output_dir=args.output_dir,
            host=args.host,
        )
    elif args.compare:
        run_comparison(
            models=args.compare,
            runs=args.runs,
            temperature=args.temperature,
            quick=args.quick,
            exclude_checks=args.exclude_checks,
            output_dir=args.output_dir,
            host=args.host,
        )
    else:
        results = run_benchmark(
            model=args.model,
            test_ids=args.test,
            category=args.category,
            quick=args.quick,
            runs=args.runs,
            temperature=args.temperature,
            exclude_checks=args.exclude_checks,
            output_dir=args.output_dir,
            host=args.host,
        )
        overall = print_summary(results, args.model, runs=args.runs,
                                exclude_checks=args.exclude_checks)
        save_results(results, args.model, temperature=args.temperature,
                     runs=args.runs, exclude_checks=args.exclude_checks,
                     output_dir=args.output_dir)
