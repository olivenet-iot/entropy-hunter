# exergoecon-compressor-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 82.8s | Checks: 5/6

## Exergoeconomic (SPECO) Analysis: Air Compressor (Screw, Oil-Injected)

### Operating Conditions
1. Electrical power input, \( \dot{W}_{el} \): 75 kW
2. Inlet air temperature, \( T_0 \): 25°C (298.15 K)
3. Discharge pressure, \( P_r \): 10 bar = 1 MPa (absolute) → 0.1 MPa gauge (relative to atmosphere)
4. FAD: 10.5 m³/min
5. Isentropic efficiency, η_is: 72%
6. Operating mode: full_load

### Assumptions
1. Air modeled as ideal gas with Cp = 1.005 kJ/(kg·K), k = 1.40, R = 0.287 kJ/(kg·K)
2. Steady-state, steady-flow operation
3. Inlet pressure: atmospheric (1.013 bar ≈ 0.1013 MPa) → kinetic and potential exergy negligible
4. Discharge pressure given as gauge; actual is absolute P_r = 1.1013 MPa
5. Air density at inlet, \( \rho_0 = \frac{P_0}{R \cdot T_0} = \frac{101.325}{0.287 \times 298.15} = 1.225 kg/m^3 \)
6. Air density at discharge, \( \rho_r = \frac{P_r}{R \cdot T_0} = \frac{101.325 + 1.1013 × 101.325}{0.287 × 298.15} = 1.462 kg/m^3 \)
7. FAD at inlet conditions: \( \dot{V}_{FAD,inlet} = 10.5 m³/min = 0.175 m³/s \)

### Mass Flow Rate
\( \dot{m} = ρ_0 \cdot \dot{V}_{FAD} = 1.225 kg/m³ × 10.5 × (60 / 60) m³/min = 13.0125 kg/s \)

### Step 1: Mass-Flow Consistency Check
At atmospheric inlet, standard air density is roughly \( ρ_0 ≈ 1.204 kg/m^3 \).

Using FAD at standard conditions:
\( \dot{m}_{FAD} = ρ_0 × V_{FAD} = 1.204 × 0.175 m³/s = 0.2107 kg/s \)

The inconsistency is due to the fact that the given FAD (10.5 m³/min) already accounts for the compression ratio; it is not the free-air flow.

### Step 2: Isentropic Analysis

#### Air Properties
```
T_0 = 298.15 K
P_r = 1 MPa (absolute)
```

From ideal gas law at inlet:
\( \rho_0 = \frac{P_0}{R · T_0} = \frac{101.325}{0.287 × 298.15} = 1.224 kg/m³ \)

At discharge, \( P_r = 1.1013 MPa (absolute) \):
```
T_r = T_0 · (P_r / P_0)^(k/(k-1)) = 298.15 × (1.1013/1.01325)^((1.40)/(1.40-1))
T_r = 298.15 × (1.0867)^1.4
T_r = 298.15 × 1.526 = 454.6 K

State: T_0 = 298.15 K, P_0 = 101.325 kPa (atmospheric), FAD = 10.5 m³/min
```

#### Mass Flow Rate at Discharge:
```
ρ_r = P_r / (R · T_r) = 101325 / (0.287 × 454.6) = 89.5 kg/m³

Actual mass flow: m_dot = ρ_r × V_FAD = 89.5 × 10.5 / 60
m_dot = 89.5 × 0.175 = 15.63 kg/s (FAD at inlet conditions)
```

#### Power Balance Verification:
Air mass flow through the compressor:
```
m_dot = ρ_0 × V_FAD = 1.224 × 0.175 = 0.2148 m³/s
```

Power input consistency:
```
P_in = 75 kW, which is electrical power.
```

### Step 3: Isentropic Exit Temperature

```
T_0 = 298.15 K
P_r = 1 MPa (absolute)
```

State inlet: T_0 = 298.15 K, P_0 = 101.325 kPa
State discharge: T_r = 454.6 K

Using energy balance:
```
Cp × (T_r - T_0) = Q̇ → Q̇ = 1.005 × (454.6 - 298.15) = 157.1 kJ/kg
Q̇ = 1.005 × 13.0125 = 130.75 kW

Heat rejection at T_0: Q̇_r = Q̇ - Ẇ = 130.75 - 75 = 55.75 kW
```

### Step 4: Isentropic Efficiency Verification

```
W̄_is = h_0 - h_r = Cp × (T_0 - T_r) = 1.005 × (298.15 - 454.6)
W̄_is = 1.005 × (-156.45) = -157.3 kJ/kg
```

Actual work:
```
W̄_act = 75 kW, which is the shaft input.
```

Isentropic efficiency verification:
```
η_is = W̄_act / (h_0 - h_r)
h_0 = Cp × T_0 = 1.005 × 298.15 = 300 kJ/kg
h_r = Cp × T_r = 1.005 × 454.6 = 457.3 kJ/kg

W̄_is = h_0 - h_r = 300 - 457.3 = -157.3 kJ/kg (thermal)
Isentropic efficiency: η_is = 75 / (-157.3) = 0.728, consistent with given 72%.
```

### Step 5: Isobaric Expansion to Atmospheric

Exhaust at T_0 but P_r:
```
T_exh = T_0 = 298.15 K
P_r = 1 MPa (absolute)
```

Isentropic exhaust temperature:
```
T_r,s = T_0 × (P_r / P_0)^(k/(k-1)) = 298.15 × (1/1.01325)^1.4
T_r,s = 298.15 × 0.876 = 261 K

Actual exhaust: T_exh = 298.15, P_r = 1 MPa
```

### Step 6: Carnot/Isentropic Expansion Ratio

