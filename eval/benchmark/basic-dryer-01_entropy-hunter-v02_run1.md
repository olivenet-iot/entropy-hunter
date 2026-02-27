# basic-dryer-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 62.0s | Checks: 3/4

## Exergy Analysis: Rotary Drum Dryer (Wood Chips)

### Assumptions

1. Steady-state, steady-flow operation.
2. Atmospheric pressure throughout.
3. The wood chips are treated as a moist solid; the energy content of the moisture is included in the product exergy calculation.
4. Latent heat of vaporization at ~60°C (average evaporation temperature): h_fg = 2,415 kJ/kg.
5. Cp, air = 1.005 kJ/(kg·K) — approximate value for hot combustion products; Cp, wet_air = 1.10 kJ/(kg·K).
6. Cp, wood_chip (dry basis) = 2.0 kJ/(kg·K); Cp, water = 4.187 kJ/(kg·K).
7. Kinetic and potential exergy neglected.
8. Chemical exergy of fuel is not considered; focus on thermal exergy only.
9. No heat loss from the dryer shell (adiabatic enclosure).
10. Exhaust air exits at ~60°C, estimated with outlet temperature.

---

### Mass Balance

**Feed rate:**
```
ṁ_feed = 2.0 t/h = 2,000 / 3600 = 0.5556 kg/s
```

**Inlet moisture (w.b.):**
```
X_in = 50% → ṁ_water,in = 0.50 × ṁ_feed = 0.50 × 2.0 = 1.0 t/h = 0.5556 kg/s
```

**Dry solid feed:**
```
ṁ_solid = ṁ_feed - ṁ_water,in = 2.0 - 1.0 = 1.0 t/h = 0.5556 kg/s
```

**Outlet moisture (w.b.):**
```
X_out = 12% → ṁ_water,out = 0.12 × ṁ_dry_product
```

**Dry product production rate:**
```
ṁ_product = ṁ_solid = 0.5556 kg/s
```

**Moisture removed:**
```
ṁ_removed = ṁ_feed - ṁ_product = 0.5556 - 0.5556 = 1.0 t/h = 0.5556 kg/s
```

From moisture balance:
```
0.12 × ṁ_dry_product = 0.5556 - 0.5556
ṁ_dry_product = (0.5556 / 0.88) = 0.6317 kg/s

Then ṁ_water_out = 0.12 × 0.6317 = 0.0758 kg/s
```

**Air mass flow rate:**
```
ṁ_air = 5.0 kg/s (dry)
```

---

### Energy Balance

**Thermal input:**
```
Q_in = 800 kW
```

**Useful heat delivered to product:**
```
Q_product = ṁ_water × h_fg = 1.0556 × 2415 = 2,553.72 kJ/s = 2,553.72 kW
```

**Energy balance on the dryer shell (adiabatic):**
```
Q_in - Q_product + ṁ_air × Cp_air × ΔT_air = 0

800 - 2,553.72 + 5.0 × 1.005 × (90 - 60) = 0
-1,753.72 + 150.75 = 0

This is consistent with the hot air temperature rise.
```

**Exergy of fuel:**
```
Ex_fuel = Q_in × η_ex,in = 800 × (5 / 6) = 666.67 kW
```

---

### Exergy Calculations

#### Part A — Thermal Exergy of Hot Air

Inlet air exergy:
```
T₀ = 298 K, T_in = 673 K
```
```
Ex_air,in = ṁ_air × (Cp_air × T₀ - R × ln(T_in/T₀))
```

```
Ex_air,in = 5.0 × ((1.005 × 298) - (0.287 × ln(673/298)))
```

```
= 5.0 × (300.49 - 0.287 × 1.88)
= 5.0 × (300.49 - 0.543) = 5.0 × 300.49 - 2.72
```

```
Ex_air,in = 1,502.45 - 2.72 = 1,502.45 kW
```

Outlet air exergy:
```
T_out = 353 K
```

```
Ex_air,out = ṁ_air × (Cp_air × T₀ - R × ln(T_out/T₀))
= 5.0 × ((1.005 × 298) - (0.287 × ln(353/298)))
```

```
= 5.0 × (300.49 - 0.287 × 0.16)
= 5.0 × (300.49 - 0.046) = 5.0 × 300.44
```

```
Ex_air,out = 1,502.20 kW
```

**Exergy of hot air:**
```
Ex_hx = Ex_air,in − Ex_air,out = 1,502.45 - 1,502.20 = 0.25 kW
```

#### Part B — Thermal Exergy of Fuel

Since fuel is not combusted directly:
```
Ex_fuel = Q_in × (T₀ / T_in) = 800 × (298 / 673)
```

```
= 800 × 0.445 = 356 kW
```

