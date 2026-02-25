"""
EntropyHunter — Physically Consistent Parameter Generation

LESSON LEARNED: Power, flow rate, pressure ratio, and efficiency are
interdependent. Randomizing them independently creates impossible scenarios.

APPROACH: Pick anchor parameters, derive the rest from thermodynamics.

For compressors:
  1. Choose: subtype, pressure ratio, isentropic efficiency, flow rate
  2. CALCULATE: isentropic work from thermodynamics
  3. DERIVE: electrical power = W_isentropic / eta_is / eta_motor
  
This ensures every parameter set is physically realizable.
"""

import random
import math
from typing import Optional


# ============================================================
# PHYSICAL CONSTANTS
# ============================================================
CP_AIR = 1.005      # kJ/(kg·K)
R_AIR = 0.287       # kJ/(kg·K)
GAMMA_AIR = 1.4
P_ATM_KPA = 101.325
T0_K = 298.15       # dead state


def _air_density(T_K: float, P_kPa: float) -> float:
    """Ideal gas: ρ = P / (R × T)"""
    return P_kPa / (R_AIR * T_K)


def _isentropic_temp(T1_K: float, P1_kPa: float, P2_kPa: float) -> float:
    """T2s = T1 × (P2/P1)^((γ-1)/γ)"""
    return T1_K * (P2_kPa / P1_kPa) ** ((GAMMA_AIR - 1) / GAMMA_AIR)


# ============================================================
# COMPRESSOR — Physically Consistent Parameters
# ============================================================

# Realistic FAD ranges by subtype (m³/min at inlet conditions)
COMPRESSOR_FAD_RANGES = {
    "screw":       (1.0, 50.0),
    "piston":      (0.5, 15.0),
    "scroll":      (0.3, 5.0),
    "centrifugal": (10.0, 200.0),
}

COMPRESSOR_EFFICIENCY_RANGES = {
    "screw":       (65, 82),
    "piston":      (55, 75),
    "scroll":      (60, 78),
    "centrifugal": (72, 88),
}

COMPRESSOR_MOTOR_EFFICIENCY = {
    "screw":       (90, 95),
    "piston":      (85, 93),
    "scroll":      (88, 94),
    "centrifugal": (92, 97),
}

# Best-practice reference efficiencies for AV/UN split
COMPRESSOR_UNAVOIDABLE_REF = {
    "screw": 88,
    "piston": 82,
    "scroll": 85,
    "centrifugal": 90,
}


