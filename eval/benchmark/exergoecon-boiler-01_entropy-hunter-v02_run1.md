# exergoecon-boiler-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 83.1s | Checks: 4/6

## Exergoeconomic (SPECO) Analysis: Boiler (Water-Tube Steam Boiler, Natural Gas)

### Operating Conditions
- Thermal capacity: 2000 kW
- Fuel: natural gas
- Pressure: 12 bar
- Stack temperature: 190°C
- Feedwater temperature: 80°C
- Thermal efficiency: 87%
- Operating mode: full_load

---

### 1. Energy Balance (LHV basis)

**Step 1: Fuel energy input**

```
Q_in = Q_useful / η_th
Q_in = 2000 kW / 0.87
Q_in = 2298.85 kW
```

**Step 2: Fuel energy (LHV) consumption**

Natural gas LHV: 36.0 kJ/kWh

```
Fuel_kWh = Q_in / LHV
Fuel_kWh = 2298.85 / 0.36
Fuel_kWh = 6385.70 kWh
Fuel_kcal = 6385.70 × 1.055
Fuel_kcal = 6744.70 kcal

Fuel_MJ = 2298.85 / 0.239
Fuel_MJ = 9603.38 MJ
```

**Step 3: Useful thermal output**

```
Q_useful = 2000 kW
```

---

### 2. Exergy Balance

#### Step A: Steam Properties at Operating Conditions

**Saturation temperature (12 bar):**
T_sat = 179°C → T_sat(K) = 452.15 K

**Feedwater at inlet (80°C, compressed liquid):**
T_fw = 353.15 K
P = 12 bar → P = 1200 kPa

From IAPWS-IF97 steam tables:
```
h_fw = 462.68 kJ/kg
s_fw = 1.4902 kJ/(kg·K)
```

**Steam at outlet (saturated, 12 bar):**
```
h_s = h_g = 2763.54 kJ/kg
s_s = s_g = 6.6855 kJ/(kg·K)
```

#### Step B: Energy-based Exergy Calculations

**Exergy of fuel input (chemical exergy):**
Ex_fuel = Q_in × (1 − η_th)

```
Ex_fuel = 2298.85 kW × (1 - 0.87)
Ex_fuel = 2298.85 × 0.13
Ex_fuel = 298.85 kW
```

**Exergy of thermal output:**
```
Ex_th_out = Q_useful × (T_sat / T₀ - 1)
Ex_th_out = 2000 × (452.15 / 298.15 - 1)
Ex_th_out = 2000 × 0.513
Ex_th_out = 1026 kW
```

**Exergy of fuel combustion:**
```
Ex_comb = Q_in × (1 − T_r / T₀)
T_r = 190°C = 463.15 K, T₀ = 298.15 K

Ex_comb = 2298.85 × (1 - 463.15 / 298.15)
Ex_comb = 2298.85 × 0.387
Ex_comb = 891.78 kW
```

**Exergy of feedwater:**
```
Ex_fw = (h_fw − h_fg + T₀ × (s_fw − s_fg))
s_fg = s_f(12 bar) − s_g(12 bar)
s_fg ≈ 0.6439 kJ/(kg·K)

Ex_fw = (462.68 − 0 + 298.15 × (1.4902 − 0.6439))
Ex_fw = 462.68 + 298.15 × 0.8463
Ex_fw = 462.68 + 252.75
Ex_fw = 715.43 kW
```

**Exergy of steam:**
```
Ex_steam = (h_s − h_fg + T₀ × (s_s − s_fg))
Ex_steam = (2763.54 − 0 + 298.15 × (6.6855 − 0.6439))
Ex_steam = 2763.54 + 298.15 × 6.0416
Ex_steam = 2763.54 + 1808.89
Ex_steam = 4572.43 kW
```

**Total exergy output:**
```
Ex_out = Ex_th_out + Ex_steam − (h_fw × s_fw)
Ex_out = 1026 + 252.75 − (462.68 × 1.4902)
Ex_out = 1026 + 252.75 − 693.54
Ex_out = 585.21 kW
```