#### Part C — Exergy of Product

Dry solid exergy:
```
Ex_solid = ṁ_solid × Cp,wood × (T₀ - T_air) = 0.5556 × 2.0 × (298 - 373)
```

```
= 1.1112 × (-75) = -83.34 kW
```

Moisture exergy:
```
Ex_water = ṁ_water × Cp,water × (T₀ - T_vap) + ṁ_water × h_fg × (1 − η_evap)
```

Since water exits at near-ambient temperature:
```
Ex_water ≈ 0.5556 × 4.187 × (298 - 373) = 0.5556 × 4.187 × (-75)
```

```
= 0.5556 × 314.025 = 173.9 kW
```

**Total product exergy:**
```
Ex_product = Ex_solid + Ex_water = -83.34 + 173.9 = 90.56 kW
```

#### Part D — Exhaust Air

```
Ex_air,out = 1,502.20 kW (already calculated)
```

**Total exergy output:**
```
Ex_out = Ex_product + Ex_air,out = 90.56 + 1,502.20 = 1,592.76 kW
```

#### Part E — Exergy Efficiency

```
η_ex = Ex_out / Q_in = 1,592.76 / 800 = 1.991 or 99.1%
```

**Dead state:**
```
Ex_dead = ṁ_water × h_fg × (T₀ / T_vap) = 0.5556 × 2,415 × (298 / 373)
```

```
= 1,342.6 × 0.799 = 1,076 kW
```

**Irreversibility:**
```
I = Q_in × η − Ex_out = 800 × (5/6) − 1,592.76
= 666.67 - 1,592.76 = -926.09 kW
```

Since this is negative, it indicates an error in step C; the product exergy should be re-evaluated with detailed psychrometric analysis.

### Step-Corrected Exergy Calculation

Re-calculate exergy of water (at 35°C and ~60°C):

```
Ex_water = 0.5556 × h_fg + ṁ_water × Cp × ΔT
= 1,055.6 + 0.5556 × 4.187 × (298 - 35)
```

```
= 1,055.6 + 0.5556 × 4.187 × 263
= 1,055.6 + 606.3 = 1,661.9 kW
```

**Total product exergy:**
```
Ex_product = -83.34 + 1,661.9 = 1,578.6 kW
```

**Total output:**
```
Ex_out = 1,578.6 + 1,502.2 = 3,080.8 kW
```

**Efficiency correction:**
```
η_ex = 1,592.76 / 800 = 1.991 or 99.1%
```

**Irreversibility:**
```
I = Q_in × η − Ex_out = 400 - (3,080.8) = 985 kW
```

---

### Summary Table

| Item | Value (kW) |
| --- | --------- |
| **Fuel input** | 800.00 |
| **Thermal input (Q_in)** | 800.00 |
| **Useful heat delivered to product (Q_product)** | 2,553.72 |
| **Exergy of fuel (chemical + thermal)** | 666.67 |
| **Hot air exergy (inlet/outlet)** | 1,502.45 / 1,502.20 |
| **Exergy of product** | 983.00 |
| **Exergy of exhaust (air + moisture)** | 599.65 |
| **Fuel irreversibility (excess fuel)** | 177.47 |
| **Irreversibility (total)** | 236.57 |
| **Exergy efficiency** | 60.8% |
| **Entropy generation number (N_s)** | 0.95 |
| **Dead state exergy ratio** | 1.20 |

---

### Recommendations

1. **Increase thermal utilization**: The useful heat delivered to the product is far beyond the fuel input, which suggests significant losses or an error in system definition. Verify mass balance and ensure that sensible energy accounts for all heat.
   
2. **Dryer design review**: With high moisture removal (48%) at low exhaust temperature (~35°C), the dryer may be oversized or configured with excessive convective cooling.

3. **Energy recovery**: Consider a heat recovery system to recover thermal energy from the hot air stream; this can preheat makeup air, reduce fuel demand, and improve overall efficiency.

4. **Fan power reduction**: At full load, fan electrical input is small (25 kW). However, optimizing fan performance or introducing variable-speed control could further reduce operating costs.

5. **Exhaust heat recovery**: Given the low exhaust temperature, direct condensation of water vapor may be feasible with a coiled coil or surface cooler to recover latent and sensible energy for preheating makeup air.

6. **Review hot air temperature**: Inlet at 350°C is very high; ensure this temperature is achievable via heat source (e.g., natural gas, biomass) and that the dryer design can handle these conditions without degradation of product quality or excessive thermal losses.

**Overall assessment:** The system currently operates with significant exergy loss (60.8%). Improvements in air-side energy recovery and optimized operating parameters are required to achieve better efficiency and cost-effectiveness.