def consistent_compressor_params(subtype: Optional[str] = None) -> dict:
    """
    Generate physically consistent compressor parameters.
    
    Anchor: subtype, inlet_temp, discharge_pressure, flow_rate, isentropic_efficiency
    Derived: electrical power input (from thermodynamics)
    """
    if subtype is None:
        subtype = random.choice(["screw", "piston", "scroll", "centrifugal"])

    # Step 1: Choose anchor parameters
    inlet_temp_C = random.choice([15, 20, 25, 30, 35])
    inlet_temp_K = inlet_temp_C + 273.15
    
    discharge_pressure_bar = random.choice([6, 7, 8, 10, 12])
    discharge_pressure_kPa = discharge_pressure_bar * 100
    
    fad_lo, fad_hi = COMPRESSOR_FAD_RANGES[subtype]
    flow_rate_m3_min = round(random.uniform(fad_lo, fad_hi), 1)
    
    eff_lo, eff_hi = COMPRESSOR_EFFICIENCY_RANGES[subtype]
    isentropic_efficiency_pct = round(random.uniform(eff_lo, eff_hi))
    
    mot_lo, mot_hi = COMPRESSOR_MOTOR_EFFICIENCY[subtype]
    motor_efficiency_pct = round(random.uniform(mot_lo, mot_hi))

    # Step 2: Calculate mass flow rate
    rho_inlet = _air_density(inlet_temp_K, P_ATM_KPA)
    flow_rate_m3_s = flow_rate_m3_min / 60
    mass_flow_kg_s = rho_inlet * flow_rate_m3_s

    # Step 3: Isentropic discharge temperature
    T2s_K = _isentropic_temp(inlet_temp_K, P_ATM_KPA, discharge_pressure_kPa)

    # Step 4: Isentropic work
    W_isentropic_kW = mass_flow_kg_s * CP_AIR * (T2s_K - inlet_temp_K)

    # Step 5: Electrical power = W_is / (eta_is × eta_motor)
    eta_is = isentropic_efficiency_pct / 100
    eta_motor = motor_efficiency_pct / 100
    power_kW = W_isentropic_kW / (eta_is * eta_motor)
    power_kW = round(power_kW, 1)

    # Step 6: Specific power check (sanity)
    spc = power_kW / flow_rate_m3_min
    # Typical SPC ranges: 4-8 kW/(m³/min) at 7-10 bar
    # If SPC is way off, the parameters are still consistent but unusual

    # Step 7: Operating mode
    operating_mode = random.choice(["full_load", "part_load_75pct", "part_load_50pct"])
    
    # If part load, adjust flow and power proportionally
    if operating_mode == "part_load_75pct":
        load_factor = 0.75
        flow_rate_m3_min = round(flow_rate_m3_min * load_factor, 1)
        # Part load power penalty: power doesn't drop linearly
        power_kW = round(power_kW * load_factor * random.uniform(1.05, 1.15), 1)
    elif operating_mode == "part_load_50pct":
        load_factor = 0.50
        flow_rate_m3_min = round(flow_rate_m3_min * load_factor, 1)
        power_kW = round(power_kW * load_factor * random.uniform(1.10, 1.25), 1)

    return {
        "subtype": subtype,
        "power_kW": power_kW,
        "inlet_temp_C": inlet_temp_C,
        "discharge_pressure_bar": discharge_pressure_bar,
        "isentropic_efficiency_pct": isentropic_efficiency_pct,
        "flow_rate_m3_min": flow_rate_m3_min,
        "operating_mode": operating_mode,
        # Derived values (for quality checking, not sent in prompt)
        "_derived": {
            "mass_flow_kg_s": round(mass_flow_kg_s, 4),
            "T2s_K": round(T2s_K, 2),
            "W_isentropic_kW": round(W_isentropic_kW, 2),
            "spc_kW_per_m3_min": round(spc, 2),
            "motor_efficiency_pct": motor_efficiency_pct,
        }
    }


# ============================================================
# BOILER — Physically Consistent Parameters
# ============================================================

FUEL_LHV = {
    "natural_gas": 47100,     # kJ/kg
    "fuel_oil": 40600,
    "lpg": 46350,
    "biomass_wood": 14400,
    "biomass_pellet": 17500,
}

FUEL_EXERGY_RATIO = {
    "natural_gas": 1.04,
    "fuel_oil": 1.06,
    "lpg": 1.06,
    "biomass_wood": 1.15,
    "biomass_pellet": 1.12,
}

# Approximate saturated steam enthalpy (kJ/kg) at given pressures
STEAM_ENTHALPY_APPROX = {
    4: {"h_g": 2738, "T_sat_C": 143.6},
    6: {"h_g": 2757, "T_sat_C": 158.8},
    8: {"h_g": 2769, "T_sat_C": 170.4},
    10: {"h_g": 2778, "T_sat_C": 179.9},
    15: {"h_g": 2792, "T_sat_C": 198.3},
    20: {"h_g": 2799, "T_sat_C": 212.4},
}


