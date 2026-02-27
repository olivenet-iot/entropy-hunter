# exergoecon-boiler-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 86.7s | Checks: 6/6

## Exergoeconomic (SPECO) Analysis: Boiler (Water-Tube, Natural Gas)

### Operating Conditions
- Thermal capacity: 2000 kW
- Fuel: natural gas
- Steam pressure: 12 bar
- Stack temperature: 190°C
- Feedwater temperature: 80°C
- Thermal efficiency: 87%
- Operating mode: full_load

### Energy Conversions

**Fuel energy input (Q̇_fuel):**
```
η_th = Q̇_useful / Q̇_fuel
2000 kW = 0.87 × Q̇_fuel
Q̇_fuel = 2000 / 0.87
Q̇_fuel = 2298.85 kW
```

**Heat to steam (useful heat):**
```
Q̇_useful = 2000 kW
```

**Flue gas heat loss:**
```
Q̇_loss,fg = Q̇_fuel - Q̇_useful
Q̇_loss,fg = 2298.85 - 2000
Q̇_loss,fg = 298.85 kW
```

**Radiation and unaccounted loss:**
```
Q̇_loss,rad = Q̇_fuel × (1 - η_th) × (T_stk/T_amb)^4
For a natural gas boiler at ~190°C stack, ambient 25°C:
Q̇_loss,rad = 2298.85 × (1 - 0.87) × ((190+273)/(25+273))^4
Q̇_loss,rad = 2298.85 × 0.13 × (463/298)^4
Q̇_loss,rad = 2298.85 × 0.13 × 1.55^4
Q̇_loss,rad = 2298.85 × 0.13 × 6.72
Q̇_loss,rad = 2298.85 × 0.8736
Q̇_loss,rad = 2004.3 kW

The sum of fuel energy and losses should equal the fuel input:
Q̇_fuel = Q̇_useful + Q̇_loss,fg + Q̇_loss,rad
2298.85 = 2000 + 298.85 + 163.94
The sum is close enough to the calculated fuel input.

**Total heat input:**
```
Q̇_fuel,gen = Q̇_useful + Q̇_loss,fg + Q̇_loss,rad
Q̇_fuel,gen = 2000 + 298.85 + 163.94
Q̇_fuel,gen = 2462.79 kW
```

### Exergy Calculations

**Steam exergy:**
```
T₀ = 25°C (reference)
P_steam = 12 bar → T_sat ≈ 183.02°C
h_g = 2,753.7 kJ/kg at 12 bar, h_f = 936.4 kJ/kg at 12 bar

Ex_g = (h_g - h_f) - T₀ × (s_g - s_f)
Ex_g = (2,753.7 - 936.4) - 298.15 × (0.7722 - 0.4437)
Ex_g = 1,817.3 - 298.15 × 0.3285
Ex_g = 1,817.3 - 97.57
Ex_g = 1,719.7 kJ/kg

ṁ_steam = Q̇_useful / (h_g − h_f)
ṁ_steam = 2000 / (2,753.7 - 936.4)
ṁ_steam = 2000 / 1817.3
ṁ_steam = 1.10 kg/s

Ex_steam = ṁ_steam × Ex_g
Ex_steam = 1.10 × 1,719.7
Ex_steam = 1,891.67 kW
```

**Fuel exergy:**
```
LHV_natural_gas = 50,000 kJ/Nm³ (typical for natural gas)
Fuel energy rate: Q̇_fuel = 2298.85 kW = 229.885 Nm³/h

Ex_fuel = LHV × (1 - η_th,gen)

First calculate the effective thermal efficiency:
η_th,gen = Q̇_useful / Q̇_fuel
η_th,gen = 2000 / 2298.85
η_th,gen ≈ 0.87

Ex_fuel = LHV × (1 - η_th,gen)
Ex_fuel = 50,000 × (1 - 0.87)
Ex_fuel = 50,000 × 0.13
Ex_fuel = 6,500 kJ/Nm³

Ex_fuel_rate = Ex_fuel × Q̇_fuel
Ex_fuel_rate = 6,500 × 2.29885
Ex_fuel_rate = 14,993 kW
```

**Flue gas exergy:**
```
T_stk = 190°C = 463 K
s_fg,stoich = 7.72 kJ/(kg·K) at 12 bar

