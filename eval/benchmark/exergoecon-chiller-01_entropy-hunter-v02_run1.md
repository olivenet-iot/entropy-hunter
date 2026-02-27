# exergoecon-chiller-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 65.6s | Checks: 4/6

## Exergoeconomic (SPECO) Analysis: Centrifugal Chiller (COP = 4.2, Full Load)

### Assumptions
1. Steady-state, steady-flow operation.
2. COP = Q_cooling / W_compression = 4.2 (full load).
3. Evaporator temperature T_evap = 5°C → T_evap = 278.15 K.
4. Condenser temperature T_cond = 35°C → T_cond = 308.15 K.
5. Refrigerant: R-134a; properties derived from standard refrigeration cycle relations.
6. Cooling capacity Q_cooling = 500 kW (thermal load).
7. Electrical power consumption W_compression = Q_cooling / COP = 500/4.2 = 119.05 kW.
8. Exergy of electricity = electrical work → Ex_el = Ė_x = W_compression × 1 (pure work factor).
9. Heat rejection to environment: Q_reject = Q_cooling + W_compression (energy balance check follows).
10. Carnot COP for comparison: COP_Carnot,T_evap,T_cond = T_evap / (T_cond - T_evap) = 278.15 / (308.15 - 278.15) = 278.15/30.00 ≈ 9.27.
11. Kinetic and potential exergy changes negligible.

### Energy Balance Verification

```
Q_cooling      = 500.00 kW
Q_reject       = Q_cooling + W_compression
Q_reject       = 500.00 + 119.05 = 619.05 kW
COP            = 4.2

Verification: COP = Q_cooling / W_compression
W_compression  = Q_cooling / 4.2 = 119.05 kW (consistent)

Energy balance: ΣQ_in = 0 → Q_evap + Q_cond - Q_rejection = 0
Q_evap         = Q_cooling = 500.00 kW
Q_cond         = Q_reject = 619.05 kW

Consistent with stated COP and energy balance.
```

### Exergy Calculations

#### 1. Thermal (First-Law) Exergy Flows

**Ex_evap:** The exergy associated with the cooling effect at the evaporator temperature.

```
T_amb = 308.15 K
Ex_evap = Q_cooling × (T_amb / T_evap - 1)
Ex_evap = 500.00 × (308.15 / 278.15 - 1)
Ex_evap = 500.00 × (1.1046 - 1) = 500.00 × 0.1046
Ex_evap = 52.30 kW
```

**Ex_cond:** The exergy associated with heat rejection at the condenser temperature.

```
Ex_cond = Q_reject × (T_amb / T_cond - 1)
Ex_cond = 619.05 × (308.15 / 308.15 - 1)
Ex_cond = 619.05 × (1.0000 - 1) = 619.05 × 0
Ex_cond = 0 kW
```

**Carnot Exergy:**

```
Ex_Carnot = Q_cooling × (T_cond / T_evap - 1)
Ex_Carnot = 500.00 × (308.15 / 278.15 - 1)
Ex_Carnot = 500.00 × (1.1046 - 1) = 500.00 × 0.1046
Ex_Carnot = 52.30 kW
```

#### 2. Exergy of Compression

```
Ex_comp = Ė_x = W_compression = 119.05 kW
```

#### 3. Total Exergy Balance

```
Ex_in  = Ex_comp + Ex_evap (waste exergy in the cooling side is useful)
Ex_in  = 119.05 + 52.30 = 171.35 kW

Ex_out = Q_cooling (all goes into useful cooling exergy)

Exergy efficiency: η_ex = Ex_out / Ex_in
η_ex = 52.30 / 171.35 = 0.305 or 30.5%
```

#### 4. Carnot-Based Second-Law Benchmark

```
Carnot COP = T_evap / (T_cond - T_evap) = 9.27
Exergy coefficient: η_ex,Carnot = Q_cooling × (1 / COP_Carnot)
η_ex,Carnot = 500.00 × (1 / 9.27) = 54.33 kW

COP_ex = Ex_out / Ex_in = 52.30 / 119.05 = 0.439
```

### Economic Calculations

#### A. Total Capital Investment (TCI)

```
PEC  = €85,000
Installation factor: φ_inst = 1.65
TCI  = PEC × φ_inst = 85,000 × 1.65 = €140,250
```

#### B. Annual Interest Cost (AIC)

```
r   = 8% = 0.08
N   = 20 years

Present Worth Factor: PWF_20,8% = 1 / ((1 + r)^N - 1) = 1 / (1.08^20 - 1)
PWF_20,8% = 1 / (4.660957 - 1) = 1 / 3.660957
PWF_20,8% = 0.2737

AIC   = TCI × r × PWF_N,r
AIC   = 140,250 × 0.08 × 0.2737
AIC   = 140,250 × 0.0219
AIC   = €3,067.42/year
```

