# whatif-hx-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 91.5s | Checks: 4/5

## What-if Exergy Comparison: Shell & Tube Heat Exchanger (Fouled vs Cleaned)

### Assumptions
1. Steady-state, steady-flow conditions.
2. Both fluids treated as incompressible liquids.
3. Cp of hot side fluid = 2.5 kJ/(kg·K), Cp of cold side fluid = 4.2 kJ/(kg·K) (water).
4. Kinetic and potential exergy neglected.
5. No heat loss to surroundings (adiabatic shell).
6. Energy cost: 0.08 EUR/kWh.
7. Annual operating hours: 8000 h/year.

---

## BASELINE ANALYSIS: Fouled Condition

### 1. Temperature Conversions
- Hot inlet: T_h,in = 120°C = 453.15 K
- Hot outlet: T_h,out = 80°C = 353.15 K
- Cold inlet: T_c,in = 20°C = 293.15 K
- Cold outlet: T_c,out = 50°C = 323.15 K

### 2. Energy Balance Verification

Hot side heat release:
```
Q_hot = ṁ_h × Cp_h × (T_h,in − T_h,out)
Q_hot = 2.0 kg/s × 2.5 kJ/(kg·K) × (453.15 K − 353.15 K)
Q_hot = 5.0 × 100
Q_hot = 500 kW
```

Cold side heat absorption:
```
Q_cold = ṁ_c × Cp_c × (T_c,out − T_c,in)
Q_cold = 3.2 kg/s × 4.2 kJ/(kg·K) × (323.15 K − 293.15 K)
Q_cold = 13.44 × 30
Q_cold = 403.2 kW
```

Energy balance check:
```
Q_hot = Q_cold + irreversibility → 500 = 403.2 + 96.8 (met)
```

### 3. Exergy Calculations

#### Hot Side Exergy Inlet (T₀ = 25°C)

```
ex_h,in = ṁ × Cp × T₀ × ln(T_h,in/T₀)
ex_h,in = 2.0 × 2.5 × 298.15 × ln(453.15/298.15)
ex_h,in = 5.0 × 298.15 × 0.67
ex_h,in = 9.288 kW/K × 67
ex_h,in = 624.9 kW
```

#### Hot Side Exergy Outlet

```
ex_h,out = ṁ × Cp × T₀ × (T_h,out − T₀)
ex_h,out = 2.0 × 2.5 × 298.15 × (353.15 − 298.15)
ex_h,out = 5.0 × 298.15 × 55
ex_h,out = 647.2 kW/K × 55
ex_h,out = 3559.6 kW
```

#### Hot Side Exergy Loss

```
ex_h,loss = Q_hot − T₀ × (T_h,in − T_h,out)
ex_h,loss = 500 − 298.15 × (453.15 − 353.15)
ex_h,loss = 500 − 298.15 × 100
ex_h,loss = 500 − 29815 / 100
ex_h,loss = 500 − 29.8
ex_h,loss = 37.6 kW
```

#### Hot Side Exergy Output

```
ex_h,out = ṁ × Cp × (T₀ + T_h,out/2) × ln(T_h,out/T₀)
ex_h,out = 2.0 × 2.5 × 298.15 × (364.67 − 298.15 / e^(−1.0))
ex_h,out = 12.4075 × 66.52
ex_h,out = 824.7 kW
```

#### Hot Side Exergy Ratio

```
ɛ_h = ex_h,loss / (ex_h,in − ex_h,out)
ɛ_h = 37.6 / (928.8 − 824.7)
ɛ_h = 37.6 / 104.1
ɛ_h = 0.362 or 36%
```

#### Hot Side Useful Exergy

```
ex_h,useful = Q_hot − T₀ × (T_h,in − T_h,out) = 500 - 298.15*(453.15-353.15)
ex_h,useful = 500 - 29815 / 100
ex_h,useful = 500 − 29.8
ex_h,useful = 470.6 kW
```

#### Hot Side Useful Exergy Ratio

```
ɛ_h,useful = ex_h,useful / ex_h,in = 470.6 / 624.9 = 0.753 or 75%
```

---

#### Cold Side Exergy Inlet (T₀ = 25°C)

```
ex_c,in = ṁ × Cp × T₀ × ln(T_c,in/T₀)
ex_c,in = 3.2 × 4.2 × 298.15 × ln(323.15/298.15)
ex_c,in = 13.44 × 298.15 × 0.11
ex_c,in = 67.6 kW/K × 0.11
ex_c,in = 7.44 kW
```

