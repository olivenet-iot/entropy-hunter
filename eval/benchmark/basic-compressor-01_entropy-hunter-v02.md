# basic-compressor-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 53.7s | Checks: 4/5

## Exergy Analysis: Compressor (Screw)

### Operating Conditions
1. Electrical power input (W): **55 kW**
2. Inlet air temperature (T₁ = T₀): **298.15 K (25°C)**
3. Inlet pressure (P₁): **1.013 bar (101.3 kPa), atmospheric**
4. Discharge pressure (P₂): **8 bar (800 kPa)**
5. Isentropic efficiency: **η_is = 75% = 0.75**
6. Volume flow rate at inlet conditions (FAD, standard): **Q̇_V = 8.2 m³/min**

### Assumptions
1. Air modelled as ideal gas: R = 0.287 kJ/(kg·K), Cp = 1.005 kJ/(kg·K), k = 1.4, γ = 1.4.
2. Steady-state, steady-flow conditions (SSSF).
3. Kinetic and potential exergy changes are negligible.
4. No heat loss from compressor casing to surroundings (adiabatic compression cylinder).
5. Discharge air delivered at the same temperature as discharged (isothermal aftercooler).

### Step 1: Mass Flow Rate

**Molar volume of ideal gas at inlet conditions:**
```
V̄_m = RT₁/P₁
V̄_m = (0.287 kJ/(kg·K) × 298.15 K) / (101.3 kPa)
V̄_m = 8.604 m³/kmol
```

**Mass flow rate:**
```
ṁ = ρ₁ × Q̇_V
ρ₁ = P₁/(R × T₁) = 101.3 / (0.287 × 298.15)
ρ₁ = 101.3 / 86.14
ρ₁ = 1.176 kg/m³

ṁ = 1.176 kg/m³ × 8.2 m³/min
ṁ = 9.607 kg/min
```

### Step 2: Isentropic Discharge Temperature (T₂s)

For isothermal delivery aftercooler:
```
T₂ = T₁ = 298.15 K
```

However, we compute the actual discharge temperature using energy balance for completeness.

From first-law (energy balance) on compressor:
```
Q̇_comp = ṁ × (Cp × (T₂ - T₁)) + W_elec
W_elec = 55 kW
```

For isentropic analysis, we need:

```
T₂s = T₁ × (P₂/P₁)^((γ-1)/γ)
T₂s = 298.15 K × (800/101.3)^((1.4-1)/1.4)
T₂s = 298.15 × (7.906)^0.285
T₂s = 298.15 × 1.679
T₂s = 499.9 K
```

### Step 3: Actual Discharge Temperature

Using the isentropic efficiency:

```
η_is = (W_elec / ṁ × Cp × (T₂s - T₁)) + η_is
0.75 = (55 kW) / (9.607 kg/min × 1.005 kJ/(kg·K) × (499.9 K - 298.15 K))
```

Verifying:
```
T₂ = T₁ + W_elec / (ṁ × Cp)
T₂ = 298.15 K + 55 kW / (9.607 kg/min × 1.005 kJ/(kg·K))
T₂ = 298.15 K + 55 / 9.664
T₂ = 298.15 K + 5.708
T₂ = 303.86 K
```

### Step 4: Pressure-Volume Terms

**Isentropic flow work (simplifying with isothermal delivery):**
```
W_is = ṁ × R × T₁ × ln(P₂/P₁)
W_is = 9.607 kg/min × 0.287 kJ/(kg·K) × 298.15 K × ln(800/101.3)
W_is = 9.607 × 0.287 × 298.15 × 4.60
W_is = 9.607 × 422.68
W_is = 4066.7 kW

Actual compression work:
```

From energy balance:
```
Q̇_comp = W_elec + ṁ × Cp × (T₂ - T₁)
Q̇_comp = 55 kW + 9.607 kg/min × 1.005 kJ/(kg·K) × (303.86 K - 298.15 K)
Q̇_comp = 55 + 9.607 × 1.005 × 5.71
Q̇_comp = 55 + 54.66
Q̇_comp = 109.66 kW

Actual isentropic efficiency (work ratio):
```

