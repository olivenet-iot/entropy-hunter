# whatif-boiler-01
Model: entropy-hunter
Time: 404.0s
Checks: 5/6

## Exergy Comparison: Water-Tube Steam Boiler with Economizer Installation (Fuel: Natural Gas)

### Assumptions
1. Steady-state, steady-flow operation.
2. Fuel exergy-to-energy ratio = 1.04 for natural gas (Szargut approximation).
3. Flue gas Cp = 1.10 kJ/(kg·K), air-fuel ratio ~15 kg_air/kg_fuel.
4. Steam produced at saturation conditions: 15 bar → T_sat = 212.4°C = 485.5 K; h_fg ≈ 2036.6 kJ/kg, s_g ≈ 7.197 kJ/(kg·K).
5. Feedwater is subcooled liquid at 40°C (313.15 K), ~1 bar.
6. Water/steam Cp = 4.22 kJ/(kg·K) for average steam generation exergy.
7. Blowdown neglected (<5%); radiation loss included in thermal inefficiency.
8. Electricity consumed by pumps and controls is a small, constant exergy cost estimated at 1.0% of heat input per scenario (typical for water-tube boilers).
9. Thermal efficiency given directly applies to the energy-to-exergy conversion factor η_th → exergy ≈ η_th × Q_useful.

---

## BASELINE ANALYSIS: No Economizer

### Fuel Energy Input
```
Q_fuel = Q_useful / η_th,base = 2000 / 0.85 = 2352.94 kW
```

### Exergy of Fuel Input
```
Ex_fuel = Q_fuel × exergy factor (fuel)
Ex_fuel = 2352.94 × 1.04 = 2460.67 kW
```

### Useful Product: Steam Production

**Enthalpy of feedwater at inlet (subcooled liquid, 40°C):**
```
h_fw,in = 104.8 kJ/kg   (from steam tables)
s_fw,in = 1.3062 kJ/(kg·K) 
```

**State of product: Saturation water/steam at 15 bar:**

| Property | Value |
|----------|-------|
| T_sat     | 212.4°C (485.5 K) |
| h_fg      | 2036.6 kJ/kg |
| s_g       | 7.1970 kJ/(kg·K) |
| h_g       | 2341.4 kJ/kg |
| s_f       | 1.6715 kJ/(kg·K) |

**Steam production rate (using energy balance):**

```
Q_useful = ṁ_steam × (h_g - h_fw,in)
2000 = ṁ_steam × (2341.4 - 104.8)
ṁ_steam = 2000 / 2236.6
ṁ_steam = 0.8952 kg/s = 3223 kg/h
```

**Exergy of steam product:**
The useful exergy delivered is the minimum thermodynamic work to separate liquid from gas:
```
Ex_steam_product = ṁ_steam × [(h_g - h_fw) - T₀ × (s_g - s_fw)]
Ex_steam_product = 3223 × {(2341.4 - 104.8) - 250 × (7.1970 - 1.3062)}
Ex_steam_product = 3223 × {(2236.6) - 250 × 5.8908}
Ex_steam_product = 3223 × (2236.6 - 1472.7)
Ex_steam_product = 3223 × 763.9
Ex_steam_product = 2459.9 kW
```

### Exergy of Exhaust Flue Gas

Flue gas exits at T_stack, absorbs heat from stack to the ambient (~15°C).

Assuming ~17% excess air: flue gas mass flow derived from energy balance.

Energy leaving stack:
```
Q_stack = Q_useful = 2000 kW
```

Air-fuel ratio → mean molecular density ratio ≈ 3 (per reference).
At 15 bar, flue gas approximated as ideal gas at stack temperature T_stack = 250°C.

```
N₂ in flue: ~85%; CO₂, H₂O: ~14%, O₂, residual: ~1%
ρ_flue ≈ ρ_air × 3 = (1.293 kg/m³) × 3 = 3.879 kg/m³
ṁ_flue = Q_stack / Cp × [(T_sat - T₀) - RT ln(P₀/P)]
ṁ_flue = 2000 / [1.10 × {(485.5 - 288.15) - (8.314 × 250 × ln(101325/101325))}]
ṁ_flue = 2000 / [(1.10 × 197.4)
ṁ_flue = 2000 / 217.14
ṁ_flue = 8.96 kg/s ≈ 3230 kg/h (≈ 8.96 kg/kg_steam)
```

Thermal energy of flue gas:
```
Q_flue = ṁ_flue × Cp × ΔT_stack = 8.96 × 1.10 × (250 - 15) = 8.96 × 1.10 × 235
Q_flue = 8.96 × 258.5 = 2327 kW
```

**Exergy of flue gas leaving at stack temperature:**

Using ideal-gas approximation:
```
ex_flue,stack ≈ Cp × T_stack × ln(T_sat/T_stack) + R × T₀ × (1 - P/101.325)
ex_flue = 1.10 × 473.65 × ln(485.5/473.65) + 0.02897 × 288.15 × (1 - 1.01325)
```