#### C. Annual Maintenance Cost (AMC)

```
AMC = 4% of TCI
AMC = 0.04 × 140,250 = €5,610.00/year
```

#### D. Annual Energy Cost (AEC)

```
Electricity cost: Ė_elec = W_compression = 119.05 kW
AEC   = Ė_elec × Ė_cost = 119.05 × 0.12 = €14.286/kWh
AEC   = 119.05 × 0.12 × 6000 h/year
AEC   = 119.05 × 720
AEC   = €85,692/year
```

#### E. Total Annual Cost (TAC)

```
TAC = AIC + AMC + AEC
TAC = 3,067.42 + 5,610.00 + 85,692
TAC = €94,369.42/year
```

#### F. Annual Revenue (AR) — Not Given

**For the sake of completeness:**

If a reference revenue value is provided (e.g., product saved cost), then:

```
Revenue = η_ex × Q_cooling × Ė_cost
Revenue = 0.439 × 500 × 0.12
Revenue = 0.439 × 60
Revenue = €26.34/hour

Annual Revenue: AR = 26.34 × 6000 = €158,040/year
```

#### G. Cost Performance Ratio (CRF)

```
CRF = TCI / TAC
CRF = 140,250 / 94,369.42 = 1.487 or 148.7%
```

### Ż-Analysis (Szilárd Measure)

```
Ż = AEC + AMC / TCI
Ż = 85,692 + 5,610.00 / 140,250
Ż = 85,692 + 0.03997 ≈ 85,692
```

### f-Factor

```
f_factor = AEC / Q_cooling = 85,692 / 500,000 = 0.171 kWh/kWh (efficiency degradation factor)
```

### r-Factor

```
r_factor = TCI / Q_cooling = 140,250 / 500,000 = 0.280 EUR/kW
```

### Optimization Strategy

**Current COP:** 4.2 (good performance for centrifugal at full load)
**COP_Carnot:** 9.27 → **LCOH:** 11.36 kJ/kWh (exergy basis)

**Strategy:**

1. **Upgrade to higher-efficiency R-134a compressor:** Target COP ≥ 5.0; expected LCOH drop by ~1.8–2.0 kJ/kWh.
   - Expected improvement: 5.0 → 4.2 = 16%
   - Estimated energy savings: 500 × (1 − 0.42/0.50) = 90 kW
   - Annual electricity cost reduction: 90 × 0.12 = €10,800

2. **Part-load performance optimization:** Verify part-load behavior; centrifugal chillers typically degrade at part load.
   - Install demand-based modulation (variable-speed drives) to reduce high-COP operation.

3. **Thermal recovery upgrade:**
   - Condenser water temperature reduction via economizer or heat recovery loop.
   - Recoverable waste heat for preheating, space heating, or absorption systems.

4. **Free cooling augmentation:** Install bypass or dry cooler for lower-temperature cooling (e.g., 12°C) when ambient is sufficiently cold; reduces compression work.

5. **Annual maintenance optimization:**
   - Regular cleaning, leak detection, compressor health checks.
   - Upgrade to high-efficiency fan motors and oil pumps.

### Summary Table

| Item               | Value            |
|--------------------|------------------|
| Q_cooling (kW)      | 500.00           |
| COP                | 4.2              |
| W_compression (kW)  | 119.05           |
| Ex_evap (kW)        | 52.30            |
| Ex_cond (kW)        | 0.00             |
| Ė_x                 | 119.05           |
| η_ex               | 43.9% (COP = 4.2) |
| η_ex,Carnot         | 52.30            |
| TCI (EUR)           | €140,250         |
| AIC (EUR/year)      | €3,067.42        |
| AMC (EUR/year)      | €5,610.00        |
| AEC (EUR/year)      | €85,692          |
| TAC (EUR/year)      | €94,369.42       |
| CRF                | 1.487            |
| Ż                  | 85,692           |
| f-factor (kWh/kWh)   | 0.171            |
| r-factor (EUR/kW)    | 0.280            |

**Energy savings potential:** 90 kW; **annual electricity cost reduction:** €10,800/year.

**Annualized investment savings:** With a target COP improvement of 4.2 → 5.0 and energy at 0.12 EUR/kWh:

```
ΔW_compression = 500 / 5 - 500 / 4.2
ΔW_compression = 100.00 - 119.05 = -19.05 kW

Annual energy savings: 19.05 × 6000 h/year = 114,300 kWh
Annual cost reduction: 114,300 × 0.12 = €13,716/year

Investment payback period (optimization cost ≈ 2% of TCI): 140,250 / 13,716 ≈ 10.2 years
```

**Actionable recommendation:** Begin with compressor efficiency upgrade to reduce AEC; follow up with part-load optimization and free cooling for additional savings.