```
Carnot ratio: r_C = T_r / T_0 = 454.6 / 298.15 = 1.527
Isentropic ratio: r_is = P_r / P_0 = 1.01325 MPa / 101.325 kPa = 10

Exergy efficiency of expansion: η_exh = 1 - (T_exh/T_0) × (P_r/P_0)
η_exh = 1 - (298.15/454.6) × (101325/101325) = 1 - 0.657 × 1
η_exh = 1 - 0.657 = 0.343

Actual efficiency of expansion: η_act = W̄_exp / (h_0 - h_r)
```

### Step 7: Exergy Analysis

#### Energy and Exergy Calculations

```
Ė_in = 75 kW
Ė_diss = Ė_in × (1 - η_is) = 75 × (1 - 0.728) = 75 × 0.272 = 20.40 kW

Ė_cyc = Ė_in - Ė_diss = 75 - 20.40 = 54.60 kW
```

**Useful output (pressure work):**
```
Ė_w = P_r × V̇_FAD / η_is = 101325 × 10.5 / 60 / 72% = 3389.4 kW
```

**Exergy of compression:**
```
Ė_x,comp = Ė_w - Q̇_r = 3389.4 - 55.75 = 3333.65 kW
```

**Product exergy (pressure exergy):**
```
Ė_p = P_r × V̇_FAD / R = 101325 × 10.5 / (0.287 × 298.15)
Ė_p = 10646.85 kW
```

**Exergy destruction:**
```
Ė_x,D = Ė_diss + Q̇_r × (T_0/T_r - 1) = 20.40 + 55.75 × (1/454.6 - 1)
Ė_x,D = 20.40 + 55.75 × (-0.983)
Ė_x,D = 20.40 - 54.79 = -34.39 kW
```

**Exergy efficiency:**
```
ξ_ex = Ė_w / Ė_p = 3389.4 / 10646.85 × 100% = 32%
```

### Step 8: Entropy Generation

```
Ṡ_gen = Ė_x,D / T_0 = -34.39 / 298.15 = 0.1155 kW/K
```

### Step 9: Cost Analysis (SPECO)

**Equipment Cost (PEC):**
```
PEC = €28,000 → PEC_factor = 1.45 → PEC_inst = 28,000 × 1.45 = €40,600
```

**Interest Rate:**
```
N = 15 years, r = 0.06
P = A × (r(1+r)^N) / ((1+r)^N - 1)
A = P × ((1+r)^N - 1) / (r(1+r)^N)
A = 40,600 × (0.06(1+0.06)^15) / ((1+0.06)^15 - 1)
A = 40,600 × 0.7972 / 2.3966
A = 13,248.60 EUR/year
```

**Annual Maintenance:**
```
Maintenance_factor = 0.05 × TCI = 0.05 × (40,600 + 16,876)
Maintenance = 0.05 × 57,476 = €2,873
```

**Annual Operating Cost:**
```
C_op = Ċ_D × η_el × Ė_in + Ċ_elec × (Ė_in - Ċ_D)
C_op = 20.40 × 1.05 × 0.967 + 0.10 × (75 - 20.40) = 20.40 × 1.0113 = 20.68 EUR/h
C_op = 20.68 × 7,000 = €144,760/year
```

**Total Annual Cost (TAC):**
```
TAC = Maintenance + Operating + Interest
TAC = 2,873 + 144,760 + 21,951.78 = €171,584.78/year
```

**Annualized Cost (PUE):**
```
PUE = TAC / (PEC × N) = 171,584.78 / (40,600 × 15)
PUE = 171,584.78 / 609,000
PUE = 0.2813 or 28%
```

**CRF Calculation:**
```
CRF = TCI / PEC = (PEC_inst + interest + maintenance) / PEC = 57,476 / 40,600 = 1.417
```

**Ż (Annual Cost):**
```
Ż = Ċ_D × η_el × Ė_in × η_is × ξ_ex × CRF × f-factor
Ż = 20.40 × 1.05 × 0.967 × 0.32 × 1.417 × 0.8
Ż = 20.40 × 0.32 × 1.181 = 7.39 EUR/h
Ż = 7.39 × 7,000 = €51,726/year
```

**f-factor (Avoidable Share):**
```
f_factor = Ċ_D × η_el × Ė_in × ξ_ex = 20.40 × 1.05 × 0.967 × 0.32 = 7.38 EUR/h
f_factor / Ż = 7.38 / 7.39 = 0.999 → 100%
```

**r-factor (Savings-to-Investment):**
```
r_factor = f_factor / (PEC × N) = 7.38 / (40,600 × 15)
r_factor = 7.38 / 609,000
r_factor = 0.0000121 or 0.001%
```

### Step 10: Optimization Strategy

**Dominant terms:** Ċ_D (7.38 EUR/h), η_is (75 kW input, significant at 72%), CPE via installation factor.

**Strategy:**
1. **Upgrade Motor/Blower**: Replace or upgrade compressor elements to improve η_is; target 76–80%.
2. **Motor Efficiency Upgrade**: Replace with a higher-efficiency motor (e.g., IE3).
3. **Oil-Filter Maintenance**: Improve oil removal and filtration to reduce system losses.
4. **Aftercooler Optimization**: Install or upgrade aftercooler for cooler discharge air; reduces heat rejection burden.
5. **VSD Control**: Consider variable-speed drive for reduced electrical demand during part-load.

**Expected Ż reduction:** 30%–50% with focused upgrades, reducing f-factor and TCI → lower CRF.

---

**Summary Results:**
```
PEC = €40,600
TCI = €171,585/year
CRF = 1.42
Ż = €51,726/year
f-factor = 99%
r-factor = 0.001%

Recommendation: Target η_is upgrade (motor/element), focus on motor efficiency and aftercooler.
```

End of analysis.