def consistent_boiler_params(subtype: Optional[str] = None) -> dict:
    """
    Generate physically consistent boiler parameters.
    
    Anchor: subtype, thermal_capacity, pressure, fuel_type, feedwater_temp
    Derived: stack temperature constrained by efficiency, efficiency range by subtype
    """
    if subtype is None:
        subtype = random.choice(["steam_firetube", "steam_watertube",
                                  "condensing", "waste_heat", "biomass"])

    # Fuel selection based on subtype
    fuel_map = {
        "steam_firetube": ["natural_gas", "fuel_oil"],
        "steam_watertube": ["natural_gas", "fuel_oil"],
        "hotwater": ["natural_gas", "lpg"],
        "condensing": ["natural_gas"],
        "waste_heat": ["natural_gas"],
        "biomass": ["biomass_wood", "biomass_pellet"],
    }
    fuel_type = random.choice(fuel_map.get(subtype, ["natural_gas"]))

    # Thermal capacity by subtype
    capacity_ranges = {
        "steam_firetube": [250, 500, 1000, 2000],
        "steam_watertube": [500, 1000, 2000, 5000],
        "hotwater": [50, 100, 250, 500],
        "condensing": [50, 100, 250, 500],
        "waste_heat": [100, 500, 1000, 2000],
        "biomass": [100, 250, 500, 1000],
    }
    thermal_capacity_kW = random.choice(capacity_ranges.get(subtype, [500]))

    # Pressure (steam boilers need higher, hot water lower)
    if subtype in ["hotwater", "condensing"]:
        operating_pressure_bar = random.choice([2, 3, 4, 6])
    else:
        operating_pressure_bar = random.choice([6, 8, 10, 15, 20])

    # Feedwater temperature
    feedwater_temperature_C = random.choice([15, 40, 60, 80, 100])

    # Efficiency range by subtype (thermal/first-law)
    efficiency_ranges = {
        "steam_firetube": (82, 90),
        "steam_watertube": (84, 92),
        "hotwater": (85, 93),
        "condensing": (92, 98),
        "waste_heat": (70, 85),
        "biomass": (75, 88),
    }
    eff_lo, eff_hi = efficiency_ranges.get(subtype, (80, 90))
    thermal_efficiency_pct = round(random.uniform(eff_lo, eff_hi))

    # Stack temperature — constrained by efficiency
    # Higher efficiency → lower stack temp (more heat recovered)
    if thermal_efficiency_pct > 92:
        stack_temperature_C = random.choice([80, 100, 120])
    elif thermal_efficiency_pct > 85:
        stack_temperature_C = random.choice([120, 150, 180])
    else:
        stack_temperature_C = random.choice([180, 200, 250, 300])

    # Ensure stack temp > feedwater temp (physical constraint)
    if stack_temperature_C <= feedwater_temperature_C + 20:
        stack_temperature_C = feedwater_temperature_C + random.choice([30, 50, 80])

    operating_mode = random.choice(["full_load", "part_load_75pct"])

    return {
        "subtype": subtype,
        "thermal_capacity_kW": thermal_capacity_kW,
        "fuel_type": fuel_type,
        "operating_pressure_bar": operating_pressure_bar,
        "stack_temperature_C": stack_temperature_C,
        "feedwater_temperature_C": feedwater_temperature_C,
        "thermal_efficiency_pct": thermal_efficiency_pct,
        "operating_mode": operating_mode,
    }


# ============================================================
# HEAT EXCHANGER — Physically Consistent Parameters
# ============================================================

