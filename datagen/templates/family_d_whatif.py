"""
EntropyHunter — Family D: What-if Scenario Comparison Templates

Generates baseline operating conditions + a realistic modification scenario.
Teacher model compares both and calculates savings.
"""

import random
import copy
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from consistent_params import (
    consistent_compressor_params, consistent_boiler_params,
    consistent_heat_exchanger_params, consistent_chiller_params,
    consistent_pump_params, consistent_steam_turbine_params,
    consistent_dryer_params,
)


# ============================================================
# SCENARIO GENERATORS — create realistic modifications
# ============================================================

SCENARIOS = {
    "compressor": [
        {
            "name": "Isentropic efficiency upgrade",
            "modify": lambda p: _modify(p, "isentropic_efficiency_pct", +random.choice([5, 8, 10, 12])),
            "description": "upgrading to a higher-efficiency compressor element",
        },
        {
            "name": "VSD installation (part-load improvement)",
            "modify": lambda p: _modify_vsd_compressor(p),
            "description": "installing a variable speed drive for part-load optimization",
        },
        {
            "name": "Discharge pressure reduction",
            "modify": lambda p: _modify(p, "discharge_pressure_bar", -random.choice([1, 2]),
                                        min_val=4),
            "description": "reducing system pressure demand through leak reduction and piping optimization",
        },
        {
            "name": "Inlet air cooling",
            "modify": lambda p: _modify(p, "inlet_temp_C", -random.choice([5, 10, 15]),
                                        min_val=5),
            "description": "installing inlet air precooling to reduce compression work",
        },
    ],
    "boiler": [
        {
            "name": "Economizer installation (lower stack temp)",
            "modify": lambda p: _modify(p, "stack_temperature_C", -random.choice([30, 50, 70]),
                                        min_val=80),
            "description": "installing a flue gas economizer to recover waste heat",
        },
        {
            "name": "Thermal efficiency improvement",
            "modify": lambda p: _modify(p, "thermal_efficiency_pct", +random.choice([3, 5, 7]),
                                        max_val=98),
            "description": "optimizing combustion and insulation to improve thermal efficiency",
        },
        {
            "name": "Feedwater preheating",
            "modify": lambda p: _modify(p, "feedwater_temperature_C", +random.choice([20, 30, 40]),
                                        max_val=100),
            "description": "preheating feedwater using waste heat from deaerator or blowdown",
        },
    ],
    "heat_exchanger": [
        {
            "name": "Fouling removal (restored performance)",
            "modify": lambda p: _modify_hx_defoul(p),
            "description": "cleaning heat exchanger to restore design heat transfer",
        },
        {
            "name": "Hot side temperature increase",
            "modify": lambda p: _modify(p, "hot_inlet_temp_C", +random.choice([10, 20, 30])),
            "description": "increasing hot side inlet temperature through process optimization",
        },
    ],
    "chiller": [
        {
            "name": "COP improvement (compressor upgrade)",
            "modify": lambda p: _modify_cop(p, +random.uniform(0.3, 0.8)),
            "description": "upgrading compressor for higher COP",
        },
        {
            "name": "Condenser temperature reduction",
            "modify": lambda p: _modify(p, "condenser_temp_C", -random.choice([3, 5]),
                                        min_val=25),
            "description": "installing a cooling tower upgrade to lower condenser approach temperature",
        },
    ],
    "pump": [
        {
            "name": "Pump efficiency upgrade",
            "modify": lambda p: _modify(p, "pump_efficiency_pct", +random.choice([5, 8, 10]),
                                        max_val=88),
            "description": "replacing pump with higher-efficiency model or trimming impeller",
        },
        {
            "name": "Motor efficiency upgrade (IE3→IE5)",
            "modify": lambda p: _modify(p, "motor_efficiency_pct", +random.choice([3, 4, 5]),
                                        max_val=97),
            "description": "upgrading motor from IE3 to IE5 premium efficiency class",
        },
    ],
    "steam_turbine": [
        {
            "name": "Isentropic efficiency improvement",
            "modify": lambda p: _modify(p, "isentropic_efficiency_pct", +random.choice([3, 5, 8]),
                                        max_val=92),
            "description": "blade refurbishment or upgrade to improve isentropic efficiency",
        },
        {
            "name": "Inlet steam superheat increase",
            "modify": lambda p: _modify(p, "inlet_temp_C", +random.choice([20, 30, 50]),
                                        max_val=560),
            "description": "increasing superheater capacity for higher inlet steam temperature",
        },
    ],
    "dryer": [
        {
            "name": "Inlet air temperature optimization",
            "modify": lambda p: _modify(p, "inlet_air_temp_C", +random.choice([10, 20, 30]),
                                        max_val=220),
            "description": "increasing drying air temperature for faster moisture removal",
        },
        {
            "name": "Heat recovery from exhaust air",
            "modify": lambda p: _modify(p, "thermal_input_kW",
                                        -int(p["thermal_input_kW"] * random.uniform(0.10, 0.20)),
                                        min_val=20),
            "description": "installing exhaust air heat recovery to reduce thermal input",
        },
    ],
}