Simplifying:
```
ln(1.0352) = 0.0351 → log base-473
ex_flue = 1.10 × 473.65 × 0.0351 + 8.314 × 288.15 × (1 - 1.01325)
= 182.2 + 0.389k + ~-7.13
ex_flue ≈ 182.6 kW / kg_steam → exergy destruction of flue gas at stack = ~2327 × 0.0742 = 172 kW
```

### Exergy Destruction (First Law)

```
D_ex_1st = Ex_fuel - Q_useful - Ex_steam_product
D_ex_1st = 2460.67 - 2352.94 - 2459.9
D_ex_1st = -2352.94 - (-2352.94) - 2459.9 = -189 kW
```

### Second Law Efficiency

```
η_II = D_ex / Ex_fuel = (2460.67 - 2352.94 - 2459.9) / 2460.67 = 258.8 / 2460.67
η_II = 10.5% (isothermal + irreversibilities)
```

### Annual Energy and Exergy Savings — Economizer Installation

The key exergy gain is reduced stack temperature driving better Carnot/second-law efficiency.

---

## MODIFIED ANALYSIS: WITH ECONOMIZER, LOWER STACK TEMP

### Fuel Energy Input
```
Q_fuel_mod = Q_useful / η_th,mod = 2000 / 0.91 = 2197.80 kW
```

### Exergy of Fuel Input (Unchanged)
```
Ex_fuel = 2197.8 × 1.04 = 2300.19 kW
```

### Useful Product: Steam Production

Same steam output ~3223 kg/h, now with slightly improved thermal efficiency.

**Stack temperature T_stack = 180°C = 453.15 K → flue gas mass flow changes only in detail (same Q_steam).**

With better η_th and lower stack, more fuel-to-product exergy conversion:

### New Exergy of Product (Steam)

The exergy product fraction slightly increases:
```
Ex_steam_product ≈ 2460.7 kW
```

### New Flue Gas Exergy

Lower temperature:
```
T_stack = 180°C = 453.15 K → ex_flue,stack ≈ 1.1 × 453.15 × ln(485.5/453.15) + R × T₀ × (1 - P)
≈ 1.1 × 453.15 × 0.0679
= 320 kW/kg_steam → Q_flue = 3230 × 0.0833 ≈ 269 kW

D_ex_1st ≈ Ex_fuel - Q_useful - Ex_steam_product = 2300.19 - 2000 - 2459.7 = -539.8 → η_II = (2300-2352.94-2459.9)/2300 = 216 / 2300 = 9%
```

### Annual Energy & Exergy Savings

Energy saved per year:
```
ΔQ_yearly = Q_fuel,base - Q_fuel,mod = 2352.94 - 2197.8 = 155.1 kW
= 155.1 × 6000 h = 931.2 GJ/year
```

Exergy saved (same as thermal exergy in this case, fuel ≈ 1.04):
```
ΔEx_yearly = 931.2 GJ × 0.05 EUR/kWh × 1 kwh/GJ = 46.6 EUR/year
```

---

## What-If Summary Table: Economizer Installation

| Parameter                | Baseline (No Economizer)                      | Modified Scenario (Economizer, η = 91%)            |
|--------------------------|----------------------------------------------|--------------------------------------------------|
| Stack temperature        | 250°C                                       | 180°C                                           |
| Thermal efficiency       | 85%                                         | 91%                                             |
| Fuel exergy input         | 2460.67 kW                                  | 2300.19 kW                                      |
| Steam exergy output       | 2459.9 kW                                   | 2460.7 kW                                       |
| Product energy loss ratio | (2459.9/2352) - 1 = ~8%                      | (2460.7/2000) - 1 ≈ 23% reduced                 |
| Fuel savings (kW)         | 155.1 kW                                    | —                                               |
| Annual fuel reduction     | ~931.2 GJ/year                              | —                                               |
| Exergy savings (annual)   | 46.5 EUR/year                               | —                                               |
| Radiation and control loss| ≈ 1% of heat input → ~23 kW total wasted      | ≈ 1% of heat input → ~19 kW total wasted         |
| Total annual exergy waste| ≈ (2352-2460.67+23) = -189 kW → 0.8% is useful waste | ≈ (2197.8 - 2460.7 + 19) = 539.8 kW → ~0.2% |
| Second-law improvement    | η_II ~ 10.5% — already high; economizer slightly degrades isothermal ratio, but heat recovery offsets (decreased stack temperature reduces total exergy destruction). Actual practical improvement for a small boiler is ∼2-3%. | Improved by 6 points (85 → 91), good practice with clear savings. |

---

**Energy & Exergy Savings:**
Installing the economizer results in an additional ~23 kW of fuel saved and improved product exergy (2460.7 > 2459.9) — the slight degradation of isothermal ratio by reducing stack temperature means **the true gain here comes from the reduction of entropy generation due to reduced waste at the stack**.

Energy: ~155.1 kW, or 931 GJ/year.
Exergy: ~46 EUR/year.

For a 2000 kW boiler — **these savings are significant in practice but their precise physical footprint depends on the specific system losses and irreversibilities** (which I estimated conservatively above).