def consistent_heat_exchanger_params(subtype: Optional[str] = None) -> dict:
    """
    Generate physically consistent heat exchanger parameters.
    
    Key constraints:
    - T_hot_out > T_cold_in (no temperature crossover for single-pass)
    - T_cold_out < T_hot_in
    - Energy balance: m_hot × Cp_hot × ΔT_hot ≈ m_cold × Cp_cold × ΔT_cold
    - Approach temperature ≥ 5°C
    """
    if subtype is None:
        subtype = random.choice(["shell_tube", "plate", "economizer", "recuperator"])

    # Fluid selection based on subtype
    fluid_map = {
        "shell_tube": {"hot": ["water", "steam", "thermal_oil"], "cold": ["water"]},
        "plate": {"hot": ["water"], "cold": ["water", "glycol_solution"]},
        "economizer": {"hot": ["flue_gas"], "cold": ["water"]},
        "recuperator": {"hot": ["flue_gas"], "cold": ["air"]},
        "air_cooled": {"hot": ["water"], "cold": ["air"]},
        "finned_tube": {"hot": ["flue_gas"], "cold": ["air"]},
    }
    fluids = fluid_map.get(subtype, {"hot": ["water"], "cold": ["water"]})
    fluid_hot = random.choice(fluids["hot"])
    fluid_cold = random.choice(fluids["cold"])

    # Cp values for energy balance
    cp_values = {
        "water": 4.18,
        "steam": 2.01,
        "flue_gas": 1.10,
        "air": 1.005,
        "thermal_oil": 1.85,
        "glycol_solution": 3.65,
    }
    cp_hot = cp_values.get(fluid_hot, 4.18)
    cp_cold = cp_values.get(fluid_cold, 4.18)

    # Temperature ranges depend on fluid
    if fluid_hot == "flue_gas":
        hot_inlet_C = random.choice([200, 250, 300, 350, 400, 450])
    elif fluid_hot == "thermal_oil":
        hot_inlet_C = random.choice([150, 200, 250, 300])
    else:
        hot_inlet_C = random.choice([60, 80, 100, 120, 150])

    cold_inlet_C = random.choice([10, 15, 20, 25, 30])
    
    # Approach temperature (minimum ΔT between streams)
    approach_C = random.choice([5, 8, 10, 15, 20])
    
    # Hot outlet: must be above cold inlet + approach
    hot_outlet_C = max(
        cold_inlet_C + approach_C,
        round(hot_inlet_C * random.uniform(0.3, 0.6))
    )
    
    # Cold outlet: must be below hot inlet - approach
    cold_outlet_max = hot_inlet_C - approach_C
    cold_outlet_C = min(
        cold_outlet_max,
        round(cold_inlet_C + (hot_inlet_C - cold_inlet_C) * random.uniform(0.3, 0.7))
    )
    cold_outlet_C = max(cold_outlet_C, cold_inlet_C + 10)  # at least 10°C rise

    # Hot side flow rate
    hot_flow_kg_s = round(random.uniform(0.5, 10.0), 1)

    # Calculate cold side flow from energy balance: m_h × cp_h × ΔT_h = m_c × cp_c × ΔT_c
    Q_hot = hot_flow_kg_s * cp_hot * (hot_inlet_C - hot_outlet_C)
    delta_T_cold = cold_outlet_C - cold_inlet_C
    if delta_T_cold > 0:
        cold_flow_kg_s = Q_hot / (cp_cold * delta_T_cold)
        cold_flow_kg_s = round(cold_flow_kg_s, 1)
    else:
        cold_flow_kg_s = round(hot_flow_kg_s * 1.2, 1)

    # Ensure cold flow is reasonable (not too small or too large)
    cold_flow_kg_s = max(0.3, min(cold_flow_kg_s, 50.0))

    operating_mode = random.choice(["full_load", "part_load_75pct", "fouled_moderate"])

    return {
        "subtype": subtype,
        "hot_inlet_temp_C": hot_inlet_C,
        "hot_outlet_temp_C": hot_outlet_C,
        "cold_inlet_temp_C": cold_inlet_C,
        "cold_outlet_temp_C": cold_outlet_C,
        "hot_flow_kg_s": hot_flow_kg_s,
        "cold_flow_kg_s": cold_flow_kg_s,
        "fluid_hot": fluid_hot,
        "fluid_cold": fluid_cold,
        "operating_mode": operating_mode,
        "_derived": {
            "Q_kW": round(Q_hot, 1),
            "cp_hot": cp_hot,
            "cp_cold": cp_cold,
            "approach_C": approach_C,
        }
    }


# ============================================================
# CHILLER — Physically Consistent Parameters
# ============================================================

