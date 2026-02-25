"""
EntropyHunter — User Prompt Templates (v2 — Physically Consistent)

CHANGE LOG:
- v2: Uses consistent_params.py for physically valid parameter sets
- v1: Independent randomization caused impossible scenarios (43 kW + 19.9 m³/min at 10 bar)

Each template function takes parameters and returns an Alpaca-format dict.
Parameter generation ensures thermodynamic feasibility BEFORE the teacher model sees them.
"""

import random
import sys
from pathlib import Path
from typing import Optional

# Add datagen to path for consistent_params import
sys.path.insert(0, str(Path(__file__).parent.parent))

from consistent_params import (
    consistent_compressor_params,
    consistent_boiler_params,
    consistent_heat_exchanger_params,
    consistent_chiller_params,
    consistent_pump_params,
    consistent_steam_turbine_params,
    consistent_dryer_params,
)


# ============================================================
# PROMPT TEMPLATES
# ============================================================

def template_basic_compressor(params: dict) -> dict:
    subtype_names = {
        "screw": "screw", "piston": "reciprocating piston",
        "scroll": "scroll", "centrifugal": "centrifugal",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])

    prompt = f"""Perform a complete exergy analysis for a {name} compressor.

Operating conditions:
- Electrical power input: {params['power_kW']} kW
- Air inlet temperature: {params['inlet_temp_C']}°C
- Inlet pressure: 1.013 bar (atmospheric)
- Discharge pressure: {params['discharge_pressure_bar']} bar
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- Volume flow rate (FAD at inlet conditions): {params['flow_rate_m3_min']} m³/min
- Operating mode: {params['operating_mode']}

Note: All parameters are thermodynamically consistent. The electrical power accounts for isentropic compression work, motor losses, and heat rejection via oil cooler/aftercooler.

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "compressor",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
            "derived_checks": params.get("_derived", {}),
        }
    }


def template_basic_boiler(params: dict) -> dict:
    subtype_names = {
        "steam_firetube": "fire-tube steam", "steam_watertube": "water-tube steam",
        "hotwater": "hot water", "condensing": "condensing",
        "waste_heat": "waste heat recovery", "biomass": "biomass-fired",
    }
    fuel_names = {
        "natural_gas": "natural gas", "fuel_oil": "heavy fuel oil",
        "lpg": "LPG (propane)", "biomass_wood": "wood chips",
        "biomass_pellet": "wood pellets",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])
    fuel = fuel_names.get(params["fuel_type"], params["fuel_type"])

    prompt = f"""Perform a complete exergy analysis for a {name} boiler.

Operating conditions:
- Thermal capacity: {params['thermal_capacity_kW']} kW
- Fuel: {fuel}
- Steam/hot water operating pressure: {params['operating_pressure_bar']} bar
- Stack (flue gas exit) temperature: {params['stack_temperature_C']}°C
- Feedwater inlet temperature: {params['feedwater_temperature_C']}°C
- Thermal (first-law) efficiency: {params['thermal_efficiency_pct']}%
- Operating mode: {params['operating_mode']}

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "boiler",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
        }
    }


def template_basic_heat_exchanger(params: dict) -> dict:
    subtype_names = {
        "shell_tube": "shell and tube", "plate": "plate",
        "economizer": "economizer", "recuperator": "recuperator",
        "air_cooled": "air-cooled", "finned_tube": "finned tube",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])

    prompt = f"""Perform a complete exergy analysis for a {name} heat exchanger.

Operating conditions:
- Hot side: {params['fluid_hot']}, inlet {params['hot_inlet_temp_C']}°C → outlet {params['hot_outlet_temp_C']}°C, flow rate {params['hot_flow_kg_s']} kg/s
- Cold side: {params['fluid_cold']}, inlet {params['cold_inlet_temp_C']}°C → outlet {params['cold_outlet_temp_C']}°C, flow rate {params['cold_flow_kg_s']} kg/s
- Pressure drop (hot side): 0.3 bar
- Pressure drop (cold side): 0.2 bar
- Operating mode: {params['operating_mode']}

Note: Flow rates are energy-balance consistent.

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "heat_exchanger",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
            "derived_checks": params.get("_derived", {}),
        }
    }


def template_basic_chiller(params: dict) -> dict:
    subtype_names = {
        "screw": "screw", "centrifugal": "centrifugal",
        "absorption": "absorption (LiBr/H₂O)",
        "air_cooled": "air-cooled", "water_cooled": "water-cooled",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])

    prompt = f"""Perform a complete exergy analysis for a {name} chiller.

Operating conditions:
- Cooling capacity: {params['cooling_capacity_kW']} kW
- Evaporator temperature: {params['evaporator_temp_C']}°C
- Condenser temperature: {params['condenser_temp_C']}°C
- Coefficient of Performance (COP): {params['cop']}
- Refrigerant: {params['refrigerant']}
- Operating mode: {params['operating_mode']}

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "chiller",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
            "derived_checks": params.get("_derived", {}),
        }
    }


