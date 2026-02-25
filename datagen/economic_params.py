"""
EntropyHunter — Economic Parameter Generation

Generates realistic cost and economic parameters for SPECO thermoeconomic analysis.
PEC correlations from Bejan/Tsatsaronis/Moran (Thermal Design & Optimization, 1996)
and updated industry references.
"""

import random
from typing import Optional


# ============================================================
# PURCHASE EQUIPMENT COST (PEC) CORRELATIONS
# PEC = a × (capacity)^b  [EUR, 2024 basis]
# ============================================================

PEC_CORRELATIONS = {
    "compressor": {
        "screw":       {"a": 2800, "b": 0.75, "capacity_unit": "kW", "capacity_key": "power_kW"},
        "piston":      {"a": 2200, "b": 0.78, "capacity_unit": "kW", "capacity_key": "power_kW"},
        "scroll":      {"a": 3200, "b": 0.72, "capacity_unit": "kW", "capacity_key": "power_kW"},
        "centrifugal": {"a": 3500, "b": 0.70, "capacity_unit": "kW", "capacity_key": "power_kW"},
    },
    "boiler": {
        "steam_firetube":  {"a": 1500, "b": 0.80, "capacity_unit": "kW", "capacity_key": "thermal_capacity_kW"},
        "steam_watertube": {"a": 2000, "b": 0.78, "capacity_unit": "kW", "capacity_key": "thermal_capacity_kW"},
        "condensing":      {"a": 2500, "b": 0.75, "capacity_unit": "kW", "capacity_key": "thermal_capacity_kW"},
        "waste_heat":      {"a": 1800, "b": 0.82, "capacity_unit": "kW", "capacity_key": "thermal_capacity_kW"},
        "biomass":         {"a": 3000, "b": 0.78, "capacity_unit": "kW", "capacity_key": "thermal_capacity_kW"},
    },
    "heat_exchanger": {
        "shell_tube":  {"a": 800, "b": 0.68, "capacity_unit": "kW", "capacity_key": "_Q_kW"},
        "plate":       {"a": 600, "b": 0.72, "capacity_unit": "kW", "capacity_key": "_Q_kW"},
        "economizer":  {"a": 700, "b": 0.70, "capacity_unit": "kW", "capacity_key": "_Q_kW"},
        "recuperator": {"a": 900, "b": 0.65, "capacity_unit": "kW", "capacity_key": "_Q_kW"},
    },
    "chiller": {
        "screw":       {"a": 350, "b": 0.80, "capacity_unit": "kW", "capacity_key": "cooling_capacity_kW"},
        "centrifugal": {"a": 280, "b": 0.82, "capacity_unit": "kW", "capacity_key": "cooling_capacity_kW"},
        "absorption":  {"a": 500, "b": 0.78, "capacity_unit": "kW", "capacity_key": "cooling_capacity_kW"},
        "water_cooled":{"a": 320, "b": 0.80, "capacity_unit": "kW", "capacity_key": "cooling_capacity_kW"},
    },
    "pump": {
        "centrifugal":            {"a": 1800, "b": 0.65, "capacity_unit": "kW", "capacity_key": "motor_power_kW"},
        "positive_displacement":  {"a": 2200, "b": 0.68, "capacity_unit": "kW", "capacity_key": "motor_power_kW"},
        "booster":                {"a": 2000, "b": 0.65, "capacity_unit": "kW", "capacity_key": "motor_power_kW"},
    },
    "steam_turbine": {
        "back_pressure": {"a": 3200, "b": 0.72, "capacity_unit": "kW", "capacity_key": "_power_est_kW"},
        "condensing":    {"a": 3800, "b": 0.70, "capacity_unit": "kW", "capacity_key": "_power_est_kW"},
        "extraction":    {"a": 3500, "b": 0.72, "capacity_unit": "kW", "capacity_key": "_power_est_kW"},
    },
    "dryer": {
        "rotary":        {"a": 2000, "b": 0.78, "capacity_unit": "kW", "capacity_key": "thermal_input_kW"},
        "fluidized_bed": {"a": 2500, "b": 0.75, "capacity_unit": "kW", "capacity_key": "thermal_input_kW"},
        "spray":         {"a": 3000, "b": 0.72, "capacity_unit": "kW", "capacity_key": "thermal_input_kW"},
        "belt":          {"a": 2200, "b": 0.76, "capacity_unit": "kW", "capacity_key": "thermal_input_kW"},
        "convective":    {"a": 1800, "b": 0.80, "capacity_unit": "kW", "capacity_key": "thermal_input_kW"},
    },
}

