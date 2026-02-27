# exergoecon-chiller-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 62.8s | Checks: 6/6

## Exergoeconomic (SPECO) Analysis: Centrifugal Chiller (Full Load)

### Assumptions
1. Steady-state, steady-flow operation.
2. Evaporator temperature T_cold = 5°C (68.15°K), corresponds to refrigerant-side evaporation temperature.
3. Condenser temperature T_hot = 35°C (308.15°K).
4. COP = Q_cooling / W_compressor = 4.2 (given).
5. Cooling capacity Q_cooling = 500 kW (full load).
6. Refrigerant: R-134a.
7. Kinetic and potential exergy changes are negligible.
8. No heat recovery from condenser rejection; waste heat is treated as dissipated to environment.
9. All temperatures are absolute (K).

### Step 1 — Basic Energy Calculations

**Compressor power input:**
```
W_comp = Q_cooling / COP
W_comp = 500 kW / 4.2
W_comp = 119.05 kW
```

**Condenser heat rejection:**
```
Q_cond = Q_cooling + W_comp
Q_cond = 500 kW + 119.05 kW
Q_cond = 619.05 kW
```

**Exergy of cooling (cold-side useful output):**
```
Ex_cold = Q_cooling × (T₀ / T_cold - 1)
Ex_cold = 500 kW × (298.15 K / 278.15 K - 1)
Ex_cold = 500 × (1.0634 - 1)
Ex_cold = 500 × 0.0634
Ex_cold = 31.7 kW
```

**Condenser exergy destruction:**
```
Ex_cond = Q_cond × (T₀ / T_cond - 1)
Ex_cond = 619.05 kW × (298.15 K / 308.15 K - 1)
Ex_cond = 619.05 × (0.9674 - 1)
Ex_cond = 619.05 × (-0.0326)
Ex_cond = -20.28 kW
```

Since the condenser rejection is at a higher temperature than T₀, this represents useful dissipation; however, we treat it as exergy destruction for the analysis:
```
Ex_cond = 619.05 × (1 / 308.15 - 1/298.15)
Ex_cond = 619.05 × (-0.000327)
Ex_cond = 0.204 kW
```

**Total entropy generation:**
```
Ṡ_gen = (Q_cooling / T₀) + (Q_cond / T₀) - (Q_cooling / T_cold) - (Q_cond / T_hot)
Ṡ_gen = ((500 / 298.15) + (619.05 / 298.15) - (500 / 278.15) - (619.05 / 308.15))
Ṡ_gen = (1.6748 + 2.0761 - 1.7922 - 2.0131)
Ṡ_gen = 0.9455 kW/K
```

**Exergy efficiency:**
```
η_ex = Ex_cold / Q_cooling
η_ex = 31.7 / 500
η_ex = 6.34%
```

**Condenser effectiveness (COP_chilled):**
```
COP_chilled = Q_cooling / (Q_cond - Q_cooling)
COP_chilled = 500 / (619.05 - 500)
COP_chilled = 500 / 119.05
COP_chilled = 4.20%
```

**Condenser approach temperature:**
```
ΔT_cold = T_cond - T_cold = 35°C - 5°C = 30 K
```

**Condenser effectiveness (COP_cond):**
```
COP_cond = Q_cooling / Q_cond
COP_cond = 500 / 619.05
COP_cond = 0.8072 or 80.7%
```

### Step 2 — Entropy Generation Minimization (EGM) Analysis

**Dominant mechanism identification:**
- Compressor power input → is the driver of entropy generation.
- Condenser effectiveness and approach temperature are secondary.

**Achievable COP improvement potential:** Given the current COP = 4.2, a typical centrifugal chiller can achieve up to ~5.0 with advanced controls and improvements. We aim for COP_target = 5.0.

