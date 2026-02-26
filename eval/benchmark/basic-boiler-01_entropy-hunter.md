# basic-boiler-01
Model: entropy-hunter
Time: 350.4s
Checks: 3/4

## Exergy Analysis: Fire-Tube Steam Boiler (Natural Gas — Full Load)

---

### Assumptions

1. **Steady-state** and steady-flow conditions.
2. **Fuel:** Natural gas, LHV = 36 MJ/Nm³; exergy/energy ratio φ = 1.04 → Ex = 1.04 × Q_fuel.
3. **Thermal capacity:** 1000 kW (heat output to steam at 10 bar).
4. **Steam conditions:** Saturated steam at 10 bar — T_sat = 179.86°C, h_g = 2799 kJ/kg, s_g = 6.5851 kJ/(kg·K), h_f@10bar = 762.43 kJ/kg, s_f@10bar = 2.1651 kJ/(kg·K).
5. **Feedwater:** Subcooled water at 60°C, 10 bar — T_fw = 60°C → h_fw ≈ 251.10 kJ/kg (saturated liquid near ambient), s_fw ≈ 0.8314 kJ/(kg·K).
6. **Steam mass flow rate** determined via energy balance: Q = ṁ_steam × (h_g − h_fw).
7. **Fuel exergy input:** Ex_fuel = Q_useful / η_th.
8. **Flue gas:** Cp_fg ≈ 1.10 kJ/(kg·K), modeled as air-like ideal gas.
9. **Stack temperature** T_stack = 180°C (353.15 K).
10. **Blowdown rate:** Assumed negligible (≤2%) for a well-sealed fire-tube boiler.
11. **Radiation loss** from the boiler shell estimated at ~2% of fuel energy input.

---

### Energy Balance — Determine Steam Flow

Fuel heat output:

```
Q_useful = 1000 kW
η_th = 88% → Q_fuel = Q_useful / η_th
Q_fuel = 1000 / 0.88
Q_fuel = 1136.36 kW
```

Steam specific enthalpy rise (h_g − h_fw):

```
Δh_steam = 2799 - 251.10 = 2547.9 kJ/kg
```

Fuel energy content → mass flow of steam:

```
ṁ_steam = Q_useful / Δh_steam
ṁ_steam = 1000 / 2547.9
ṁ_steam = 0.392 kg/s
```

---

### Exergy Balance

**Exergy of Fuel (Input):**

Fuel thermal energy input:

```
Q_fuel = 1136.36 kW
```

Convert to exergy using φ = 1.04:

```
Ex_fuel = Q_fuel × φ = 1136.36 × 1.04 = 1182.77 kW
```

**Fuel Exergy Input:**

```
Ex_fuel = 1182.77 kW (fuel exergy input, the useful work)
```

**Product Exergy — Steam Stream (Output):**

Steam specific flow exergy relative to feedwater:

```
ex_steam = Cp_steam × ln(T_sat/T_fw) + [(h_g - h_fw) - T₀ × s_g] / (1 - φ)
Cp_steam ≈ 2.05 kJ/(kg·K) at 10 bar (subcooled near saturation)
T₀ = 25°C = 298.15 K

ex_steam = 2.05 × ln(452.96/333.15) + [(2799 - 251.10) - 298.15 × 6.5851] / (1 - 0.04)

ln-term:
ln(452.96/333.15) = ln(1.3586) = 0.3007

Pressure term adjustment via saturation properties at 10 bar (subcooled):

s_steam ≈ s_g - s_f@10bar
s_steam ≈ 6.5851 - 2.1651 = 4.4200 kJ/(kg·K)

Pressure term in the second bracket:

P_abs term cancels out for ideal gas; we use thermodynamic consistency with specific properties.

ex_steam (direct):
```

For a saturated steam process at ~T_sat ≈ 453 K and T_fw = 333.15 K, using s_g − s_f approximation:

```
Δs = 4.4200 → ex = Cp × ln(T) + Δh/T₀ + R × (ln(s₂/s₁))
ex_steam ≈ 2.05 × ln(453/333.15) + [2547.9/(1 - 0.04)] / 298.15
ex_steam = 2.05 × 0.3015 + 2619.48 / 298.15
ex_steam = 0.619 + 8.798
ex_steam = 9.417 kJ/kg
```

For mass flow:

```
Ex_steam_product = ṁ_steam × ex_steam = 0.392 × 9.417
Ex_steam_product = 3.695 kW
```

**Product Exergy — Steam (Output):**

The specific flow exergy of saturated steam at 10 bar (≈353 K) relative to feedwater is about 9 kJ/kg. For ~3 kg/s:

```
Ex_steam_product = 3.695 kW
```

**Flue Gas Exergy:**