# Energy prices (EUR/kWh) by fuel type
ENERGY_PRICES = {
    "electricity":    (0.08, 0.18),
    "natural_gas":    (0.03, 0.07),
    "fuel_oil":       (0.04, 0.08),
    "lpg":            (0.05, 0.10),
    "biomass_wood":   (0.02, 0.05),
    "biomass_pellet": (0.03, 0.06),
    "steam":          (0.02, 0.05),
    "district_heat":  (0.03, 0.06),
}

# Installation factor ranges by equipment type
INSTALLATION_FACTORS = {
    "compressor":     (1.4, 1.8),
    "boiler":         (1.6, 2.2),
    "heat_exchanger": (1.3, 1.6),
    "chiller":        (1.5, 2.0),
    "pump":           (1.3, 1.5),
    "steam_turbine":  (1.8, 2.5),
    "dryer":          (1.5, 2.0),
}


def generate_economic_params(equipment_type: str, subtype: str, physical_params: dict) -> dict:
    """
    Generate consistent economic parameters for a given equipment.
    
    Returns dict with PEC, TCI, energy price, CRF inputs, etc.
    """
    # Get PEC correlation
    corr = PEC_CORRELATIONS.get(equipment_type, {}).get(subtype)
    if corr is None:
        # Fallback: use first available subtype
        subtypes = PEC_CORRELATIONS.get(equipment_type, {})
        corr = next(iter(subtypes.values())) if subtypes else {"a": 2000, "b": 0.75, "capacity_key": "power_kW"}

    # Get capacity value
    cap_key = corr["capacity_key"]
    if cap_key.startswith("_"):
        # Special derived keys
        if cap_key == "_Q_kW":
            derived = physical_params.get("_derived", {})
            capacity = derived.get("Q_kW", 100)
        elif cap_key == "_power_est_kW":
            # Estimate turbine power from mass flow (rough)
            capacity = physical_params.get("mass_flow_kg_s", 5) * 200
        else:
            capacity = 100
    else:
        capacity = physical_params.get(cap_key, 100)
    
    capacity = max(capacity, 1)  # avoid zero

    # PEC calculation
    pec_eur = corr["a"] * (capacity ** corr["b"])
    # Add ±15% randomness for market variation
    pec_eur *= random.uniform(0.85, 1.15)
    pec_eur = round(pec_eur, -1)  # round to nearest 10

    # Installation factor → TCI
    inst_lo, inst_hi = INSTALLATION_FACTORS.get(equipment_type, (1.4, 1.8))
    installation_factor = round(random.uniform(inst_lo, inst_hi), 2)

    # Economic parameters
    interest_rate_pct = random.choice([5, 6, 8, 10])
    lifetime_years = random.choice([15, 20, 25])
    maintenance_factor_pct = random.choice([2, 3, 4, 6])
    annual_hours = random.choice([4000, 5000, 6000, 7500, 8000])

    # Energy price depends on equipment fuel type
    fuel_type = physical_params.get("fuel_type", None)
    if equipment_type in ["compressor", "pump", "chiller"]:
        energy_type = "electricity"
    elif fuel_type:
        energy_type = fuel_type
    else:
        energy_type = "natural_gas"

    price_lo, price_hi = ENERGY_PRICES.get(energy_type, (0.05, 0.12))
    energy_price_eur_kwh = round(random.uniform(price_lo, price_hi), 3)

    return {
        "pec_eur": pec_eur,
        "installation_factor": installation_factor,
        "interest_rate_pct": interest_rate_pct,
        "lifetime_years": lifetime_years,
        "maintenance_factor_pct": maintenance_factor_pct,
        "annual_operating_hours": annual_hours,
        "energy_type": energy_type,
        "energy_price_eur_kwh": energy_price_eur_kwh,
        "_derived": {
            "tci_eur": round(pec_eur * installation_factor, -1),
            "capacity_kW": round(capacity, 1),
        }
    }


if __name__ == "__main__":
    # Quick test
    test_params = {"power_kW": 75, "subtype": "screw"}
    econ = generate_economic_params("compressor", "screw", test_params)
    print(f"PEC: €{econ['pec_eur']:,.0f}")
    print(f"TCI: €{econ['_derived']['tci_eur']:,.0f}")
    print(f"Energy: {econ['energy_price_eur_kwh']} EUR/kWh ({econ['energy_type']})")
    print(f"CRF inputs: i={econ['interest_rate_pct']}%, n={econ['lifetime_years']}y")
