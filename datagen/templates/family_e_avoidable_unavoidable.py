"""
EntropyHunter — Family E: Avoidable/Unavoidable Exergy Destruction Templates

Same physical parameters + reference (best available technology) efficiencies.
Asks teacher model for detailed AV/UN and endogenous/exogenous decomposition.
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
# REFERENCE EFFICIENCIES — Best Available Technology (BAT)
# Used to define "unavoidable" destruction threshold
# ============================================================

REFERENCE_EFFICIENCIES = {
    "compressor": {
        "screw":       {"eta_is_ref": 88, "motor_ref": 97, "source": "Atlas Copco GA VSD+"},
        "piston":      {"eta_is_ref": 82, "motor_ref": 95, "source": "Bitzer high-eff reciprocating"},
        "scroll":      {"eta_is_ref": 85, "motor_ref": 96, "source": "Copeland ZR premium"},
        "centrifugal": {"eta_is_ref": 90, "motor_ref": 98, "source": "Siemens STC-GV"},
    },
    "boiler": {
        "steam_firetube":  {"thermal_eff_ref": 94, "source": "Viessmann Vitomax condensing"},
        "steam_watertube": {"thermal_eff_ref": 95, "source": "Bosch UT-HZ high-efficiency"},
        "condensing":      {"thermal_eff_ref": 99, "source": "Viessmann Vitocrossal 300"},
        "waste_heat":      {"thermal_eff_ref": 90, "source": "HRSG design optimum"},
        "biomass":         {"thermal_eff_ref": 92, "source": "KWB Multifire premium"},
    },
    "heat_exchanger": {
        "shell_tube":  {"approach_ref_C": 3, "source": "Alfa Laval Aalborg optimized"},
        "plate":       {"approach_ref_C": 2, "source": "Alfa Laval T-series gasketed"},
        "economizer":  {"approach_ref_C": 5, "source": "Cleaver-Brooks condensing economizer"},
        "recuperator": {"approach_ref_C": 8, "source": "HeatMatrix polymer recuperator"},
    },
    "chiller": {
        "screw":       {"cop_ref": 5.5, "source": "York YVWA VSD screw"},
        "centrifugal": {"cop_ref": 6.5, "source": "Carrier AquaEdge 19MV"},
        "absorption":  {"cop_ref": 1.4, "source": "LG Therma V double-effect LiBr"},
        "water_cooled":{"cop_ref": 6.0, "source": "Trane CenTraVac CVHG"},
    },
    "pump": {
        "centrifugal":           {"pump_eff_ref": 88, "motor_ref": 97, "source": "Grundfos CRE IE5"},
        "positive_displacement": {"pump_eff_ref": 85, "motor_ref": 95, "source": "Netzsch NEMO optimized"},
        "booster":               {"pump_eff_ref": 82, "motor_ref": 96, "source": "Grundfos CMBE booster"},
    },
    "steam_turbine": {
        "back_pressure": {"eta_is_ref": 88, "gen_ref": 98, "source": "Siemens SST-060"},
        "condensing":    {"eta_is_ref": 90, "gen_ref": 98, "source": "Siemens SST-300"},
        "extraction":    {"eta_is_ref": 87, "gen_ref": 97, "source": "MAN extraction turbine"},
    },
    "dryer": {
        "rotary":        {"sec_ref_kJ_kg": 3000, "source": "Bühler Aeroglide optimized"},
        "fluidized_bed": {"sec_ref_kJ_kg": 2800, "source": "Ventilex fluid bed with heat recovery"},
        "spray":         {"sec_ref_kJ_kg": 3500, "source": "GEA Niro MSD with heat pump"},
        "belt":          {"sec_ref_kJ_kg": 3000, "source": "Bühler Aeroglide belt"},
        "convective":    {"sec_ref_kJ_kg": 3200, "source": "Optimal with exhaust recovery"},
    },
}


def _ref_block(equipment_type: str, subtype: str) -> str:
    """Format reference efficiency block for prompts."""
    refs = REFERENCE_EFFICIENCIES.get(equipment_type, {}).get(subtype, {})
    if not refs:
        return "Reference: Use best available technology (BAT) values from literature."

    source = refs.pop("source", "Industry benchmark")
    lines = [f"Reference (Best Available Technology): {source}"]
    for k, v in refs.items():
        label = k.replace("_ref", "").replace("_", " ").replace("eta is", "η_is").replace("pct", "%")
        lines.append(f"  - {label}: {v}")
    refs["source"] = source  # restore
    return "\n".join(lines)


def _build_template(equipment_type: str, subtype_names: dict, params: dict,
                    operating_block: str) -> dict:
    name = subtype_names.get(params["subtype"], params["subtype"])
    ref_info = _ref_block(equipment_type, params["subtype"])
    refs = REFERENCE_EFFICIENCIES.get(equipment_type, {}).get(params["subtype"], {})

    prompt = f"""Perform a detailed Avoidable/Unavoidable exergy destruction analysis for a {name} {equipment_type.replace('_', ' ')}.

{operating_block}

{ref_info}

