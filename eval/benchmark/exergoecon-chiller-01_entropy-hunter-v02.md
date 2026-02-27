# exergoecon-chiller-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 52.4s | Checks: 5/6

## Exergoeconomic (SPECO) Analysis: Centrifugal Chiller (500 kW, R-134a)

### Assumptions

1. Steady-state, steady-flow operation.
2. Evaporator temperature T_cold = 5°C → T_cold,in = 5 + 273.15 = 278.15 K (supplying chilled water at ~5°C).
3. Condenser temperature T_hot = 35°C → T_hot,out = 35 + 273.15 = 308.15 K (rejecting heat to condenser water at ~35°C).
4. COP = Q_cold / W_comp = 4.2 (given, full-load condition).
5. Refrigerant: R-134a.
6. Kinetic and potential exergy changes are negligible.
7. Heat rejection at the condenser is a useful process; therefore, all extracted work contributes to the cold production.

### Energy Balance

**Cold (exergy product):**
```
Q_cold = 500 kW
T_cold,in = 278.15 K
T_0 = 298.15 K
Ex_cold = Q_cold × ((T_0 - T_cold,in) / T_0)
Ex_cold = 500 × (298.15 - 278.15) / 298.15
Ex_cold = 500 × 0.06734
Ex_cold = 33.67 kW
```

**Heat rejection:**
```
Q_hot = Q_cold + W_comp = 500 + (500 / 4.2) = 500 + 119.05 = 619.05 kW
```

**Compensation work:**
```
W_comp = Q_cold / COP = 500 / 4.2 = 119.05 kW
```

### Exergy Balance

**Total exergy input (work):**
```
Ex_in = W_comp = 119.05 kW
```

**Cold-side exergy output:**
```
Ex_cold = Q_cold × ((T_0 - T_cold) / T_0)
Ex_cold = 500 × (298.15 - 278.15) / 298.15
Ex_cold = 500 × 0.06734
Ex_cold = 33.67 kW
```

**Condenser exergy rejection:**
```
Ex_hot = Q_hot × ((T_0 - T_hot) / T_0)
Ex_hot = 619.05 × (298.15 - 308.15) / 298.15
Ex_hot = 619.05 × (-0.03400)
Ex_hot = -21.05 kW
```

**Irreversibility at condenser:**
```
Ex_d,cond = Q_hot × (T_0 / T_hot) × (1 - T_cold / T_0)
Ex_d,cond = 619.05 × (298.15 / 308.15) × (1 - 278.15 / 298.15)
Ex_d,cond = 619.05 × 0.9674 × 0.0667
Ex_d,cond = 619.05 × 0.0643
Ex_d,cond = 40.08 kW
```

**Total irreversibility:**
```
Ex_d = Ex_cold + Ex_hot - Ex_in
Ex_d = 33.67 - 21.05 + 119.05 - 119.05
Ex_d = 14.67 kW
```

**Efficiency (COP_ex):**
```
COP_ex = Ex_cold / W_comp = 33.67 / 119.05 = 0.2829
```

**Irreversibility ratio:**
```
η_d = Ex_d / Ex_in = 14.67 / 119.05 = 0.1228
```

### Entropy Generation Minimization (EGM) — Avoidable, Unavoidable

**Unavoidable irreversibility (second-law efficiency):**
```
ŋ_unav = 1 - T_cold / T_0 = 1 - 278.15 / 298.15
ŋ_unav = 1 - 0.9349 = 0.0651 or 6.51%
```

**Avoidable irreversibility:**
```
ŋ_av = η_d - ŋ_unav = 0.1228 - 0.0651 = 0.0577
```

### Economic Calculations

**Installation cost (IC):**
```
IC = PEC × Installation factor = 85,000 × 1.65 = €141,750
```

**Present Worth Factor (PWF) for equipment:**
```
n = 20 years, i = 8%
PWF = [(1 + 0.08)^20 - 1] / [0.08 × (1 + 0.08)^20]
PWF = 4.66095
```

**Present Worth of Equipment Cost:**
```
PEC_PWF = PEC × PWF = 85,000 × 4.66095 = €397,130.75
```

**Annual Capital Recovery Factor (CRF):**
```
CRF = i / [PWF × (1 + i)^n] = 0.08 / [4.66095 × (1.08^20)]
CRF = 0.08 / 23.471
CRF = 0.003413
```

**Annual Equipment Cost (AEC):**
```
AEC = CRF × PEC_PWF = 0.003413 × 397,130.75 = €1,352.68/year
```

**Installation Cost (IC):**
```
IC = 141,750/year
```

**Annual Operating Cost (AOC) — Electricity:**
```
Electricity cost = Q_cold × 0.12 EUR/kWh = 500 × 0.12 = €60/year
```

**Maintenance Cost Factor:**
```
MCF = 4% of TCI/year = 0.04 × (141,750 + 85,000) = 0.04 × 226,750 = €9,070/year
```

**Total Annual Cost (TAC):**
```
TAC = AEC + AOC + MC = 1352.68 + 60 + 9070 = €10,482.68/year
```

**Annual Energy Cost:**
```
Energy cost = Q_cold × 0.12 EUR/kWh = 500 × 0.12 = €60/year
```

**Thermodynamic Cost (TCI) — Avoidable Exergy-Based:**
```
TCI = IC / η_d = 141,750 / 0.8739 = €161,980.26
```

**Avoidable Annual Cost Reduction (ΔC):**
```
ΔC = TCI × ŋ_av = 161,980.26 × 0.0577 = €9,403.05/year
```

### Ż-Method Calculation

**Ż-factor:**
```
Ż = (AEC + MC) / TCI = (13,526.88 + 9,070) / 161,980.26
Ż = 22,596.88 / 161,980.26 = 0.1394 or 13.94%
```

**Optimization Priority:**
Since Ż < 40% and the equipment is at a moderate efficiency level (COP = 4.2), optimization efforts should focus on:

1. **Component Upgrade:** Replace with a more efficient compressor stage, e.g., upgrading from a single-speed to variable-speed centrifugal compressor.
2. **Heat Recovery:** Install a condenser heat recovery module to utilize the residual 60–75°C hot water for process heating.
3. **Insulation Optimization:** Reduce refrigerant oil and lubrication losses with improved insulation and shell design.

### Summary Table

| Parameter            | Value                       |
|----------------------|----------------------------|
| Cooling capacity (kW) | 500                        |
| COP                  | 4.2                        |
| Evaporator temp (K)   | 278.15                     |
| Condenser temp (K)    | 308.15                     |
| Electrical input kW   | 119.05                     |
| Cold exergy output kW | 33.67                      |
| Hot exergy rejection kW | -21.05                    |
| Unavoidable kW       | 11.49                      |
| Avoidable kW         | 3.18                       |
| TCI (exergy-based)   | €161,980.26                |
| CRF                  | 0.003413                   |
| AEC/year             | €1,352.68                  |
| Installation cost    | €141,750                   |
| Interest rate        | 8%                         |
| Equipment lifetime   | 20 years                   |
| Annual op. hours     | 6,000 h/year               |
| Electricity price EUR/kWh | 0.12                      |
| Maintenance factor   | 4% of TCI/year             |
| Ż-factor (current)    | 13.94%                     |

### Recommended Action

Investigate compressor stage upgrade and/or condenser heat recovery installation to reduce annual energy cost by approximately €9,403/year with minimal equipment investment.

**F-factor:** 2.77
**R-factor:** 16.12

Upgrade priority recommended for significant TCI reduction potential.