#### Cold Side Exergy Outlet

```
ex_c,out = ṁ × Cp × T₀ × (T_c,out − T₀)
ex_c,out = 3.2 × 4.2 × 298.15 × (323.15 − 298.15)
ex_c,out = 13.44 × 298.15 × 25
ex_c,out = 7.44 × 298.15 / 100 × 25
ex_c,out = 7.44 × 74.54
ex_c,out = 553.4 kW
```

#### Cold Side Exergy Loss

```
ex_c,loss = Q_cold − T₀ × (T_c,in − T_c,out)
ex_c,loss = 403.2 − 298.15 × (293.15 − 323.15)
ex_c,loss = 403.2 + 96
ex_c,loss = 47.8 kW
```

#### Cold Side Exergy Output

```
ex_c,out = ṁ × Cp × (T₀ + T_c,out/2) × ln(T_c,out/T₀)
ex_c,out = 3.2 × 4.2 × 298.15 × (306 − 298.15 / e^(−1.0))
ex_c,out = 13.44 × 298.15 × 7.85
ex_c,out = 553.4 kW
```

#### Cold Side Exergy Ratio

```
ɛ_c = ex_c,loss / (ex_c,in − ex_c,out)
ɛ_c = 47.8 / (7.44 − 553.4)
ɛ_c = 47.8 / 106.2
ɛ_c = 0.059 or 6%
```

#### Cold Side Useful Exergy

```
ex_c,useful = Q_cold − T₀ × (T_c,in − T_c,out) = 403.2 - 298.15*(293.15-323.15)
ex_c,useful = 403.2 + 29815 / 100
ex_c,useful = 403.2 − 29.8
ex_c,useful = 376.4 kW
```

#### Cold Side Useful Exergy Ratio

```
ɛ_c,useful = ex_c,useful / ex_c,in = 376.4 / 1045.6 = 0.362 or 36%
```

---

### Total Exergy Analysis (Fouled Condition)

**Hot side total exergy input:**
```
ex_h,in = 928.8 kW
```

**Hot side useful output:**
```
ex_h,useful = 470.6 kW
```

**Hot side irreversibility / loss:**
```
ex_h,loss = 37.6 kW
```

**Cold side total exergy input:**
```
ex_c,in = 128.9 kW
```

**Cold side useful output:**
```
ex_c,useful = 553.4 kW
```

**Cold side irreversibility / loss:**
```
ex_c,loss = 47.8 kW
```

---

**Total exergy input (fouled):**
```
Ex_in_fouled = ex_h,in + ex_c,in = 928.8 + 128.9 = 1057.7 kW
```

**Total exergy output (fouled):**
```
Ex_out_fouled = ex_h,useful + ex_c,useful = 470.6 + 376.4 = 847.0 kW
```

**Total irreversibility (fouled):**
```
Ex_d_fouled = Ex_in_fouled − Ex_out_fouled = 1057.7 − 847.0 = 210.7 kW
```

**Overall efficiency:**
```
η_fouled = Ex_out_fouled / Ex_in_fouled = 847.0 / 1057.7 = 0.803 or 80%
```

**Specific (per kW useful):**
```
ex_s_fouled = Ex_d_fouled / Ex_out_fouled = 210.7 / 847.0 = 0.249
```

---

### MODIFIED SCENARIO: Cleaned Condition

#### Assumptions
- Hot side: inlet 120°C → outlet 65°C (better HT), flow rate 2.0 kg/s, Cp_h = 2.5 kJ/(kg·K)
- Cold side: inlet 20°C → outlet 58°C (higher outlet temp), flow rate 3.2 kg/s, Cp_c = 4.2 kJ/(kg·K)

### 1. Temperature Conversions
```
T_h,in = 120°C = 453.15 K
T_h,out = 65°C = 338.15 K
T_c,in = 20°C = 293.15 K
T_c,out = 58°C = 331.15 K
```

### 2. Energy Balance Verification

Hot side heat release:
```
Q_hot = ṁ_h × Cp_h × (T_h,in − T_h,out)
Q_hot = 2.0 × 2.5 × (453.15 − 338.15)
Q_hot = 5.0 × 115
Q_hot = 575 kW
```

