"""
EntropyHunter — Family C: Entropy Generation Minimization (EGM) Templates

Same physical parameters as Family A.
Asks teacher model for Bejan's EGM analysis with mechanism decomposition.
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


def _egm_instruction(name: str, equipment_type: str, operating_block: str) -> str:
    return f"""Perform an Entropy Generation Minimization (EGM) analysis for a {name} {equipment_type.replace('_', ' ')}.

{operating_block}

Focus on:
1. Total entropy generation rate (Ṡ_gen) via Gouy-Stodola theorem
2. Bejan number (N_s) with grade assignment (A-F)
3. Decomposition of entropy generation by mechanism:
   - Heat transfer irreversibility (ΔT-driven)
   - Pressure drop irreversibility (friction-driven)
   - Mixing/chemical irreversibility
   Show kW/K and percentage share for each mechanism.
4. Dominant mechanism identification and physical explanation
5. Achievable Ṡ_gen reduction potential with specific measures
6. Step-by-step calculations ending with summary table and recommendations."""


def _build_template(equipment_type: str, subtype_names: dict, params: dict,
                    operating_block: str) -> dict:
    name = subtype_names.get(params["subtype"], params["subtype"])
    prompt = _egm_instruction(name, equipment_type, operating_block)
    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": equipment_type,
            "subtype": params["subtype"],
            "analysis_type": "entropy_generation",
            "operating_mode": params.get("operating_mode", "full_load"),
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
        }
    }


def template_egm_compressor(params: dict) -> dict:
    names = {"screw": "screw", "piston": "reciprocating piston",
             "scroll": "scroll", "centrifugal": "centrifugal"}
    block = f"""Operating conditions:
- Electrical power input: {params['power_kW']} kW
- Air inlet temperature: {params['inlet_temp_C']}°C
- Discharge pressure: {params['discharge_pressure_bar']} bar
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- Volume flow rate (FAD): {params['flow_rate_m3_min']} m³/min
- Operating mode: {params['operating_mode']}"""
    return _build_template("compressor", names, params, block)


def template_egm_boiler(params: dict) -> dict:
    names = {"steam_firetube": "fire-tube steam", "steam_watertube": "water-tube steam",
             "condensing": "condensing", "waste_heat": "waste heat recovery", "biomass": "biomass-fired"}
    fuel_names = {"natural_gas": "natural gas", "fuel_oil": "heavy fuel oil",
                  "lpg": "LPG", "biomass_wood": "wood chips", "biomass_pellet": "wood pellets"}
    fuel = fuel_names.get(params.get("fuel_type", ""), "")
    block = f"""Operating conditions:
- Thermal capacity: {params['thermal_capacity_kW']} kW
- Fuel: {fuel}
- Operating pressure: {params['operating_pressure_bar']} bar
- Stack temperature: {params['stack_temperature_C']}°C
- Feedwater temperature: {params['feedwater_temperature_C']}°C
- Thermal efficiency: {params['thermal_efficiency_pct']}%
- Operating mode: {params['operating_mode']}"""
    return _build_template("boiler", names, params, block)


def template_egm_heat_exchanger(params: dict) -> dict:
    names = {"shell_tube": "shell and tube", "plate": "plate",
             "economizer": "economizer", "recuperator": "recuperator"}
    block = f"""Operating conditions:
- Hot side: {params['fluid_hot']}, inlet {params['hot_inlet_temp_C']}°C → outlet {params['hot_outlet_temp_C']}°C, flow {params['hot_flow_kg_s']} kg/s
- Cold side: {params['fluid_cold']}, inlet {params['cold_inlet_temp_C']}°C → outlet {params['cold_outlet_temp_C']}°C, flow {params['cold_flow_kg_s']} kg/s
- Operating mode: {params['operating_mode']}"""
    return _build_template("heat_exchanger", names, params, block)


def template_egm_chiller(params: dict) -> dict:
    names = {"screw": "screw", "centrifugal": "centrifugal",
             "absorption": "absorption (LiBr/H₂O)", "water_cooled": "water-cooled"}
    block = f"""Operating conditions:
- Cooling capacity: {params['cooling_capacity_kW']} kW
- Evaporator temperature: {params['evaporator_temp_C']}°C
- Condenser temperature: {params['condenser_temp_C']}°C
- COP: {params['cop']}
- Refrigerant: {params['refrigerant']}
- Operating mode: {params['operating_mode']}"""
    return _build_template("chiller", names, params, block)


def template_egm_pump(params: dict) -> dict:
    names = {"centrifugal": "centrifugal", "positive_displacement": "positive displacement",
             "booster": "booster"}
    block = f"""Operating conditions:
- Volume flow rate: {params['flow_rate_m3_h']} m³/h
- Total head: {params['head_m']} m
- Motor power: {params['motor_power_kW']} kW
- Pump efficiency: {params['pump_efficiency_pct']}%
- Motor efficiency: {params['motor_efficiency_pct']}%
- Fluid: water at {params['fluid_temp_C']}°C
- Operating mode: {params['operating_mode']}"""
    return _build_template("pump", names, params, block)


def template_egm_steam_turbine(params: dict) -> dict:
    names = {"back_pressure": "back-pressure", "condensing": "condensing",
             "extraction": "extraction"}
    block = f"""Operating conditions:
- Inlet pressure: {params['inlet_pressure_bar']} bar
- Inlet temperature: {params['inlet_temp_C']}°C
- Outlet pressure: {params['outlet_pressure_bar']} bar
- Mass flow rate: {params['mass_flow_kg_s']} kg/s
- Isentropic efficiency: {params['isentropic_efficiency_pct']}%
- Generator efficiency: {params['generator_efficiency_pct']}%
- Operating mode: {params['operating_mode']}"""
    return _build_template("steam_turbine", names, params, block)


def template_egm_dryer(params: dict) -> dict:
    names = {"rotary": "rotary drum", "fluidized_bed": "fluidized bed",
             "spray": "spray", "belt": "belt", "convective": "convective hot air"}
    block = f"""Operating conditions:
- Air inlet temperature: {params['inlet_air_temp_C']}°C
- Air outlet temperature: {params['outlet_air_temp_C']}°C
- Product flow rate: {params['product_flow_kg_h']} kg/h
- Moisture: {params['initial_moisture_pct']}% → {params['final_moisture_pct']}%
- Thermal input: {params['thermal_input_kW']} kW
- Operating mode: {params['operating_mode']}"""
    return _build_template("dryer", names, params, block)


TEMPLATE_MAP_C = {
    "compressor":     (template_egm_compressor, consistent_compressor_params),
    "boiler":         (template_egm_boiler, consistent_boiler_params),
    "heat_exchanger": (template_egm_heat_exchanger, consistent_heat_exchanger_params),
    "chiller":        (template_egm_chiller, consistent_chiller_params),
    "pump":           (template_egm_pump, consistent_pump_params),
    "steam_turbine":  (template_egm_steam_turbine, consistent_steam_turbine_params),
    "dryer":          (template_egm_dryer, consistent_dryer_params),
}


def generate_prompt(equipment_type: str, subtype: Optional[str] = None) -> dict:
    template_fn, params_fn = TEMPLATE_MAP_C[equipment_type]
    params = params_fn(subtype)
    return template_fn(params)
