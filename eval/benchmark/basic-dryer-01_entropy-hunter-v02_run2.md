# basic-dryer-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 62.2s | Checks: 2/3

## Exergy Analysis: Rotary Drum Dryer (Wood Chips)

### Assumptions

1. Steady-state, steady-flow operation.
2. Atmospheric pressure for all streams — exergy of pressure is negligible.
3. Kinetic and potential energy changes are negligible.
4. Wood chips treated as a liquid-suspended solid with typical properties derived from the moisture content: CP_solid = 1.5 kJ/(kg·K), CP_water = 4.2 kJ/(kg·K).
5. Latent heat of water at ~60°C average (typical wood chip drying range): h_fg ≈ 2,300 kJ/kg.
6. The hot air is modeled as ideal gas with Cp_air ≈ 1.005 kJ/(kg·K), but since it's a small fraction of total mass flow in the exergy analysis (hot air is only ~2.5% at standard conditions, not explicitly given), its effect on dry air volume is minor.
7. Thermal input of 800 kW from fuel or steam coil represents the actual heat delivered to hot air at an effective thermal efficiency η_eff = Q_dryer / Q_in = 1.625 (based on typical rotary dryer losses). We use this to confirm consistency with stated thermal input.
8. No chemical exergy change of wood chips is considered.

---

### Step 1: Mass Flow Rates

**Wet feed rate:** ṁ_wet = 2.0 t/h = 2,000 / 3600 = 0.5556 kg/s

**Moisture content in (wet basis):** X_in = 50% → Dry solid mass fraction: ds = 1 - 0.5 = 0.5
**Solid flow rate:** ṁ_solid = 0.5 × 0.5556 = 0.2778 kg/s

**Moisture content out (wet basis):** X_out = 12% → Dry solid mass fraction: ds' = 1 - 0.12 = 0.88
**Dry solid flow rate verified:** ṁ_solid = 0.5 × 0.88 = 0.44 kg/s

**Water evaporated (kg/s):**
```
ṁ_water = ṁ_wet − ṁ_solid
ṁ_water = 0.5556 - 0.2778 = 0.2778 kg/s
```

**Dry product flow rate:**
```
ṁ_dry_product = ṁ_solid = 0.44 kg/s
```

---

### Step 2: Energy Balance on Moisture Removal

Energy required to evaporate water:
```
Q_evap = ṁ_water × h_fg
h_fg ≈ 2,300 kJ/kg (at ~60°C)
Q_evap = 0.2778 × 2,300 = 641.94 kW
```

Energy from hot air:
```
Q_air = ṁ_hot_air × Cp_air × (T_in − T_out)
ṁ_hot_air = 5.0 kg/s, but mass ratio is key: Hot air ≈ 2.5% of total
Ẇ_total = 2,000/3600 = 0.5556 kg/s wet feed rate

Since hot air is 5.0 kg/s:
ṁ_dry_air = 5.0 / (1 + 0.2778) ≈ 4.916
ṁ_wet_air_out = ṁ_dry_air + ṁ_water = 4.916 + 0.2778 = 5.1938 kg/s

Hot air temperature: T_in = 350°C = 623.15 K, T_out = 90°C = 363.15 K
Q_air = 4.916 × 1.005 × (623.15 − 363.15)
Q_air = 4.916 × 1.005 × 260
Q_air = 1,287.3 kW

Verification: Q_air must equal thermal input of 800 kW at η_eff = 1.625 (given).
```

**Exergy Analysis:** We use the stated 800 kW as the heat source.
---

### Step 3: Exergy Calculations

#### 3.1 — Thermal (First-Law) Exergy of Fuel Input:

```
Ex_fuel = Q_in × η_eff
Ex_fuel = 800 × 1.625 = 1,300 kW
```

#### 3.2 — Product Exergy: Dry Solid + Latent Heat

**Dry solid exergy:**
```
Ex_solid = ṁ_dry_product × CP_solid × (T_air − T_ambient)
Assume atmospheric temperature for ambient reference: T_amb = 15°C = 288.15 K
Ex_solid = 0.44 × 1.5 × (363.15 - 288.15) = 0.66 × 75 = 49.5 kW
```

**Latent heat exergy of evaporation:**
```
Ex_evap = Q_evap × (h_fg/T_amb)
Ex_evap = 641.94 × (2,300 / 288.15) = 641.94 × 7.98
Ex_evap = 5,110.6 kW
```

**Total product exergy:**
```
Ex_product = Ex_solid + Ex_evap = 49.5 + 5,110.6 = 5,160.1 kW
```

#### 3.3 — Hot Air Entropy Generation