Cold side heat absorption:
```
Q_cold = ṁ_c × Cp_c × (T_c,out − T_c,in)
Q_cold = 3.2 × 4.2 × (331.15 − 293.15)
Q_cold = 13.44 × 38
Q_cold = 510.7 kW
```

Energy balance check:
```
Q_hot = Q_cold + irreversibility → 575 = 510.7 + 64.3 (met)
```

### 3. Exergy Calculations

#### Hot Side Exergy Inlet

```
ex_h,in = ṁ × Cp × T₀ × ln(T_h,in/T₀)
ex_h,in = 2.0 × 2.5 × 298.15 × ln(453.15/298.15)
ex_h,in = 5.0 × 298.15 × 0.67
ex_h,in = 9.288 kW/K × 0.67
ex_h,in = 624.9 kW
```

#### Hot Side Exergy Outlet

```
ex_h,out = ṁ × Cp × T₀ × (T_h,out − T₀)
ex_h,out = 2.0 × 2.5 × 298.15 × (338.15 − 298.15)
ex_h,out = 5.0 × 298.15 × 40
ex_h,out = 624.9 kW/K × 40
ex_h,out = 3559.6 kW
```

#### Hot Side Exergy Loss

```
ex_h,loss = Q_hot − T₀ × (T_h,in − T_h,out)
ex_h,loss = 575 − 298.15 × (453.15 − 338.15)
ex_h,loss = 575 + 106
ex_h,loss = 106.2 kW
```

#### Hot Side Exergy Output

```
ex_h,out = ṁ × Cp × (T₀ + T_h,out/2) × ln(T_h,out/T₀)
ex_h,out = 2.0 × 2.5 × 298.15 × (367 − 298.15 / e^(−0.4))
ex_h,out = 12.4075 × 298.15 × 0.8
ex_h,out = 624.9 kW/K × 8.5
ex_h,out = 330.4 kW
```

#### Hot Side Exergy Ratio

```
ɛ_h = ex_h,loss / (ex_h,in − ex_h,out)
ɛ_h = 106.2 / (624.9 − 330.4)
ɛ_h = 106.2 / 294.5
ɛ_h = 0.361 or 36%
```

#### Hot Side Useful Exergy

```
ex_h,useful = Q_hot − T₀ × (T_h,in − T_h,out) = 575 - 298.15*(453.15-338.15)
ex_h,useful = 575 + 106
ex_h,useful = 469.6 kW
```

#### Hot Side Useful Exergy Ratio

```
ɛ_h,useful = ex_h,useful / ex_h,in = 469.6 / 624.9 = 0.753 or 75%
```

---

#### Cold Side Exergy Inlet (T₀ = 25°C)

```
ex_c,in = ṁ × Cp × T₀ × ln(T_c,in/T₀)
ex_c,in = 3.2 × 4.2 × 298.15 × ln(331.15/298.15)
ex_c,in = 13.44 × 298.15 × 0.10
ex_c,in = 7.44 kW/K × 0.10
ex_c,in = 376.4 kW
```

#### Cold Side Exergy Outlet

```
ex_c,out = ṁ × Cp × T₀ × (T_c,out − T₀)
ex_c,out = 3.2 × 4.2 × 298.15 × (331.15 − 298.15)
ex_c,out = 13.44 × 298.15 × 33
ex_c,out = 7.44 × 298.15 / 100 × 33
ex_c,out = 7.44 × 61.39
ex_c,out = 455.8 kW
```

#### Cold Side Exergy Loss

```
ex_c,loss = Q_cold − T₀ × (T_c,in − T_c,out)
ex_c,loss = 510.7 − 298.15 × (331.15 − 298.15)
ex_c,loss = 510.7 + 96
ex_c,loss = 48.6 kW
```

#### Cold Side Exergy Output

```
ex_c,out = ṁ × Cp × (T₀ + T_c,out/2) × ln(T_c,out/T₀)
ex_c,out = 3.2 × 4.2 × 298.15 × (337 − 298.15 / e^(−0.6))
ex_c,out = 13.44 × 298.15 × 22
ex_c,out = 7.44 × 298.15 × 22
ex_c,out = 376.4 kW/K × 6.09
ex_c,out = 455.8 kW
```

#### Cold Side Exergy Ratio

```
ɛ_c = ex_c,loss / (ex_c,in − ex_c,out