# exergoecon-chiller-01
Model: entropy-hunter-v02
Time: 411.0s
Checks: 5/7

## Exergoeconomic (SPECO) Analysis: Centrifugal Chiller (R-134a, 500 kW Cooling)

### Operating Conditions
- **Cooling capacity:** Q_c = 500 kW
- **Evaporator temperature (T_evap):** 5°C → T_evap = 278.15 K
- **Condenser temperature (T_cond):** 35°C → T_cond = 308.15 K
- **COP:** COP = 4.2
- **Refrigerant:** R-134a
- **Operating mode:** Full load

### Step 1: Basic Calculations — Energy and Exergy

**Electric power input (W):**
```
W = Q_c / COP = 500 kW / 4.2 = 119.05 kW
```

**Condenser heat rejection (Q_cond):**
```
Q_cond = Q_c + W = 500 + 119.05 = 619.05 kW
```

**Carnot COP reference:**
```
COP_Carnot = T_evap / (T_cond - T_evap) = 278.15 / (308.15 − 278.15)
COP_Carnot = 278.15 / 30.00 = 9.27
```

**Exergy of cooling (Q_c ex):**
```
EX_cooling = Q_c × (T_evap - T₀) / T_evap
          = 500 kW × (278.15 K − 253.15 K) / 278.15 K
          = 500 × 0.09466
          = 47.33 kW
```

**Exergy of heat rejection (Q_cond ex):**
```
EX_rejection = Q_cond × (T_cond - T₀) / T_cond
            = 619.05 kW × (308.15 K − 253.15 K) / 308.15 K
            = 619.05 × 0.17994
            = 111.06 kW
```

**Total exergy output (exergy product):**
```
EX_product = EX_cooling − EX_rejection
           = 47.33 kW − 111.06 kW
           = −63.73 kW

Since this value is negative, it indicates an error in the reference temperature assumption or calculation. In a centrifugal chiller with R-134a:
  - Q_cooling = 500 kW at T_evap = 278 K
  - Q_condenser = ~619 kW at T_cond = 308 K

Using the correct approach for exergy of cooling and rejection:

```
EX_cooling = Q_c × (T₀/T_evap) = 500 × (298.15/278.15)
           = 500 × 1.0694
           = 534.7 kW

EX_rejection = Q_cond × (T_cond − T₀)/(T_cond)
            = 619.05 × (308.15/298.15) − 619.05
            = 619.05 × 1.0337 − 619.05
            = 640.12 − 619.05
            = 21.07 kW

EX_product = 534.7 − 21.07 = 513.63 kW
```

**Thermal efficiency:**
```
η_th = Q_c / Q_gen = 500 / 119.05 = 4.20 (COP)
```

**Second-law efficiency:**
```
η_II = EX_product / Q_gen = 513.63 kW / 119.05 kW
     = 4.34 (or as COP_ex = 4.34)
```

### Step 2: Entropy Generation Calculation

**Generator:**
```
Gen = Q_gen × (T₀/T_evap − T₀/T_cond) + Q_c × (1/Δ_T_cool − 1/Δ_T_cond)
Gen = 119.05 × ((298.15 / 278.15) − (298.15 / 308.15)) + 500 × (1/(6 K) − 1/(30.0 K))
Gen = 119.05 × (1.0694 − 0.9670) + 500 × (0.1667 − 0.0333)
Gen = 119.05 × 0.1024 + 500 × 0.1334
Gen = 12.18 + 66.70
Gen = 78.88 kW/K
```

**Entropy generation ratio:**
```
N_s = Gen / (T_evap × η_II)
N_s = 78.88 / (253.15 × 4.34)
N_s = 78.88 / 1096.9
N_s = 0.0719
```

### Step 3: Cost Analysis — PEC → TCI → CRF

**Installation factor (equipment cost):**
```
PEC_inst = PEC × Installation_factor = 85,000 × 1.65 = €140,250
```

**Interest rate annualization:**
```
IRR = (P/F) / Year = (1 − Discount_factor)^−1
For TCI calculation at end-of-life:
Discount_factor = PEC_inst × r / (e^(r×n) − 1)
Where r is interest rate, n is equipment lifetime.
PEC_inst = 85,000 → Interest rate 8%, 20-year loan
PEC_inst = A × (P/A, 8%, 20) + P × (P/F, 8%, 20)
```

**Loan repayment:**
```
A = PEC_inst / (P/A, 8%, 20) = 140,250 / 9.818
A = 14,265.73

Principal repayment over 20 years:
P = A × (F/P, 8%, 20)
P = 14,265.73 × 4.661
P = 66,918.76

Total interest paid: Interest = Total payment − Principal
Interest = 140,250 − 66,918.76
Interest = 73,331.24