def consistent_chiller_params(subtype: Optional[str] = None) -> dict:
    """
    Key constraint: COP must be below Carnot COP.
    COP_Carnot = T_evap / (T_cond - T_evap)  [in Kelvin]
    """
    if subtype is None:
        subtype = random.choice(["screw", "centrifugal", "absorption", "water_cooled"])

    evaporator_temp_C = random.choice([-5, 0, 2, 5, 7, 10])
    condenser_temp_C = random.choice([30, 35, 38, 40, 45])

    # Carnot COP limit
    T_evap_K = evaporator_temp_C + 273.15
    T_cond_K = condenser_temp_C + 273.15
    cop_carnot = T_evap_K / (T_cond_K - T_evap_K)

    # Realistic COP as fraction of Carnot
    carnot_fraction_ranges = {
        "screw": (0.35, 0.50),
        "centrifugal": (0.40, 0.55),
        "scroll": (0.30, 0.45),
        "reciprocating": (0.30, 0.42),
        "absorption": (0.08, 0.15),  # much lower for absorption
        "air_cooled": (0.25, 0.38),
        "water_cooled": (0.38, 0.52),
    }
    frac_lo, frac_hi = carnot_fraction_ranges.get(subtype, (0.30, 0.45))
    carnot_fraction = random.uniform(frac_lo, frac_hi)
    cop = round(cop_carnot * carnot_fraction, 1)
    
    # Ensure COP is in realistic absolute range
    cop = max(cop, 0.6 if subtype == "absorption" else 2.0)
    cop = min(cop, 1.5 if subtype == "absorption" else 7.0)

    refrigerant_map = {
        "screw": ["R134a", "R410A"],
        "centrifugal": ["R134a", "R1234ze"],
        "scroll": ["R410A"],
        "reciprocating": ["R134a"],
        "absorption": ["LiBr_H2O"],
        "air_cooled": ["R410A", "R134a"],
        "water_cooled": ["R134a", "R410A"],
    }

    cooling_capacity_kW = random.choice([50, 100, 200, 500, 1000, 2000])

    return {
        "subtype": subtype,
        "cooling_capacity_kW": cooling_capacity_kW,
        "evaporator_temp_C": evaporator_temp_C,
        "condenser_temp_C": condenser_temp_C,
        "cop": cop,
        "refrigerant": random.choice(refrigerant_map.get(subtype, ["R134a"])),
        "operating_mode": random.choice(["full_load", "part_load_75pct"]),
        "_derived": {
            "cop_carnot": round(cop_carnot, 2),
            "carnot_fraction": round(carnot_fraction, 3),
            "compressor_power_kW": round(cooling_capacity_kW / cop, 1),
        }
    }


# ============================================================
# PUMP — Physically Consistent Parameters
# ============================================================

def consistent_pump_params(subtype: Optional[str] = None) -> dict:
    """
    Key constraint: hydraulic power = ρ × g × Q × H
    Motor power must be > hydraulic power / (η_pump × η_motor)
    """
    if subtype is None:
        subtype = random.choice(["centrifugal", "positive_displacement", "booster"])

    flow_rate_m3_h = random.choice([5, 10, 20, 50, 100, 200])
    head_m = random.choice([10, 20, 30, 50, 80, 100])
    
    pump_efficiency_pct = round(random.uniform(55, 82))
    motor_efficiency_pct = round(random.uniform(87, 94))
    fluid_temp_C = random.choice([15, 25, 40, 60, 80])

    # Calculate hydraulic power
    rho = 998  # kg/m³ (water, approximate)
    g = 9.81
    Q_m3_s = flow_rate_m3_h / 3600
    P_hyd_kW = rho * g * Q_m3_s * head_m / 1000

    # Motor power from hydraulic power and efficiencies
    eta_pump = pump_efficiency_pct / 100
    eta_motor = motor_efficiency_pct / 100
    motor_power_kW = P_hyd_kW / (eta_pump * eta_motor)
    
    # Round to nearest standard motor size
    standard_motors = [0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75, 90, 110]
    motor_power_kW = min(standard_motors, key=lambda x: abs(x - motor_power_kW))

    operating_mode = random.choice(["full_load", "part_load_75pct", "part_load_50pct"])

    return {
        "subtype": subtype,
        "flow_rate_m3_h": flow_rate_m3_h,
        "head_m": head_m,
        "motor_power_kW": motor_power_kW,
        "pump_efficiency_pct": pump_efficiency_pct,
        "motor_efficiency_pct": motor_efficiency_pct,
        "fluid_temp_C": fluid_temp_C,
        "operating_mode": operating_mode,
        "_derived": {
            "P_hydraulic_kW": round(P_hyd_kW, 2),
            "wire_to_water_pct": round(P_hyd_kW / motor_power_kW * 100, 1),
        }
    }


# ============================================================
# STEAM TURBINE — Physically Consistent Parameters
# ============================================================

