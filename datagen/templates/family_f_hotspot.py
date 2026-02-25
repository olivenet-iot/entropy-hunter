"""
EntropyHunter — Family F: Factory-Level Hotspot Detection Templates

Generates a realistic factory with 3-5 equipment items.
Asks teacher model to analyze all, rank by exergy destruction, identify hotspot.
"""

import random
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
# FACTORY PROFILES — realistic equipment combinations by sector
# ============================================================

FACTORY_PROFILES = {
    "food_beverage": {
        "name": "Food & Beverage Processing Plant",
        "equipment": [
            ("boiler", "steam_firetube"),
            ("heat_exchanger", "plate"),
            ("compressor", "screw"),
            ("pump", "centrifugal"),
            ("chiller", "screw"),
        ],
        "pick": (3, 5),  # pick 3-5 from the list
    },
    "chemical": {
        "name": "Chemical Processing Facility",
        "equipment": [
            ("boiler", "steam_watertube"),
            ("heat_exchanger", "shell_tube"),
            ("compressor", "centrifugal"),
            ("pump", "centrifugal"),
            ("steam_turbine", "back_pressure"),
        ],
        "pick": (3, 5),
    },
    "pharmaceutical": {
        "name": "Pharmaceutical Manufacturing Plant",
        "equipment": [
            ("boiler", "steam_firetube"),
            ("chiller", "water_cooled"),
            ("compressor", "scroll"),
            ("pump", "centrifugal"),
            ("heat_exchanger", "plate"),
        ],
        "pick": (3, 4),
    },
    "textile": {
        "name": "Textile Mill",
        "equipment": [
            ("boiler", "steam_watertube"),
            ("dryer", "belt"),
            ("heat_exchanger", "economizer"),
            ("pump", "centrifugal"),
            ("compressor", "piston"),
        ],
        "pick": (3, 5),
    },
    "commercial_building": {
        "name": "Commercial Building HVAC System",
        "equipment": [
            ("chiller", "centrifugal"),
            ("pump", "centrifugal"),
            ("heat_exchanger", "plate"),
            ("boiler", "condensing"),
            ("compressor", "scroll"),
        ],
        "pick": (3, 4),
    },
    "pulp_paper": {
        "name": "Pulp & Paper Mill",
        "equipment": [
            ("boiler", "steam_watertube"),
            ("steam_turbine", "back_pressure"),
            ("dryer", "rotary"),
            ("pump", "centrifugal"),
            ("heat_exchanger", "economizer"),
        ],
        "pick": (3, 5),
    },
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

EQUIPMENT_NAMES = {
    "compressor": {"screw": "screw compressor", "piston": "piston compressor",
                   "scroll": "scroll compressor", "centrifugal": "centrifugal compressor"},
    "boiler": {"steam_firetube": "fire-tube steam boiler", "steam_watertube": "water-tube steam boiler",
               "condensing": "condensing boiler"},
    "heat_exchanger": {"shell_tube": "shell-and-tube HX", "plate": "plate heat exchanger",
                       "economizer": "flue gas economizer"},
    "chiller": {"screw": "screw chiller", "centrifugal": "centrifugal chiller",
                "water_cooled": "water-cooled chiller"},
    "pump": {"centrifugal": "centrifugal pump"},
    "steam_turbine": {"back_pressure": "back-pressure steam turbine"},
    "dryer": {"rotary": "rotary dryer", "belt": "belt dryer"},
}


def _format_equipment_block(idx: int, eq_type: str, subtype: str, params: dict) -> str:
    """Format a single equipment's params for the factory prompt."""
    name = EQUIPMENT_NAMES.get(eq_type, {}).get(subtype, f"{subtype} {eq_type}")

    if eq_type == "compressor":
        return f"""**Equipment {idx}: {name}**
- Electrical power: {params['power_kW']} kW
- Discharge pressure: {params['discharge_pressure_bar']} bar
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- FAD: {params['flow_rate_m3_min']} m³/min"""
    elif eq_type == "boiler":
        return f"""**Equipment {idx}: {name}**
- Thermal capacity: {params['thermal_capacity_kW']} kW
- Fuel: {params.get('fuel_type', 'natural_gas')}
- Operating pressure: {params['operating_pressure_bar']} bar
- Thermal efficiency: {params['thermal_efficiency_pct']}%
- Stack temperature: {params['stack_temperature_C']}°C"""
    elif eq_type == "heat_exchanger":
        return f"""**Equipment {idx}: {name}**
- Hot side: {params['fluid_hot']}, {params['hot_inlet_temp_C']}°C → {params['hot_outlet_temp_C']}°C, {params['hot_flow_kg_s']} kg/s
- Cold side: {params['fluid_cold']}, {params['cold_inlet_temp_C']}°C → {params['cold_outlet_temp_C']}°C, {params['cold_flow_kg_s']} kg/s"""
    elif eq_type == "chiller":
        return f"""**Equipment {idx}: {name}**
- Cooling capacity: {params['cooling_capacity_kW']} kW
- Evaporator: {params['evaporator_temp_C']}°C, Condenser: {params['condenser_temp_C']}°C
- COP: {params['cop']}"""
    elif eq_type == "pump":
        return f"""**Equipment {idx}: {name}**
- Flow rate: {params['flow_rate_m3_h']} m³/h, Head: {params['head_m']} m
- Motor power: {params['motor_power_kW']} kW
- Pump efficiency: {params['pump_efficiency_pct']}%, Motor efficiency: {params['motor_efficiency_pct']}%"""
    elif eq_type == "steam_turbine":
        return f"""**Equipment {idx}: {name}**
- Inlet: {params['inlet_pressure_bar']} bar, {params['inlet_temp_C']}°C
- Outlet: {params['outlet_pressure_bar']} bar
- Mass flow: {params['mass_flow_kg_s']} kg/s
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%"""
    elif eq_type == "dryer":
        return f"""**Equipment {idx}: {name}**
- Air: {params['inlet_air_temp_C']}°C → {params['outlet_air_temp_C']}°C
- Product: {params['product_flow_kg_h']} kg/h, moisture {params['initial_moisture_pct']}% → {params['final_moisture_pct']}%
- Thermal input: {params['thermal_input_kW']} kW"""
    return f"**Equipment {idx}: {name}** — {params}"


def generate_prompt(equipment_type: Optional[str] = None, subtype: Optional[str] = None) -> dict:
    """
    Generate a factory-level hotspot detection prompt.
    equipment_type parameter is ignored (factory has mixed equipment).
    """
    # Pick a random factory profile
    sector = random.choice(list(FACTORY_PROFILES.keys()))
    profile = FACTORY_PROFILES[sector]
    
    # Pick N equipment from the profile
    lo, hi = profile["pick"]
    n = random.randint(lo, hi)
    selected = random.sample(profile["equipment"], min(n, len(profile["equipment"])))
    
    # Generate params for each
    equipment_list = []
    equipment_blocks = []
    for idx, (eq_type, eq_subtype) in enumerate(selected, 1):
        params = PARAM_GENERATORS[eq_type](eq_subtype)
        equipment_list.append({
            "equipment_type": eq_type,
            "subtype": eq_subtype,
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
        })
        equipment_blocks.append(_format_equipment_block(idx, eq_type, eq_subtype, params))

    prompt = f"""Perform a factory-level exergy hotspot analysis for a {profile['name']}.

The facility has the following {len(selected)} equipment items:

{chr(10).join(equipment_blocks)}

For each equipment:
1. Calculate exergy input, output, destruction, and efficiency
2. Calculate entropy generation rate

Then:
3. Present a ranking table: Equipment | Ex_d (kW) | η_ex (%) | N_s | Priority
4. Identify the #1 hotspot (largest exergy destruction) and #1 priority (worst efficiency)
5. Calculate total facility exergy destruction and weighted average efficiency
6. Recommend top 3 improvement actions ranked by expected exergy savings (kW)

End with summary table and overall facility assessment."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "factory",
            "subtype": sector,
            "analysis_type": "hotspot_detection",
            "operating_mode": "full_load",
            "equipment_list": equipment_list,
        }
    }