def _modify(params: dict, key: str, delta, min_val=None, max_val=None) -> dict:
    """Apply a delta to a single parameter."""
    p = copy.deepcopy(params)
    p[key] = p[key] + delta
    if min_val is not None:
        p[key] = max(p[key], min_val)
    if max_val is not None:
        p[key] = min(p[key], max_val)
    return p


def _modify_vsd_compressor(params: dict) -> dict:
    """VSD: reduce power at part load (better turndown)."""
    p = copy.deepcopy(params)
    p["operating_mode"] = "part_load_75pct"
    p["power_kW"] = round(p["power_kW"] * 0.72, 1)  # VSD follows affinity law better
    p["flow_rate_m3_min"] = round(p["flow_rate_m3_min"] * 0.75, 1)
    return p


def _modify_hx_defoul(params: dict) -> dict:
    """Fouling removal: improve cold outlet temp (better heat transfer)."""
    p = copy.deepcopy(params)
    improvement = random.choice([5, 8, 10])
    p["cold_outlet_temp_C"] = min(p["cold_outlet_temp_C"] + improvement,
                                   p["hot_inlet_temp_C"] - 5)
    p["hot_outlet_temp_C"] = max(p["hot_outlet_temp_C"] - improvement,
                                  p["cold_inlet_temp_C"] + 5)
    return p


def _modify_cop(params: dict, delta: float) -> dict:
    """Increase COP within Carnot limit."""
    p = copy.deepcopy(params)
    derived = params.get("_derived", {})
    cop_carnot = derived.get("cop_carnot", 10)
    p["cop"] = round(min(p["cop"] + delta, cop_carnot * 0.60), 1)
    return p


# ============================================================
# PROMPT BUILDER
# ============================================================

def _format_params_block(equipment_type: str, params: dict) -> str:
    """Format operating conditions for a given equipment type."""
    if equipment_type == "compressor":
        return f"""- Electrical power input: {params['power_kW']} kW
- Air inlet temperature: {params['inlet_temp_C']}°C
- Discharge pressure: {params['discharge_pressure_bar']} bar
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- Volume flow rate (FAD): {params['flow_rate_m3_min']} m³/min
- Operating mode: {params['operating_mode']}"""
    elif equipment_type == "boiler":
        return f"""- Thermal capacity: {params['thermal_capacity_kW']} kW
- Fuel: {params.get('fuel_type', 'natural_gas')}
- Operating pressure: {params['operating_pressure_bar']} bar
- Stack temperature: {params['stack_temperature_C']}°C
- Feedwater temperature: {params['feedwater_temperature_C']}°C
- Thermal efficiency: {params['thermal_efficiency_pct']}%
- Operating mode: {params['operating_mode']}"""
    elif equipment_type == "heat_exchanger":
        return f"""- Hot side: {params['fluid_hot']}, inlet {params['hot_inlet_temp_C']}°C → outlet {params['hot_outlet_temp_C']}°C, flow {params['hot_flow_kg_s']} kg/s
- Cold side: {params['fluid_cold']}, inlet {params['cold_inlet_temp_C']}°C → outlet {params['cold_outlet_temp_C']}°C, flow {params['cold_flow_kg_s']} kg/s
- Operating mode: {params['operating_mode']}"""
    elif equipment_type == "chiller":
        return f"""- Cooling capacity: {params['cooling_capacity_kW']} kW
- Evaporator temperature: {params['evaporator_temp_C']}°C
- Condenser temperature: {params['condenser_temp_C']}°C
- COP: {params['cop']}
- Refrigerant: {params['refrigerant']}
- Operating mode: {params['operating_mode']}"""
    elif equipment_type == "pump":
        return f"""- Volume flow rate: {params['flow_rate_m3_h']} m³/h
- Total head: {params['head_m']} m
- Motor power: {params['motor_power_kW']} kW
- Pump efficiency: {params['pump_efficiency_pct']}%
- Motor efficiency: {params['motor_efficiency_pct']}%
- Fluid: water at {params['fluid_temp_C']}°C
- Operating mode: {params['operating_mode']}"""
    elif equipment_type == "steam_turbine":
        return f"""- Inlet pressure: {params['inlet_pressure_bar']} bar
- Inlet temperature: {params['inlet_temp_C']}°C
- Outlet pressure: {params['outlet_pressure_bar']} bar
- Mass flow rate: {params['mass_flow_kg_s']} kg/s
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- Generator efficiency: {params['generator_efficiency_pct']}%
- Operating mode: {params['operating_mode']}"""
    elif equipment_type == "dryer":
        return f"""- Air inlet temperature: {params['inlet_air_temp_C']}°C
- Air outlet temperature: {params['outlet_air_temp_C']}°C
- Product flow rate: {params['product_flow_kg_h']} kg/h
- Moisture: {params['initial_moisture_pct']}% → {params['final_moisture_pct']}%
- Thermal input: {params['thermal_input_kW']} kW
- Operating mode: {params['operating_mode']}"""
    return str(params)


