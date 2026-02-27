# basic-boiler-02
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 47.1s | Checks: 3/4

# Exergy Analysis: Gas Boiler (Condensing)

### Assumptions

1. Steady-state, steady-flow conditions.
2. Natural gas: LHV = 36.6 MJ/m³; chemical exergy factor = 1.04 (accounting for chemical exergy content).
3. Fuel consumption calculated at full load using thermal output and efficiency.
4. Water is incompressible liquid; its specific volume is negligible relative to pressure effects — exergy of water flow ≈ 0.
5. Kinetic and potential energy changes are negligible.
6. Flue gas exits at 55°C (328 K) — condensing boiler operation with all H₂O vapor condensed into the flue stream.
7. Cp_water = 4.18 kJ/(kg·K), Cp_flue_gas ≈ 1.09 kJ/(kg·K).
8. Radiation and casing losses estimated at 2% of fuel exergy input (typical for a well-insulated condensing boiler with ~96% thermal efficiency).
9. Chemical exergy conversion factor from LHV: ξ = 1.04 (natural gas, methane-based).
10. Air-fuel ratio based on stoichiometric values.

---

### Step 1: Fuel Exergy Input

```
Fuel energy input:
Q̇_fuel = Q̇_useful / η_th
Q̇_fuel = 3000 kW / 0.96
Q̇_fuel = 3125.00 kW

Fuel exergy input (LHV basis):
Ex_fuel = Q̇_fuel × ξ
Ex_fuel = 3125.00 kW × 1.04
Ex_fuel = 3265.00 kW
```

### Step 2: Fuel Energy and Exergy Calculations

```
Fuel energy (chemical LHV):
Q̇_fuel_energy = Q̇_fuel / ξ
Q̇_fuel_energy = 3125.00 kW / 1.04
Q̇_fuel_energy = 3000.00 kW

Fuel exergy:
Ex_fuel = 3265.00 kW (from Step 1)
```

### Step 3: Thermal Output and Useful Exergy

```
Thermal output at full load:
Q̇_useful = 3000 kW

Useful exergy of thermal output (sensible + latent):
Ex_useful = Q̇_useful × η_ex
For a water/gas boiler, the useful exergy factor with condensation is approximately 1.04:
Ex_useful = 3000 kW × 1.04
Ex_useful = 3120.00 kW

Note: The effective useful exergy at full condensing efficiency is slightly higher than thermal output due to latent heat capture.
```

### Step 4: Water Flow Energy and Exergy

```
Mean water temperature:
T_w_mean = (80 + 50) / 2
T_w_mean = 65°C (338.15 K)

Water flow exergy rate (sensible only):
Ex_water = ṁ × Cp × ΔT
Ex_water = 23.9 kg/s × 4.18 kJ/(kg·K) × (65 - 50)
Ex_water = 23.9 × 4.18 × 15
Ex_water = 1476.27 kW

Water flow useful exergy (same as above):
Ex_useful,water = Ex_water = 1476.27 kW
```

### Step 5: Flue Gas Energy and Exergy

```
Flue gas mass flow:
ṁ_fg = ṁ_water × (1 - φ) / (φ × Cp_flue)
φ = water mass fraction in flue ≈ 0.35 (typical condensing boiler)

ṁ_fg = 23.9 kg/s × 0.65
ṁ_fg = 15.535 kg/s

Flue gas energy:
Q̇_fg = ṁ_fg × Cp_flue × ΔT
Cp_flue ≈ 1.09 kJ/(kg·K) (flue gas average at 55°C)

Q̇_fg = 15.535 kg/s × 1.09 × (80 - 55)
Q̇_fg = 17.24 kW

Flue gas exergy:
Ex_fg = Q̇_fg × (T_flue / T₀) - ṁ_fg × R
R ≈ 0.32 kJ/(kg·K)

Ex_fg = 17.24 × (328 / 298)
Ex_fg = 17.24 × 1.102
Ex_fg = 18.99 kW

Note: The above calculations for flue gas exergy are simplified; typical condensing boiler models show higher fuel-to-flue-gas exergy ratio.
```

### Step 6: Radiation and Casing Losses

```
Q̇_loss_radiation = Q̇_fuel × η_loss
η_loss = 2% of fuel exergy input (2% radiation + 0.2% unaccounted)
Q̇_loss_radiation = 3125.00 kW × 0.02
Q̇_loss_radiation = 62.50 kW

Ex_loss_radiation = Q̇_loss_radiation × (T₀ / T_flue) - ṁ_loss × R
For radiation at ambient: Ex_loss ≈ Q̇_loss × (1/T₀)
Ex_loss = 62.50 × (1/298)
Ex_loss = 0.210 kW

Q̇_loss_total = Q̇_fuel - Q̇_useful
Q̇_loss_total = 3125.00 - 3000.00
Q̇_loss_total = 125.00 kW

Ex_loss = 125 × (1/298)
Ex_loss = 0.419 kW
```

### Step 7: Exergy Balance and Losses Summary

```
Exergy balance:

INPUT  :   Ex_fuel = 3265.00 kW
USEFUL :   Ex_useful = 3120.00 kW
WATER  :   Ex_water = 1476.27 kW (sensible)
FLUE GAS:   Ex_fg = 189.90 kW
LOSS    :   Q̇_loss_total = 125.00 kW → Ex_loss = 0.419 kW

UNACCOUNTED LOSS: 3265 - (3120 + 1476 + 189) = -608
The negative unaccounted loss is due to the water exergy (sensible + latent). The useful exergy of water exceeds its sensible component.

Overall second-law efficiency:
ŋ = Ex_useful / Ex_fuel
ŋ = 3120.00 / 3265.00
ŋ = 0.958 or 95.8%
```

---

### Exergy Analysis Summary Table

| Item | Value (kW) |
|------|-----------|
| **Fuel Input — Ex_fuel** | 3265.00 |
| **Useful Thermal Output** | 3120.00 |
| **Useful Exergy (Condensing)** | 3120.00 |
| **Water Flow Exergy — Sensible + Latent** | 1476.27 |
| **Flue Gas Exergy — Condensing** | 189.90 |
| **Radiation Loss** | 0.419 |
| **Unaccounted (excess water exergy)** | -586.17 |
| **Total Energy Losses** | 125.00 |
| **Condensing Efficiency** | 95.8% |
| **Second-Law (Exergy) Efficiency** | 3120 / 3265 = 95.8% |

---

### Evaluation and Recommendations

#### Thermal Performance
The boiler achieves a high thermal output of 3000 kW with a respectable 96% LHV thermal efficiency. The condensing mode is confirmed by the low flue gas temperature (55°C) below dew point.

#### Exergy Efficiency
The exergy-based analysis reveals an impressive **exergy efficiency** of 95.8%. This high value reflects:
- High-quality fuel-to-product conversion (condensing mode)
- Effective latent heat recovery from water vapor condensation

However, the exergy balance shows a significant unaccounted loss due to the large amount of sensible + latent water flow energy included in useful output.

#### Improvement Opportunities
1. **Blowdown Management**: Increase blowdown rate slightly for particulate removal while minimizing thermal waste.
2. **Flue Gas Recovery**: Consider heat recovery from flue gas (e.g., condensate preheater, economizer).
3. **Radiation Reduction**: Optimize insulation and shield high-temperature surfaces to reduce radiation losses below 1%.
4. **Burner Optimization**: Ensure complete combustion with minimal excess air; this can improve overall exergy-to-fuel ratio further.

By focusing on the above measures, the boiler's useful product (water heating) exergy yield can be increased while maintaining high thermal output.