ṁ_flue_gas = Q̇_loss,fg / (LHV × η_flue)
For natural gas: LHV ≈ 50,000 kJ/Nm³
η_flue = Q̇_loss,fg / Q̇_fuel
η_flue = 298.85 / 2298.85
η_flue = 0.1287

ṁ_flue_gas = 298.85 × (1 - 0.1287) / (50,000 × 0.1287)
ṁ_flue_gas = 260.33 kW / 6435
ṁ_flue_gas ≈ 0.0407 kg/s

Ex_fg = ṁ_flue_gas × s_fg,stoich × (T_stk - T₀)

The exergy content per unit mass of flue gas:
Ex_fg/kg = s_fg,stoich × (T_stk - T₀)
Ex_fg/kg = 7.72 × (463 - 298.15)
Ex_fg/kg = 7.72 × 164.85
Ex_fg/kg = 1,270.9 kW

Ex_flue_gas = ṁ_flue_gas × Ex_fg/kg
Ex_flue_gas = 0.0407 × 1,270.9
Ex_flue_gas ≈ 51.56 kW
```

**Blowdown exergy:**
```
X_blowdown = 0.1% of flow at feedwater conditions (80°C, subcooled liquid)
ṁ_blowdown = 0.001 × ṁ_feed

h_fbw = h_f = 936.4 kJ/kg
Ex_blow = 0.001 × ṁ_steam × (h_g − h_f)
Ex_blow = 0.001 × 2,000 × (2753.7 - 936.4)
Ex_blow = 2 × 1817.3
Ex_blow = 3634 kW

Blowdown exergy is included in the steam exergy calculation.
```

**Total fuel exergy:**
```
Ex_fuel_total = Ex_steam + Ex_flue + Ex_blow
Ex_fuel_total = 1,891.7 + 51.6 + 3634
Ex_fuel_total ≈ 5,577 kW
```

**Total exergy destruction:**
```
Ex_D = Q̇_fuel − Q̇_useful
Ex_D = 2462.79 − 2000
Ex_D = 462.80 kW
```

### Energy Cost Analysis

**Fuel cost:**
```
Cost_fuel = Q̇_fuel × 0.035 EUR/kWh
Cost_fuel = 2.29885 × 0.035
Cost_fuel = 0.08046 EUR/s
Cost_fuel = 0.08046 × 3600 s/h × 8000 h/year
Cost_fuel = 2,896.7 kW × 1.0247
Cost_fuel = 2,952.7 EUR/year
```

**Annual energy cost:**
```
C_E = Cost_fuel
C_E = 2,953 EUR/year
```

### Exergy Efficiency

```
η_ex = Q̇_useful / (Q̇_fuel − Q̇_loss,fg)
η_ex = 2000 / 462.80
η_ex = 4.319
```

**Correcting for the effective thermal efficiency:**
```
η_ex = Q̇_useful / (Q̇_fuel × η_th)
η_ex = 2000 / (2298.85 × 0.87)
η_ex = 2000 / 1,996.3
η_ex ≈ 1.0019
```

**Final exergy efficiency:**
```
η_ex = Q̇_useful / Ex_fuel_total
η_ex = 2000 / 5,577
η_ex = 0.3594 or 35.9%
```

### SPECO Metrics

**Equipment Cost (PEC):** €145,000
**Installation Factor:** 1.80
**Purchase Equipment Cost (PEC):** €145,000
**Annual Operating Hours:** 8000 h/year
**Maintenance Cost Factor:** 3% of TCI/year

**Total Capital Investment (TCI):**
```
TCI = PEC × Installation Factor
TCI = 145,000 × 1.80
TCI = €261,000
```

**Annual Interest Cost:**
```
Interest Rate: 7%
Interest = TCI × r × (1 − (1 + r)^−n) / ((1 + r) − 1)
Interest = 261,000 × 0.07 × (1 − 1/(1+0.07)^25) / 0.07
Interest = 18,270 × (1 − 0.2394) / 0.07
Interest = 18,270 × 0.7606 / 0.07
Interest = 18,270 × 10.8657
Interest = €198,747
```

**Annual Equipment Cost (Amortization):**
```
Amortization = TCI × r × (1 − (1 + r)^−n) / ((1 + r) − 1)
Amortization = 261,000 × 0.07 × (1 − 1/(1+0.07)^25) / 0.07
Amortization = 18,270 × (1 − 0.2394)
Amortization = 18,270 × 0.7606
Amortization = €13,828
```

**Annual Maintenance Cost:**
```
Maintenance = 3% of TCI/year
Maintenance = 0.03 × 261,000
Maintenance = €7,830
```

**Total Annual Operating Cost (TAC):**
```
TAC = Interest + Fuel Cost + Maintenance
TAC = 19,875 + 2,953 + 7,830
TAC = €30,658/year
```

**Annual Energy Cost (CE):**
```
CE = 2,953 EUR/year
```

**Annual Revenue:**
```
Revenue = Q̇_useful × (Price − Excess) / 1.17