TCI (total cost of installation):
TCI = PEC_inst + Interest
TCI = 140,250 + 73,331.24
TCI = €213,581.24
```

**Annual energy cost:**
```
Energy_cost = Q_gen × Energy_price
Energy_cost = 119.05 kW × 0.12 EUR/kWh × 6000 h/year
Energy_cost = 14.286 kWe × 720 kWh
Energy_cost = 10,317.12 kW × year × €/kWh
Energy_cost = 10,317.12 EUR/year
```

**Annual maintenance cost:**
```
Maintenance = TCI × Maintenance_factor
Maintenance = 213,581.24 × 0.04
Maintenance = 8,543.25 EUR/year
```

**Annualized equipment cost (using interest rate method):**
```
A_eq = PEC / P/A factor
P/A, 8%, 20 = 9.818
A_eq = 140,250 / 9.818
A_eq = 14,263.73 EUR/year
```

**Annual total cost (SPECO):**
```
Ż = Energy_cost + Maintenance + Interest
Interest = (PEC_inst − Principal) × r
Interest = (140,250 − 66,918.76) × 0.08
Interest = 73,331.24 × 0.08
Interest = 5,866.50 EUR/year

Ż = 10,317.12 + 8,543.25 + 5,866.50
Ż = 24,726.87 EUR/year
```

**CRF (Cost Reduction Factor):**
```
Without baseline: CRF = 1.0 (benchmark is TCI)
Baseline comparison needed for actual improvement factor.
```

### Step 4: Optimization Recommendation

Current COP: 4.2 → Exergy efficiency: 513.63 / 119.05 = 4.34

**Benchmark:** For R-134a centrifugal chillers, a well-designed system can achieve ~5–7% improvement in exergy-to-work ratio over baseline (e.g., 4.2 → 4.5).

**Action:**
- **Component upgrades:** Check pump/motor efficiency improvements.
- **Blade optimization:** Review compressor blade geometry for improved isentropic efficiency.
- **Heat recovery:** Consider condenser-side heat recovery to increase overall thermal exergy.
- **Variable frequency drive (VFD):** Install VFD on compressors/pumps for part-load efficiency improvement.

### Step 5: Ż → Ċ_D calculation

For the current system with TCI = €213,581.24 and annual operating cost:

```
Ż = 24,726.87 EUR/year
```

**Annual energy savings (Ż_s):**
```
Assuming improvement factor for baseline comparison: e.g., 5% improvement in exergy efficiency leads to η_II improvement.

For a 1% exergy increase:
ΔCOP = 4.2 × 0.01 = 0.042
Energy_saved = Q_gen × ΔCOP
            = 119.05 kW × 0.042
            = 5.00 kW

Annual energy savings: Ċ_D = 5.00 kW × 6000 h/year
                       = 30,000 kWh/year

Energy cost reduction:
C_D = 30,000 × 0.12 EUR/kWh
C_D = 3,600 EUR/year
```

** Ż_s / Ċ_D ratio:**
```
Ratio = Ż / Ċ_D
Ratio = 24,726.87 / 3,600
Ratio = 6.87 EUR/kWh
```

**f-factor (energy-to-cost ratio):**
```
f_factor = Q_gen / Ż
f_factor = 119.05 kW / 24,726.87 × 0.12
f_factor = 119.05 / 2967.23
f_factor = 0.0400
```

**r-factor (efficiency-to-cost ratio):**
```
r_factor = η_II / Ż
r_factor = 4.34 / 24,726.87 × 0.12
r_factor = 4.34 / 2967.23
r_factor = 0.00146
```

### Step 6: Optimization Strategy Summary

**Current baseline:** TCI = €213,581.24; Ż = 24,726.87 EUR/year; f-factor = 0.0400; r-factor = 0.00146

**Improvement target:** For a competitive centrifugal chiller (e.g., 4.3 → 5.0 COP):

- **Achievable improvement:** 2% increase in COP (COP = 4.2 × 1.02 = 4.30)
- **Annual energy savings estimate:** 5.00 kW × 6000 h/year = 30,000 kWh
- **Energy cost reduction:** 30,000 × 0.12 EUR/kWh = €3,600
- **Annualized savings (after interest):** 3,600 / 8% = 45,000 EUR/year

**Payback period:**
```
Payback_period = TCI_equipment_cost / Annual_savings
Payback_period = 213,581.24 / 36,000
Payback_period ≈ 5.93 years
```

### Step 7: Recommendation

**Action recommendation:** Upgrade compressors/pumps and implement blade optimization to achieve the targeted COP improvement. The system can deliver significant energy cost reductions within a reasonable payback period.

By improving the exergy efficiency from 4.2 → 4.5, we increase annual savings by ~10% on investment of equipment upgrade cost (e.g., €6–8/kW for R-134a centrifugal).

**Action plan:**
1. **Baseline measurement:** Measure current COP and energy consumption.
2. **Benchmarking:** Compare with industry best practices at 500 kW capacity.
3. **Part-load analysis:** Perform part-load efficiency review (e.g., with CHPD mode consideration).
4. **Component upgrade procurement:** Quote for compressor/pump/condenser upgrades.
5. **Installation and commissioning plan:** Establish project timeline and budget.

**Expected Ż reduction after optimization:** 2–3% improvement in COP → 10–15% annual savings, translating to ~€2600–4200/year.