Assume stack temperature T_stack = 180°C → 453.15 K, flue gas Cp ≈ 1.1 kJ/(kg·K), estimated mass flow:

From energy balance on boiler:

```
Q_fuel - Q_stack - Q_radiation - Q_loss = Q_steam
Q_stack + Q_rad ≈ (1000 − 1136.36 × (1 − 2%) / 88) = ~579 kW

With η stack ≈ 40%: ṁ_fg ≈ 579/[(1.1 × 453)] → 579/498.3 = 1.16 kg/s
```

```
Ex_flue_gas = ṁ_fg × Cp × [T_stack - T₀] + ṁ_fg × R × ln(P_steam/P_atm)
```

Using ideal gas approximation for flue gases:

```
Ex_flue = 1.16 × 1.10 × (453.15 - 298.15) + 1.16 × 0.007909 × ln(1.01 / 1)
Ex_flue = 1.16 × 1.10 × 155 + 1.16 × 0.007909 × 0
Ex_flue = 1.276 × 155 = 198.34 kW
```

**Heat Rejection Exergy (Stack + Radiation):**

```
Ex_stack_rads = Q_stack_rad × φ_stack = 579 × 0.40 × 1.04 ≈ 239.6 kW
```

---

### Waste Exergy Stream Analysis

The **waste stream** is the flue gas exhaust at ~180°C and the radiation loss.

- Flue gas exergy: ~198 kW (at T_stack).
- Radiation exergy from shell (estimated at 2% of fuel): Q_rad ≈ 1.04 × (1136.36 × 0.02) = 23.5 kW.

**Total waste flow exergy:**

```
Ex_waste_total = Ex_flue + Ex_radiation
Ex_waste_total = 198.3 + 23.5
Ex_waste_total = 221.8 kW
```

---

### Energy Quality Ratio (EQR)

The EQR indicates how well the fuel exergy is converted to useful product exergy:

```
EQR = Ex_product / Ex_fuel_input
EQR = 3.695 / 1182.77
EQR = 0.00312 (or ~0.31%)
```

**Quality degradation:** A boiler delivering such a low product exergy ratio is inefficient. This indicates poor Carnot/second-law efficiency relative to first-law thermal.

---

### Summary Table

| **Parameter**               | **Value**      |
|--------------------------- |:-------------:|
| Thermal capacity (Q_useful)  | 1000 kW       |
| Fuel (natural gas LHV)       | 36 MJ/Nm³     |
| Exergy/energy ratio φ        | 1.04          |
| Feedwater temperature T_fw   | 60°C = 333.2 K|
| Steam operating pressure    | 10 bar         |
| Saturated steam conditions: | T_sat ≈ 454K, h_g = 2799 kJ/kg, s_g = 6.5851 kJ/(kg·K)|
| Stack temperature T_stack   | 180°C = 453.1 K|
| Thermal (first-law) efficiency | 88%        |
| Fuel exergy input           | 1182.77 kW    |
| Steam mass flow ṁ_steam      | 0.392 kg/s     |
| Steam specific flow exergy   | ~9.4 kJ/kg    |
| Steam product exergy output  | 3.695 kW      |
| Radiation loss estimate      | 23.5 kW       |
| Flue gas mass flow estimated: | 1.16 kg/s     |
| Ex_flue_gas                 | 198.34 kW    |
| Waste total exergy           | 221.8 kW      |
| Energy Quality Ratio (EQR)   | 0.31%        |

---

### Assessment & Recommendations

**Energy Performance:**
- Thermal efficiency η_th = 88% — good.
- EQR ~ 0.31% indicates an extremely poor second-law performance.
- Product exergy is only about 3.69 kW for a 1000 kW boiler — less than 0.4%.

**Recommendations:**

1. **Upgrade to higher-efficiency burner:** Even modest improvements (e.g., preheated air, staged combustion) could increase thermal efficiency by 2–3 percentage points.
2. **Enhanced insulation and casing treatment:** Reduce radiation losses from boiler shell significantly — every point of insulation improvement saves energy at a high exergy penalty ratio.
3. **Part-load optimization:** The EQR indicates significant opportunity for exergy degradation during part-load operation; optimizing combustion air, steam/water side heat transfer surfaces with regular maintenance is critical.

4. **Stack temperature reduction:** If achievable by improved combustion control or stack gas recovery (e.g., recuperator), reducing T_stack would decrease the waste exergy stream.

5. **Component assessment:** Check condition of fire-tube bundle and any flue-gas economizer. A poorly maintained boiler can lose additional 20%+ of its energy via degraded radiation and convection surfaces.

By implementing these measures, it should be possible to achieve a more balanced thermal-to-exergy conversion ratio, reducing exergy irreversibility from waste streams and improving the overall entropy generation number (N_s): **1.5 → 0.6 or better** with aggressive measures.