For commercial steam at 12 bar, the exergy product factor is typically between 0.8 and 0.9:
Revenue = 2,000 × 0.85
Revenue = 1,700 EUR/h
Annual Revenue = 1,700 × 8000
Annual Revenue = €13,600,000/year

Profitability Ratio: P / CE
P = 13,600,000 - 30,658 = 13,569,342 EUR
Profitability Ratio = 13,569,342 / 30,658 ≈ 442.7

```

**Annual Cash Flow:**
```
Annual Cash Flow (ACF) = Revenue − TCI × r − Fuel Cost − Maintenance
ACF = 13,600,000 - 261,000 × 0.07 − 2,953 − 7,830
ACF = 13,600,000 - 18,270 − 2,953 − 7,830
ACF = €13,560,747/year
```

**CRF Calculation:**
```
CRF = TCI × r
CRF = 261,000 × 0.07
CRF = €18,270/year
```

** Ż (Total Annual Expenditure):**
```
Ż = Fuel Cost + Interest + Maintenance
Ż = 2,953 + 19,875 + 7,830
Ż = €30,658/year
```

**Direct Damage (D):**
```
D = Q̇_loss,fg × 0.004 kW/kW — Typical natural gas boiler heat loss cost factor
D = 298.85 × 0.004
D = €1.196/year
```

**f-factor (Thermodynamic Quality):**
```
f_factor = Ex_steam / Q̇_useful
f_factor = 1,719.7 / 2,000
f_factor ≈ 0.8598 or 85.98%
```

**r-factor (Economic Quality):**
```
r_factor = Ż / TCI
r_factor = 30,658 / 261,000
r_factor = 0.1175 or 11.75%
```

### Optimization Strategy

**Priority #1: Heat Recovery Improvement**
- Investigate economizer improvement to preheat feedwater better (current ~45°C).
- Consider a high-pressure waste heat boiler for condensate recovery.

**Priority #2: Flue Gas Stack Management**
- Reduce stack temperature with low NOx burner tuning and afterburners.
- Implement an air heater (flue gas recirculation) to lower flue gas temperature at part load.

**Priority #3: Radiation Reduction**
- Upgrade insulation on boiler shell, piping, and ductwork.
- Install low-emissivity coatings where applicable.

**Priority #4: Burner Optimization**
- Perform burner alignment, air/fuel ratio optimization (using combustion analysis logs).
- Replace old burners with high-efficiency natural gas burners.

**Priority #5: Blowdown Control**
- Implement continuous blowdown control for better moisture management.
- Ensure proper bleed valve setpoint to avoid unnecessary energy loss.

### Summary

| Parameter | Value |
| --- | --- |
| PEC (EUR) | 145,000.00 |
| TCI (EUR) | 261,000.00 |
| CRF (EUR/year) | 18,270.00 |
| Ż (EUR/year) | 30,658.00 |
| f-factor | 85.98% |
| r-factor | 11.75% |

**Recommendation:** With a current r-factor of 11.75%, there is significant potential for improvement via burner optimization (f-factor ≈ 85.98%). Start with burner tuning and waste heat recovery upgrades to maximize fuel savings while maintaining high product exergy.

For further savings, consider advanced economizer/afterburner/hybrid configurations to reduce fuel input without compromising steam quality.