Your analysis MUST include:
1. Basic exergy analysis (Ex_in, Ex_out, Ex_d, η_ex)
2. Unavoidable exergy destruction (Ex_d,UN) — calculated using reference/BAT efficiency
3. Avoidable exergy destruction (Ex_d,AV) = Ex_d - Ex_d,UN
4. Avoidable ratio: Ex_d,AV / Ex_d (what fraction can actually be improved)
5. Improvement priority assessment based on avoidable ratio
6. Specific measures to reduce Ex_d,AV with estimated savings
7. Step-by-step calculations ending with summary table."""

    return {
        "instruction": prompt,
        "input": "",
        "metadata": {
            "equipment_type": equipment_type,
            "subtype": params["subtype"],
            "analysis_type": "avoidable_unavoidable",
            "operating_mode": params.get("operating_mode", "full_load"),
            "parameters": {k: v for k, v in params.items() if k != "_derived"},
            "reference_efficiencies": refs,
        }
    }


def template_avun_compressor(p):
    names = {"screw": "screw", "piston": "reciprocating piston",
             "scroll": "scroll", "centrifugal": "centrifugal"}
    block = f"""Operating conditions:
- Electrical power input: {p['power_kW']} kW
- Air inlet temperature: {p['inlet_temp_C']}°C
- Discharge pressure: {p['discharge_pressure_bar']} bar
- Isentropic efficiency: {p['isentropic_efficiency_pct']}%
- Volume flow rate (FAD): {p['flow_rate_m3_min']} m³/min
- Operating mode: {p['operating_mode']}"""
    return _build_template("compressor", names, p, block)


def template_avun_boiler(p):
    names = {"steam_firetube": "fire-tube steam", "steam_watertube": "water-tube steam",
             "condensing": "condensing", "waste_heat": "waste heat recovery", "biomass": "biomass-fired"}
    block = f"""Operating conditions:
- Thermal capacity: {p['thermal_capacity_kW']} kW
- Fuel: {p.get('fuel_type', 'natural_gas')}
- Operating pressure: {p['operating_pressure_bar']} bar
- Stack temperature: {p['stack_temperature_C']}°C
- Feedwater temperature: {p['feedwater_temperature_C']}°C
- Thermal efficiency: {p['thermal_efficiency_pct']}%"""
    return _build_template("boiler", names, p, block)


def template_avun_heat_exchanger(p):
    names = {"shell_tube": "shell and tube", "plate": "plate",
             "economizer": "economizer", "recuperator": "recuperator"}
    block = f"""Operating conditions:
- Hot side: {p['fluid_hot']}, inlet {p['hot_inlet_temp_C']}°C → outlet {p['hot_outlet_temp_C']}°C, flow {p['hot_flow_kg_s']} kg/s
- Cold side: {p['fluid_cold']}, inlet {p['cold_inlet_temp_C']}°C → outlet {p['cold_outlet_temp_C']}°C, flow {p['cold_flow_kg_s']} kg/s"""
    return _build_template("heat_exchanger", names, p, block)


def template_avun_chiller(p):
    names = {"screw": "screw", "centrifugal": "centrifugal",
             "absorption": "absorption", "water_cooled": "water-cooled"}
    block = f"""Operating conditions:
- Cooling capacity: {p['cooling_capacity_kW']} kW
- Evaporator temperature: {p['evaporator_temp_C']}°C
- Condenser temperature: {p['condenser_temp_C']}°C
- COP: {p['cop']}
- Refrigerant: {p['refrigerant']}"""
    return _build_template("chiller", names, p, block)


def template_avun_pump(p):
    names = {"centrifugal": "centrifugal", "positive_displacement": "positive displacement",
             "booster": "booster"}
    block = f"""Operating conditions:
- Volume flow rate: {p['flow_rate_m3_h']} m³/h
- Total head: {p['head_m']} m
- Motor power: {p['motor_power_kW']} kW
- Pump efficiency: {p['pump_efficiency_pct']}%
- Motor efficiency: {p['motor_efficiency_pct']}%
- Fluid: water at {p['fluid_temp_C']}°C"""
    return _build_template("pump", names, p, block)


def template_avun_steam_turbine(p):
    names = {"back_pressure": "back-pressure", "condensing": "condensing",
             "extraction": "extraction"}
    block = f"""Operating conditions:
- Inlet pressure: {p['inlet_pressure_bar']} bar
- Inlet temperature: {p['inlet_temp_C']}°C
- Outlet pressure: {p['outlet_pressure_bar']} bar
- Mass flow rate: {p['mass_flow_kg_s']} kg/s
- Isentropic efficiency: {p['isentropic_efficiency_pct']}%
- Generator efficiency: {p['generator_efficiency_pct']}%"""
    return _build_template("steam_turbine", names, p, block)


def template_avun_dryer(p):
    names = {"rotary": "rotary drum", "fluidized_bed": "fluidized bed",
             "spray": "spray", "belt": "belt", "convective": "convective hot air"}
    block = f"""Operating conditions:
- Air inlet temperature: {p['inlet_air_temp_C']}°C
- Air outlet temperature: {p['outlet_air_temp_C']}°C
- Product flow rate: {p['product_flow_kg_h']} kg/h
- Moisture: {p['initial_moisture_pct']}% → {p['final_moisture_pct']}%
- Thermal input: {p['thermal_input_kW']} kW"""
    return _build_template("dryer", names, p, block)


TEMPLATE_MAP_E = {
    "compressor":     (template_avun_compressor, consistent_compressor_params),
    "boiler":         (template_avun_boiler, consistent_boiler_params),
    "heat_exchanger": (template_avun_heat_exchanger, consistent_heat_exchanger_params),
    "chiller":        (template_avun_chiller, consistent_chiller_params),
    "pump":           (template_avun_pump, consistent_pump_params),
    "steam_turbine":  (template_avun_steam_turbine, consistent_steam_turbine_params),
    "dryer":          (template_avun_dryer, consistent_dryer_params),
}


def generate_prompt(equipment_type: str, subtype: Optional[str] = None) -> dict:
    template_fn, params_fn = TEMPLATE_MAP_E[equipment_type]
    params = params_fn(subtype)
    return template_fn(params)