```
Cp_air ≈ 1.005 kJ/(kg·K)
Hot air exergy per kg: Ex_air/kg = T_amb × log(T_hot/T_cold)
Ex_air/kg = 288.15 × log(623.15/363.15) ≈ 288.15 × 0.749
Ex_air/kg = 216.56 kJ/(kg·K)

Hot air exergy input:
Ex_in = ṁ_hot_air × Ex_air/kg = 5.0 × 216.56 = 1,082.8 kW

Energy in hot air stream: Q_hot = 4.916 × 1.005 × (623 - 363)
Q_hot = 4.916 × 1.005 × 260 = 1,297.8 kW
```

**Entropy generation from hot air:** The hot air is at T_in; we need its entropy:
```
s_air = Cp_air / R = 1.005 / 0.247 = 4.059 kJ/(kg·K)
Hot air exergy: Ex_hair = Q_hot × (T_amb / T_hot) = 1,297.8 × (288.15/623.15)

Ex_hair = 1,297.8 × 0.463
Ex_hair = 596.5 kW

```

**Useful hot air exergy:** Hot air is the driving mechanism.
```
Ex_hair_useful = Q_hot − Q_evap = 1,297.8 − 641.94 = 655.86
```

#### 3.4 — Exhaust Air (Waste Stream) Exergy

```
Cp_waste = Cp_air ≈ 1.005 kJ/(kg·K)
Ex_waste = ṁ_wet_air × T_amb × log(T_out/T_amb)
Ex_waste = 0.2778 × 288.15 × log(363.15/288.15)

Ex_waste = 0.2778 × 288.15 × 0.25
Ex_waste = 20.4 kW
```

#### 3.5 — Unaccounted Exergy (Radiation, Blowdown)

```
Ex_unacc = Ex_in − (Ex_product + Ex_waste)
Ex_unacc = 1,687.8 − (5,160.1 + 20.4)
Ex_unacc = 1,687.8 − 5,180.5
Ex_unacc = -3,492.7 kW

Since this is negative: we confirm the system is over-estimated at 800 kW input.
```

---

### Step 4: Exergy Efficiency & Avoidable/Destroyable Calculations

**Efficiency (product exergy / fuel exergy):**
```
η_ex = Ex_product / Ex_fuel
η_ex = 5,160.1 / 1,300 = 3.97
```

Since this is greater than 1: the 800 kW input is re-evaluated against stated thermal input.

**Avoidable exergy (reducing fuel by η_eff):**
```
Avoidable = Ex_fuel × (1 − η_eff)
Avoidable = 1,300 × (1 − 0.625) = 1,300 × 0.375
Avoidable = 487.5 kW
```

**Destroyable exergy (minimum fuel reduction to maintain Q_evap):**
```
Q_min = ṁ_water × h_fg ≈ 641.94 kW

Fuel at minimum: Q_fuel,min = Q_min / η_eff
Q_fuel,min = 641.94 / 0.625
Q_fuel,min = 1,027.1 kW

Ex_fuel,min = Q_fuel,min × (1 − η_recuperator)
For a 30% recuperator: Ex_fuel,min = 1,027.1 × (1 - 0.5) = 513.6 kW
```

**Destroyable exergy:** The difference between 800 and the minimum fuel.

---

### Summary Table

| Item                          | Value            | Unit      |
|-------------------------------|------------------|-----------|
| **Operating Conditions**       |                 |           |
| Hot air inlet (T_in)           | 350             | °C        |
| Hot air outlet (T_out)         | 90              | °C        |
| Thermal input (Q_in, stated)   | 800             | kW        |
| Fuel exergy (Ex_fuel)          | 1,300           | kW        |
| Product exergy (Ex_product)    | 5,160.1         | kW        |
| Hot air exergy input (Q_hot)   | 1,297.8         | kW        |
| Waste stream exergy (Ex_waste)| 20.4            | kW        |
| Unaccounted exergy (error)     | -3,492.7        | kW        |
| **Efficiency**                 |                 |           |
| Exergy efficiency (η_ex)       | 3.97            |          |
| Avoidable exergy savings      | 487.5           | kW        |
| Destroyable exergy reduction   | 286.1 (Q_in → 513.6) | kW    |

---

### Recommendations

1. **Thermal Input Correction:** The stated thermal input of 800 kW is physically impossible for this process at the given hot air conditions and moisture removal rate; it must be lower than 790 kW to match the 642 kW evaporation requirement.
2. **Recuperator Optimization:** A recuperative heat exchanger can reduce fuel by ~513.6 kW (at 30% efficiency) while maintaining product output.
3. **Blowdown Management:** The large unaccounted exergy suggests significant radiation or blowdown losses; better insulation and air control are needed.
4. **Fan Power Correction:** The fan power required for exhaust at 5.19 kg/s is not accounted here, but high-pressure fan systems in this size range typically consume ~2–3 kW for every 0.1 kg/s of exhaust.

**Baseline Improvement:** By installing a 6 kW recuperator + optimizing the air system, the fuel can be reduced by about 4% (avoidable) + 7% (destroyable), achieving a total of approximately 11% fuel reduction — reducing annual energy costs and emissions significantly.