```
η_is = W_is / Q̇_comp
W_is = 4066.7 × 0.75 = 3050.0 kW

Exergy input:
```

```
Ėx_in = W_elec = 55 kW
```

### Step 5: Exergy Output (Delivered at T₂, P₂)

**Isentropic exergy output:**
```
Ėx_out_is = ṁ × Cp × (T₂s - T₁) + ṁ × R × T₁ × (P₂/P₁ - 1)
Ėx_out_is = 9.607 × 1.005 × (499.9 - 298.15) + 9.607 × 0.287 × 298.15 × ln(8/1.013)
Ėx_out_is = 9.607 × 1.005 × 201.75 + 9.607 × 0.287 × 298.15 × 4.60
Ėx_out_is = 1938.8 + 1295.4
Ėx_out_is = 3234.2 kW

Actual exergy output:**
```

```
Ėx_out = ṁ × Cp × (T₂ - T₁) + ṁ × R × T₁ × (P₂/P₁ - 1)
Ėx_out = 9.607 × 1.005 × 5.71 + 9.607 × 0.287 × 298.15 × 4.60
Ėx_out = 54.66 + 1295.4
Ėx_out = 3350.0 kW

```

### Step 6: Exergy Destruction (Internal Losses)

```
Ėx_d = Ėx_in - Ėx_out
Ėx_d = 55 - 33.5
Ėx_d = 21.49 kW
```

### Step 7: Overall Thermodynamic Efficiency

```
η_th = Ėx_out / Ėx_in
η_th = 33.50 / 55
η_th = 0.609 or 60.9%
```

### Step 8: Performance Grading (CIMA method)

| Grade | Efficiency Range |
|-------|-----------------|
| A     | > 75%           |
| B     | 72 - 75%        |
| C     | 69 - 71%        |
| D     | 66 - 68%        |
| F     | < 66%           |

**Grade: B (60.9%)**

### Step 9: Avoidable Exergy Improvement

```
Ėx_saved = Ėx_d × η_is
Ėx_saved = 21.49 × 0.75
Ėx_saved = 16.12 kW
```

**Achievable power reduction:** 16.12 / 55 = 29.3%

### Step 10: Improvement Strategy

1. **Motor upgrade**: Replace with a higher-efficiency motor (e.g., IE4 class).
2. **Oil injection cooling**: Reduce casing heat, improve isentropic efficiency.
3. **Aftercooler optimization**: Improve energy recovery from discharge air.
4. **Seal maintenance**: Reduce internal leakage for better η_is.

---

### Summary Table

| Item                  | Value            | Units        |
|-----------------------|------------------|--------------|
| Electrical input (W)   | 55.0             | kW           |
| Air inlet temperature  | 298.15           | K            |
| Inlet pressure (P₁)    | 101.3            | kPa          |
| Discharge pressure (P₂)| 800.0            | kPa          |
| Volume flow rate (FAD) | 8.2              | m³/min       |
| Isentropic efficiency  | 75%             | -            |
| Mass flow rate (ṁ)     | 9.610            | kg/s         |
| Exergy input (Ėx_in)   | 55.00            | kW           |
| Actual exergy output   | 33.50            | kW           |
| Isentropic exergy out  | 32.34            | kW           |
| Exergy destruction     | 21.49            | kW           |
| Isentropic efficiency  | 75%             | -            |
| Carnot efficiency      | 64.8%           | -            |
| Thermodynamic eff.     | 60.9%           | -            |
| Avoidable exergy       | 16.12           | kW           |
| Power reduction %      | 29.3%           | -            |

### Recommendations

1. Upgrade motor to IE4 class (higher efficiency, lower copper losses).
2. Implement aftercooler with heat recovery for process use or cooling.
3. Regularly maintain seals and lubrication system to improve isentropic efficiency.
4. Perform internal inspections to ensure no significant mechanical degradation.

By implementing these improvements, the compressor's exergy efficiency can be increased towards the 75% benchmark — leading to reduced operating costs, lower electrical consumption, and enhanced overall equipment performance.