**Total exergy input:**
```
Ex_in = Ex_fuel + Ex_comb + Ex_fw − (h_fw × s_fw)
Ex_in = 298.85 + 891.78 + 715.43 − (462.68 × 1.4902)
Ex_in = 298.85 + 891.78 + 715.43 − 693.54
Ex_in = 1222.52 kW
```

**Thermal exergy efficiency:**
```
η_ex_th = Ex_out / Q_useful
η_ex_th = 585.21 / 2000
η_ex_th = 0.293 or 29.3%
```

---

### 3. Exergy Analysis Summary

| Item | Value |
|------|-------|
| Q_in (kW) | 2298.85 |
| Q_useful (kW) | 2000 |
| η_th (%) | 87 |
| Ex_fuel (kW) | 298.85 |
| Ex_comb (kW) | 891.78 |
| Ex_fw (kW) | 715.43 |
| Ex_steam (kW) | 4572.43 |
| Ex_out (kW) | 585.21 |
| Ex_in (kW) | 1222.52 |
| η_ex_th (%) | 29.3 |
| Ex_waste (kW) | 637.31 |

---

### 4. Entropy Generation Minimization (EGM / Avoidable / Unavoidable)

**Step A: Total entropy generation**

```
Ṡ_gen = Q_in × (T₀/T_sat - η_th)
Ṡ_gen = 2298.85 × ((298.15/452.15) - 0.87)
Ṡ_gen = 2298.85 × (0.659 - 0.87)
Ṡ_gen = 2298.85 × (-0.211)
Ṡ_gen = -483.66 kW/K
```

**Step B: Avoidable / Unavoidable**

Avoidable fraction:

```
f_avoid = Q_in × (T₀/T_sat − η_th) × (Q_in − Q_useful) / Q_in²
f_avoid = 2298.85 × ((0.659 - 0.87) × (1 - 0.87))
f_avoid = 2298.85 × (-0.211 × 0.13)
f_avoid = 2298.85 × -0.0274
f_avoid = 63.33 kW
```

Unavoidable fraction:

```
f_unav = Q_in × (T₀/T_sat − η_th) × Q_useful / Q_in²
f_unav = 2298.85 × ((0.659 - 0.87) × 2000)
f_unav = 2298.85 × (-0.211 × 2000)
f_unav = 2298.85 × -422
f_unav = -963,490 kW
```

---

### 5. Economic Analysis (SPECO)

**Step A: Equipment Cost (PEC) → Installation Factor**

```
PEC = €145,000
Install factor = 1.80
TCI = PEC × Install factor
TCI = 145,000 × 1.80
TCI = €261,000
```

**Step B: Interest Rate (7%) — Capital Recovery Factor**

For a 25-year loan at 7%:

```
CRF_7pct_25y = PEC × r-factor(25yr, 7%)

r-factor(25yr, 7%) = A/P factor from interest tables
r-factor(25yr, 7%) ≈ 0.146

CRF_PEC = 145,000 × 0.146
CRF_PEC = €21,070/year
```

**Step C: Annual Fuel Cost**

```
Fuel cost (natural gas): 35 EUR/MWh → 0.035 kWh

Annual fuel consumption:
Fuel_kWh/year = Q_in × 8000 h/year
Fuel_kWh/year = 2298.85 × 8000
Fuel_kWh/year = 18,390,800 kWh

Fuel_cost_year = 18,390,800 × 0.035
Fuel_cost_year = €643,678.00
```

**Step D: Maintenance Cost**

Maintenance cost factor (3% of TCI):

```
Maint_cost_year = 0.03 × TCI
Maint_cost_year = 0.03 × 261,000
Maint_cost_year = €7,830/year
```

**Step E: Total Annual Cost (TAC):**

```
TAC = Fuel_cost + Maintenance_cost + CRF_PEC
TAC = 643,678.00 + 7,830.00 + 21,070.00
TAC = €672,578/year
```

**Step F: Annual Energy Cost (AEC):**

```
AEC = Fuel_cost / Q_useful × 100
AEC = (643,678 / 2000) × 100
AEC = 321.84 kWh/kWh × 100
AEC = 32.18 EUR/kWh
```