def consistent_steam_turbine_params(subtype: Optional[str] = None) -> dict:
    """
    Key constraints:
    - Inlet temp must be above saturation temp at inlet pressure
    - Outlet pressure < inlet pressure
    - Superheat must be sufficient
    """
    if subtype is None:
        subtype = random.choice(["back_pressure", "condensing", "extraction"])

    # Inlet pressure and corresponding minimum superheat
    inlet_pressure_bar = random.choice([10, 15, 20, 30, 40, 60])
    
    # Saturation temperatures (approximate)
    T_sat = {10: 180, 15: 198, 20: 212, 30: 234, 40: 250, 60: 276}
    T_sat_C = T_sat.get(inlet_pressure_bar, 200)
    
    # Inlet temp must be above saturation + superheat margin
    min_inlet_C = T_sat_C + 20
    inlet_temp_options = [t for t in [250, 300, 350, 400, 450, 500, 540] if t >= min_inlet_C]
    inlet_temp_C = random.choice(inlet_temp_options) if inlet_temp_options else min_inlet_C + 50

    # Outlet pressure by subtype
    outlet_ranges = {
        "back_pressure": [2.0, 3.0, 4.0, 6.0],
        "condensing": [0.05, 0.08, 0.1],
        "extraction": [1.0, 2.0, 3.0],
        "orc": [1.0, 2.0],
        "micro_turbine": [1.5, 2.0],
    }
    outlet_pressure_bar = random.choice(outlet_ranges.get(subtype, [2.0]))

    # Ensure pressure ratio > 2
    if inlet_pressure_bar / outlet_pressure_bar < 2:
        outlet_pressure_bar = inlet_pressure_bar / random.choice([3, 4, 5])

    mass_flow_kg_s = random.choice([1, 2, 5, 10, 20, 50])
    isentropic_efficiency_pct = round(random.uniform(65, 85))
    generator_efficiency_pct = random.choice([92, 94, 95, 96])

    return {
        "subtype": subtype,
        "inlet_pressure_bar": inlet_pressure_bar,
        "inlet_temp_C": inlet_temp_C,
        "outlet_pressure_bar": round(outlet_pressure_bar, 2),
        "mass_flow_kg_s": mass_flow_kg_s,
        "isentropic_efficiency_pct": isentropic_efficiency_pct,
        "generator_efficiency_pct": generator_efficiency_pct,
        "operating_mode": random.choice(["full_load", "part_load_75pct"]),
    }


# ============================================================
# DRYER — Physically Consistent Parameters
# ============================================================

def consistent_dryer_params(subtype: Optional[str] = None) -> dict:
    """
    Key constraints:
    - Outlet air temp < inlet air temp
    - Thermal input must be sufficient for moisture removal
    - Specific energy consumption in realistic range
    """
    if subtype is None:
        subtype = random.choice(["rotary", "fluidized_bed", "spray", "belt", "convective"])

    inlet_air_temp_C = random.choice([80, 100, 120, 150, 180])
    outlet_air_temp_C = random.choice([t for t in [40, 50, 60, 70] if t < inlet_air_temp_C])

    product_flow_kg_h = random.choice([50, 100, 200, 500, 1000])
    initial_moisture_pct = random.choice([30, 40, 50, 60, 70])
    final_moisture_pct = random.choice([3, 5, 8, 10, 12])

    # Ensure initial > final moisture
    if final_moisture_pct >= initial_moisture_pct:
        final_moisture_pct = max(3, initial_moisture_pct - 20)

    # Calculate water removal rate
    X_in = initial_moisture_pct / 100
    X_out = final_moisture_pct / 100
    water_removed_kg_h = product_flow_kg_h * (X_in - X_out) / (1 - X_out)

    # Thermal input based on realistic specific energy consumption
    # SEC typically 3000-8000 kJ/kg water for industrial dryers
    sec_ranges = {
        "rotary": (3500, 5500),
        "fluidized_bed": (3000, 5000),
        "spray": (4000, 7000),
        "belt": (3500, 5500),
        "convective": (4000, 6500),
        "heat_pump": (2000, 3500),
        "infrared": (3000, 5000),
    }
    sec_lo, sec_hi = sec_ranges.get(subtype, (3500, 6000))
    sec_kJ_per_kg = random.uniform(sec_lo, sec_hi)

    thermal_input_kW = round(water_removed_kg_h * sec_kJ_per_kg / 3600, 0)
    thermal_input_kW = max(thermal_input_kW, 20)  # minimum 20 kW

    return {
        "subtype": subtype,
        "inlet_air_temp_C": inlet_air_temp_C,
        "outlet_air_temp_C": outlet_air_temp_C,
        "product_flow_kg_h": product_flow_kg_h,
        "initial_moisture_pct": initial_moisture_pct,
        "final_moisture_pct": final_moisture_pct,
        "thermal_input_kW": thermal_input_kW,
        "operating_mode": random.choice(["full_load", "part_load_75pct"]),
        "_derived": {
            "water_removed_kg_h": round(water_removed_kg_h, 1),
            "sec_kJ_per_kg_water": round(sec_kJ_per_kg, 0),
        }
    }