**Energy savings from improved COP:**
```
Q_cooling_same_system = Q_cond / (1 + COP_comp)
Q_cooling_same_system = 619.05 kW / (1 + 4.2/3.87)  [COP_compressor for improvement]
Q_cooling_same_system = 619.05 / 1.71
Q_cooling_same_system = 361.96 kW

ΔQ_cooling = Q_cooling - Q_cooling_same_system
ΔQ_cooling = 500 - 361.96
ΔQ_cooling = 138.04 kW

Energy savings = ΔQ_cooling × (t_on / t_year)
Energy savings = 138.04 × (6000 / 8760)
Energy savings = 138.04 × 0.685
Energy savings = 94.1 kW

Annual energy cost saving: 94.1 kW × 0.12 EUR/kWh × 6000 h/year
Annual energy cost saving = 94.1 × 0.12 × 6000
Annual energy cost saving = 68,352 EUR/year

Investment payback period: TCI / annual savings
Assuming TCI calculated as usual (not yet known), we use the improvement factor.

### Step 3 — Economic Calculations

**Installation factor:**
```
TCI = PEC × IF
TCI = 85,000 × 1.65
TCI = 140,250 EUR
```

**Interest rate (equipment cost with interest):**
```
PEC_equipment = PEC + PEC × r × t_year / 360
PEC_equipment = 85,000 + 85,000 × 0.08 × 20
PEC_equipment = 85,000 + 136,000
PEC_equipment = 221,000 EUR
```

**Annual energy cost:**
```
C_op = Q_cooling × (t_on / t_year) × C_elec
C_op = 500 kW × (6000 / 8760) × 0.12 EUR/kWh
C_op = 500 × 0.685 × 0.12
C_op = 411 kW × 0.12
C_op = 49.32 kW
```

**Annual maintenance cost:**
```
C_maint = C_op × 4%
C_maint = 49.32 × 0.04
C_maint = 1.97 EUR/year
```

**Annual total cost (TC):**
```
TC = C_op + C_maint
TC = 49.32 + 1.97
TC = 51.29 EUR/year
```

**Annualized equipment cost:**
```
PEC_annual = PEC_equipment × r × t_year / (t_year - n)
PEC_annual = 221,000 × 0.08 × 360 / (360 - 20)
PEC_annual = 221,000 × 0.08 × 360 / 340
PEC_annual = 7597.97 EUR/year
```

**Total annualized cost:**
```
TAC = TCI × r + TC
TAC = 140,250 × 0.08 + 51.29
TAC = 11,220 + 51.29
TAC = 11,271.29 EUR/year
```

**Annual energy cost savings (optimization scenario):**
At COP 5.0:
```
Q_cooling_opt = Q_cond / (1 + COP_comp)
Q_cooling_opt = 619.05 kW / (1 + 4.2/3.87)
Q_cooling_opt = 619.05 / 1.71
Q_cooling_opt = 361.96 kW

Energy savings = 500 - 361.96
Energy savings = 138.04 kW

Annual energy cost saving: 138.04 × 0.12 × 6000
Energy cost saving = 138.04 × 72
Energy cost saving = 10,005.6 EUR/year
```

**CRF (Current Equipment Ratio):**
```
CRF = TCI / PEC_equipment
CRF = 140,250 / 221,000
CRF = 0.634
```

**F-factor:**
```
F_factor = CRF × (C_op + C_maint) / (PEC_equipment × r)
F_factor = 0.634 × 51.29 / (221,000 × 0.08)
F_factor = 0.634 × 51.29 / 17,680
F_factor = 0.634 × 0.0029
F_factor = 0.00184
```

** Ż (Szemeszthy) factor:**
```
Ż_factor = (C_op + C_maint) / TCI
Ż_factor = 51.29 / 140,250
Ż_factor = 0.000366
```

**R-factor:**
```
R_factor = 1 - CRF
R_factor = 1 - 0.634
R_factor = 0.366
```

### Step 4 — Optimization Strategy

Given the improvement potential from COP increase:
- Target: COP = 5.0 (achievable with advanced controls/variable speed compressor)
- Expected energy savings: ~27% of annual electricity cost
- Estimated annual energy savings: 138.04 kW × 6000 h/year × 0.27
- Estimated annual energy savings: 235,920.00 kWh → 235.92 MWh

**Estimated annual electricity cost reduction:**
```
Annual energy cost saving = 235,920 kWh × 0.12 EUR/kWh
Annual energy cost saving = 28,310.4 EUR/year
```

**Payback period calculation for COP improvement:**
```
COP_improvement_investment = PEC_equipment + TCI × r - PEC_equipment + (TCI / CRF) - TCI
COP_improvement_investment = 221,000 + 140,250 × 0.08 × 360/340

Improvement cost = COP improvement investment – baseline annual energy savings
Improvement cost = 194,075 - 28,310.4
Improvement cost = 165,764.6 EUR

Payback period = Improvement cost / Annual energy cost saving
Payback period = 165,764.6 / 28,310.4
Payback period = 5.86 years
```

**Conclusion:**
The centrifugal chiller at full load is operating with a relatively low COP (4.2). A targeted improvement to COP = 5.0 through advanced controls and/or variable speed technology would yield significant energy savings (~138 kW), annual cost reduction (over 23 kWh/year), and payback in ~6 years.

**Recommendation:** Prioritize upgrade to high-efficiency compressor or package with advanced controls for full-load improvement, resulting in substantial exergy gain and reduced TCI.

End of analysis.