**Step G: CRF — Annualized Cost Factor**

```
CRF_TCI = TAC / TCI
CRF_TCI = 672,578 / 261,000
CRF_TCI = 2.579/year
```

**Step H: Ż (Szép) Index — Cost Improvement Priority**

```
Ż = Ex_in − Q_useful
Ż = 1222.52 − 2000
Ż = -777.48 kW
```

Since we are dealing with a natural gas boiler, the negative value of Ż indicates that the thermal output is already at the physical limit (natural gas combustion exergy input). Therefore, the focus should be on improving energy recovery from waste heat and reducing parasitic losses.

**Step I: Avoidable / Unavoidable Cost Split**

```
Avoidable annual cost:
  = f_avoid × TCI
  = 63.33 kW × 261,000
  = €16,578/year

Unavoidable annual cost:
  = f_unav × TCI
  = -963,490 kW × 261,000
  = 0 (physical law constraint)
```

---

### 6. Optimization Strategy

**Priority:**

1. **Radiation minimization:** Reduce radiation losses by insulating the boiler shell and exhaust stack.
2. **Flue gas recovery:** Install an economizer or waste heat boiler to recover sensible heat from flue gases at 190°C, increasing feedwater temperature.
3. **Combustion optimization:** Fine-tune combustion air/fuel ratio for higher flame temperatures (reduce excess air), improving chemical exergy capture.
4. **Blowdown minimization:** Reduce blowdown rate and treat condensate to reduce make-up water load.
5. **Stack economizer:** Install a stack-side economizer to preheat feedwater using the exhaust gas, reducing fuel consumption.

**Estimated Ż reduction (conservative):** 10% → 77.74 kW

**Expected TCI reduction:**
```
ΔTCI = CRF × ΔŻ
ΔTCI = 261,000 × 0.10
ΔTCI = €26,100/year
```

**Annual savings (savings = fuel cost share):**

```
Annual_savings = TCI × f_factor × η_fuel

f_factor = Ż / Q_useful
f_factor = -777.48 / 2000
f_factor = 0.3887

η_fuel = 1 − θ_th, so fuel share:
fuel_share = 0.65 × 0.13 (thermal to chemical)

Annual_savings = 672,578 × 0.3887 × 0.65 × 0.13
Annual_savings = 672,578 × 0.0314
Annual_savings = €21,096/year
```

**Investment payback period:**

```
Payback_period = Initial_investment / Annual_savings
Payback_period = 26,100 / 21,096
Payback_period ≈ 1.24 years

**F-factor (optimization priority):**
f_factor = 0.3887 — indicates significant potential for improvement.

**R-factor (investment value):**
R_factor = Annual_savings / CRF
R_factor = 21,096 / 21,070
R_factor ≈ 1.00

**Conclusion:**
The boiler is performing at the physical limit with fuel cost already minimized. However, significant exergy savings (77.74 kW) are achievable through economizer and radiation minimization measures. A focused retrofit strategy will achieve a quick payback period.

---

### Summary Table

| **Parameter** | **Value** |
|--------------|----------|
| Q_in (kW)     | 2,298.85 |
| Q_useful (kW) | 2,000.00 |
| η_th (%)      | 87       |
| Ex_fuel (kW)  | 298.85   |
| Ex_comb (kW)  | 891.78   |
| Ex_fw (kW)    | 715.43   |
| Ex_steam (kW) | 4,572.43 |
| Ex_out (kW)   | 585.21   |
| Ex_in (kW)    | 1,222.52 |
| η_ex_th (%)   | 29.3     |
| f_avoid (kW)  | 63.33    |
| f_unav (kW)   | -        |
| Ż (kW)        | -777.48  |

**Recommendation:** Implement radiation reduction measures and economizer installation to capture the large exergy potential from feedwater and flue gas recovery.

---

The analysis concludes with a clear roadmap for improvement based on detailed thermodynamic calculations, demonstrating that significant cost savings are achievable through targeted retrofits aimed at reducing heat loss and increasing overall system efficiency.