# ============================================================
# VALIDATION
# ============================================================

def validate_params(equipment_type: str, params: dict) -> tuple[bool, list[str]]:
    """Quick physical sanity check on generated parameters."""
    errors = []
    
    if equipment_type == "compressor":
        p = params
        # SPC check
        if p["flow_rate_m3_min"] > 0:
            spc = p["power_kW"] / p["flow_rate_m3_min"]
            if spc < 2.0 or spc > 15.0:
                errors.append(f"SPC = {spc:.1f} kW/(m³/min) outside typical range [2, 15]")
    
    elif equipment_type == "heat_exchanger":
        p = params
        if p["hot_outlet_temp_C"] <= p["cold_inlet_temp_C"]:
            errors.append("Temperature crossover: T_hot_out <= T_cold_in")
        if p["cold_outlet_temp_C"] >= p["hot_inlet_temp_C"]:
            errors.append("Temperature crossover: T_cold_out >= T_hot_in")
    
    elif equipment_type == "chiller":
        p = params
        derived = p.get("_derived", {})
        if derived.get("cop_carnot") and p["cop"] >= derived["cop_carnot"]:
            errors.append(f"COP ({p['cop']}) >= Carnot COP ({derived['cop_carnot']})")
    
    elif equipment_type == "pump":
        p = params
        derived = p.get("_derived", {})
        if derived.get("wire_to_water_pct", 100) > 100:
            errors.append("Wire-to-water efficiency > 100%")
    
    return len(errors) == 0, errors


# ============================================================
# MASTER INTERFACE
# ============================================================

CONSISTENT_GENERATORS = {
    "compressor": consistent_compressor_params,
    "boiler": consistent_boiler_params,
    "heat_exchanger": consistent_heat_exchanger_params,
    "chiller": consistent_chiller_params,
    "pump": consistent_pump_params,
    "steam_turbine": consistent_steam_turbine_params,
    "dryer": consistent_dryer_params,
}


def generate_consistent_params(equipment_type: str, subtype: Optional[str] = None) -> dict:
    """Generate physically consistent parameters with validation."""
    generator = CONSISTENT_GENERATORS[equipment_type]
    
    for attempt in range(10):
        params = generator(subtype)
        valid, errors = validate_params(equipment_type, params)
        if valid:
            return params
        # Retry with different random values
    
    # Return last attempt even if not perfect
    return params


if __name__ == "__main__":
    import json
    
    print("=== Physically Consistent Parameter Generation Test ===\n")
    
    for eq_type in CONSISTENT_GENERATORS:
        params = generate_consistent_params(eq_type)
        valid, errors = validate_params(eq_type, params)
        
        # Remove _derived for display
        display = {k: v for k, v in params.items() if k != "_derived"}
        derived = params.get("_derived", {})
        
        status = "✅" if valid else f"❌ {errors}"
        print(f"{eq_type}/{params.get('subtype', '?')} {status}")
        print(f"  Params: {json.dumps(display, indent=None)}")
        if derived:
            print(f"  Derived: {json.dumps(derived, indent=None)}")
        print()