EQUIPMENT_NAMES = {
    "compressor": {"screw": "screw", "piston": "reciprocating piston",
                   "scroll": "scroll", "centrifugal": "centrifugal"},
    "boiler": {"steam_firetube": "fire-tube steam", "steam_watertube": "water-tube steam",
               "condensing": "condensing", "waste_heat": "waste heat recovery", "biomass": "biomass-fired"},
    "heat_exchanger": {"shell_tube": "shell and tube", "plate": "plate",
                       "economizer": "economizer", "recuperator": "recuperator"},
    "chiller": {"screw": "screw", "centrifugal": "centrifugal",
                "absorption": "absorption", "water_cooled": "water-cooled"},
    "pump": {"centrifugal": "centrifugal", "positive_displacement": "positive displacement",
             "booster": "booster"},
    "steam_turbine": {"back_pressure": "back-pressure", "condensing": "condensing",
                      "extraction": "extraction"},
    "dryer": {"rotary": "rotary drum", "fluidized_bed": "fluidized bed",
              "spray": "spray", "belt": "belt", "convective": "convective hot air"},
}

PARAM_GENERATORS = {
    "compressor": consistent_compressor_params,
    "boiler": consistent_boiler_params,
    "heat_exchanger": consistent_heat_exchanger_params,
    "chiller": consistent_chiller_params,
    "pump": consistent_pump_params,
    "steam_turbine": consistent_steam_turbine_params,
    "dryer": consistent_dryer_params,
}


def generate_prompt(equipment_type: str, subtype: Optional[str] = None) -> dict:
    """Generate a what-if comparison prompt."""
    params_fn = PARAM_GENERATORS[equipment_type]
    baseline = params_fn(subtype)
    
    # Pick a random scenario
    scenarios = SCENARIOS.get(equipment_type, SCENARIOS["compressor"])
    scenario = random.choice(scenarios)
    
    modified = scenario["modify"](baseline)
    
    names = EQUIPMENT_NAMES.get(equipment_type, {})
    name = names.get(baseline["subtype"], baseline["subtype"])
    
    energy_price = round(random.uniform(0.06, 0.15), 3)
    annual_hours = random.choice([4000, 5000, 6000, 7500, 8000])

    prompt = f"""Perform a what-if exergy comparison for a {name} {equipment_type.replace('_', ' ')}.

**Scenario:** {scenario['name']} — {scenario['description']}

### BASELINE
{_format_params_block(equipment_type, baseline)}

### MODIFIED SCENARIO
{_format_params_block(equipment_type, modified)}

Energy cost: {energy_price} EUR/kWh
Annual operating hours: {annual_hours} h/year

Perform exergy analysis for BOTH conditions, present a comparison table (Baseline | Scenario | Delta | %), and calculate annual energy and cost savings."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": equipment_type,
            "subtype": baseline["subtype"],
            "analysis_type": "whatif_comparison",
            "operating_mode": baseline.get("operating_mode", "full_load"),
            "scenario_name": scenario["name"],
            "parameters_baseline": {k: v for k, v in baseline.items() if k != "_derived"},
            "parameters_modified": {k: v for k, v in modified.items() if k != "_derived"},
            "energy_price_eur_kwh": energy_price,
            "annual_hours": annual_hours,
        }
    }