def template_basic_pump(params: dict) -> dict:
    subtype_names = {
        "centrifugal": "centrifugal", "positive_displacement": "positive displacement",
        "submersible": "submersible", "booster": "booster", "vacuum": "vacuum",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])

    prompt = f"""Perform a complete exergy analysis for a {name} pump.

Operating conditions:
- Volume flow rate: {params['flow_rate_m3_h']} m³/h
- Total head: {params['head_m']} m
- Motor electrical power: {params['motor_power_kW']} kW
- Pump hydraulic efficiency: {params['pump_efficiency_pct']}%
- Motor efficiency: {params['motor_efficiency_pct']}%
- Fluid: water at {params['fluid_temp_C']}°C
- Operating mode: {params['operating_mode']}

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "pump",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
            "derived_checks": params.get("_derived", {}),
        }
    }


def template_basic_steam_turbine(params: dict) -> dict:
    subtype_names = {
        "back_pressure": "back-pressure", "condensing": "condensing",
        "extraction": "extraction", "orc": "ORC",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])

    prompt = f"""Perform a complete exergy analysis for a {name} steam turbine.

Operating conditions:
- Inlet steam pressure: {params['inlet_pressure_bar']} bar
- Inlet steam temperature: {params['inlet_temp_C']}°C (superheated)
- Outlet pressure: {params['outlet_pressure_bar']} bar
- Steam mass flow rate: {params['mass_flow_kg_s']} kg/s
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- Generator efficiency: {params['generator_efficiency_pct']}%
- Operating mode: {params['operating_mode']}

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "steam_turbine",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
        }
    }


def template_basic_dryer(params: dict) -> dict:
    subtype_names = {
        "convective": "convective hot air", "rotary": "rotary drum",
        "fluidized_bed": "fluidized bed", "spray": "spray",
        "belt": "belt (conveyor)", "heat_pump": "heat pump assisted",
    }
    name = subtype_names.get(params["subtype"], params["subtype"])

    prompt = f"""Perform a complete exergy analysis for a {name} dryer.

Operating conditions:
- Drying air inlet temperature: {params['inlet_air_temp_C']}°C
- Drying air outlet temperature: {params['outlet_air_temp_C']}°C
- Product mass flow rate: {params['product_flow_kg_h']} kg/h
- Initial moisture content: {params['initial_moisture_pct']}% (wet basis)
- Final moisture content: {params['final_moisture_pct']}% (wet basis)
- Thermal energy input: {params['thermal_input_kW']} kW
- Operating mode: {params['operating_mode']}

Provide the analysis with step-by-step calculations, ending with a summary table and recommendations."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": "dryer",
            "subtype": params["subtype"],
            "analysis_type": "basic_exergy",
            "operating_mode": params["operating_mode"],
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
            "derived_checks": params.get("_derived", {}),
        }
    }


# ============================================================
# TEMPLATE MAP & GENERATORS
# ============================================================

TEMPLATE_MAP = {
    "compressor":     (template_basic_compressor, consistent_compressor_params),
    "boiler":         (template_basic_boiler, consistent_boiler_params),
    "heat_exchanger": (template_basic_heat_exchanger, consistent_heat_exchanger_params),
    "chiller":        (template_basic_chiller, consistent_chiller_params),
    "pump":           (template_basic_pump, consistent_pump_params),
    "steam_turbine":  (template_basic_steam_turbine, consistent_steam_turbine_params),
    "dryer":          (template_basic_dryer, consistent_dryer_params),
}


def generate_prompt(equipment_type: str, subtype: Optional[str] = None) -> dict:
    """Generate a single training prompt with physically consistent parameters."""
    template_fn, params_fn = TEMPLATE_MAP[equipment_type]
    params = params_fn(subtype)
    return template_fn(params)


def generate_batch(n: int, equipment_type: Optional[str] = None) -> list[dict]:
    """Generate a batch of n prompts."""
    prompts = []
    types = [equipment_type] if equipment_type else list(TEMPLATE_MAP.keys())
    for _ in range(n):
        eq_type = random.choice(types)
        prompts.append(generate_prompt(eq_type))
    return prompts


if __name__ == "__main__":
    for eq_type in TEMPLATE_MAP:
        p = generate_prompt(eq_type)
        meta = p["metadata"]
        derived = meta.get("derived_checks", {})
        print(f"[{meta['equipment_type']}/{meta['subtype']}] {meta['operating_mode']}")
        if "spc_kW_per_m3_min" in derived:
            print(f"  SPC: {derived['spc_kW_per_m3_min']} kW/(m³/min)")
        if "cop_carnot" in derived:
            print(f"  COP: {meta['parameters']['cop']} / Carnot: {derived['cop_carnot']}")
        if "wire_to_water_pct" in derived:
            print(f"  Wire-to-water: {derived['wire_to_water_pct']}%")
        print(f"  {p['instruction'][:120]}...")
        print()
