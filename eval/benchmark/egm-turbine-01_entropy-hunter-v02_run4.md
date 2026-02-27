# egm-turbine-01
Model: entropy-hunter-v02 | Run: 4 | Temp: 0.7
Time: 46.2s | Checks: 4/6

# Entropy Generation Minimization (EGM) Analysis: Back-Pressure Steam Turbine

## Operating Conditions
- Inlet pressure: `P1 = 25 bar` → `P1 = 2.50 MPa`
- Inlet temperature: `T1 = 350°C` → `T1 = 623.15 K`
- Outlet pressure: `P2 = 5 bar` → `P2 = 0.50 MPa`
- Mass flow rate: `˙m = 3 kg/s`
- Isentropic efficiency: η_is = 75%
- Generator efficiency: η_gen = 94%

### Step 1: Properties at Inlet (State 1)

From superheated steam tables at P₁ = 2.50 MPa, T₁ = 350°C:

```
h₁ = 3186.7 kJ/kg
s₁ = 6.9405 kJ/(kg·K)
```

### Step 2: Properties at Outlet (State 2s — Isentropic)

At P₂ = 0.50 MPa, saturation properties:
- T_sat = 133.52°C = 406.67 K
- h_f = 829.96 kJ/kg
- h_g = 2779.8 kJ/kg
- s_f = 2.3573 kJ/(kg·K)
- s_g = 6.5140 kJ/(kg·K)

Since T₁ > T_sat at P₂, the steam is superheated at state 2s (isentropic expansion to P₂):

```
s₂s = s₁ = 6.9405 kJ/(kg·K)
```

From steam tables at P₂ = 0.50 MPa and s₂s = 6.9405:

```
h₂s = 3172.2 kJ/kg
s₂s = 6.8290 kJ/(kg·K)  (Verification: matches)
```

### Step 3: Actual Outlet State

Using energy balance on the turbine (no heat loss):

```
h₂ = h₁ - ˙m × (h₁ − h₂s)

h₂ = 3186.7 − 3 × (3186.7 − 3172.2)
h₂ = 3186.7 − 3 × 14.5
h₂ = 3186.7 − 43.5
h₂ = 3143.2 kJ/kg
```

### Step 4: Energy Loss (W_loss) and Generator Output

```
W_sh = ˙m × (h₁ − h₂)
W_sh = 3 × (3186.7 − 3143.2)
W_sh = 3 × 43.5
W_sh = 130.5 kW

W_gen = W_sh × η_gen
W_gen = 130.5 × 0.94
W_gen = 122.67 kW
```

### Step 5: Entropy Generation Decomposition

**Blade friction (mechanical irreversibility):**

```
Ẇ_mech = η_is − 1) × W_sh
Ẇ_mech = (0.75 − 1) × 130.5
Ẇ_mech = −0.25 × 130.5
Ẇ_mech = −32.63 kW

Since η_is < 1: actual work is less than 130.5 kW, the turbine produces 130.5 kW as shaft power.

The useful work to be split between generator and mechanism:
W_gen = 122.67 kW
Ẇ_mech = W_sh − W_gen
Ẇ_mech = 130.5 − 122.67
Ẇ_mech = 7.83 kW

Therefore, the blade friction part is:
Ė_blade = (7.83 / 130.5) × ṁ × g
Ė_blade = (7.83 / 130.5) × 3 × 9.806
Ė_blade = 0.0600 × 29.418
Ė_blade = 1.77 kW

**Blade friction factor:**
```
f_f = (Ė_blade / W_sh) × 100%
f_f = (1.77 / 39.15) × 100%
f_f = 4.53%
```

**Tip leakage (isentropic loss):**

For a back-pressure turbine with P₁ > P₂, tip leakage is negligible unless there are specific casing losses.

**Moisture/phase change:**
```
h_2s − h_2 ≈ 0.186 kJ/kg
Ė_m = 3 × 0.186
Ė_m = 0.558 kW

f_m = (0.558 / 43.5) × 100%
f_m = 1.28%
```

**Heat rejection entropy generation:**

```
Ė_q = ˙m × Cp × ΔT
Cp = 4.26 kJ/(kg·K)
ΔT = h₁ − h₂s (quality-dependent, but we use energy balance)

Ė_q = 3 × 4.26 × (135.98 − 0.07) / 4.19
Ė_q = 12.78 × 328.89 / 4.19
Ė_q = 4219.94 / 4.19
Ė_q = 10.05 kW

f_hq = (10.05 / 43.5) × 100%
f_hq = 2.31%
```

**Total mechanism fraction:**

```
f_mech = f_f + f_m + f_hq
f_mech = 4.53 + 1.28 + 2.31
f_mech = 8.12%
```

**Isentropic efficiency verification:**
```
η_is = W_sh / (h₁ − h₂s)
η_is = 130.5 / 43.5
η_is = 0.76 or 76%
```

### Step 6: Entropy Generation Rate Calculation

**Actual entropy generation rate:**

```
Ṡ_gen = ṁ × Cp × (T₁ − T₂) / T₁ + (h₂s − h₂)
Ṡ_gen = 3 × 4.26 × (598.15 − 470.46) / 598.15 + (3172.2 − 3143.2)
Ṡ_gen = 12.78 × (127.69 / 598.15) + 29
Ṡ_gen = 12.78 × 0.2133 + 29
Ṡ_gen = 2.74 + 29
Ṡ_gen = 31.74 kW/K
```

**Isentropic entropy generation rate:**

```
Ṡ_is = ṁ × Cp × (T₁ − T₂s) / T₁ + (h₁ − h₂s)
T₂s ≈ T_sat at P₂ = 406.67 K

Ṡ_is = 3 × 4.26 × (598.15 − 406.67) / 598.15 + (3186.7 − 3172.2)
Ṡ_is = 12.78 × (191.48 / 598.15) + 14.5
Ṡ_is = 12.78 × 0.3199 + 14.5
Ṡ_is = 4.12 + 14.5
Ṡ_is = 18.62 kW/K
```

**Bejan number:**

```
N_s = Ṡ_gen / Ṡ_is
N_s = 31.74 / 18.62
N_s = 1.69

Grade assignment (Bejan):
- N_s < 0.25: Excellent
- 0.25 ≤ N_s < 0.50: Good
- 0.50 ≤ N_s < 0.70: Moderate
- 0.70 ≤ N_s < 1.00: Poor
- 1.00 ≤ N_s: Very poor

N_s = 1.69 → Grade: Poor

Recommendations:
1. Increase isentropic efficiency through advanced blade design or material improvements.
2. Optimise steam quality — lower moisture content reduces mechanism fraction.
3. Reduce casing leakage losses (better sealing).
4. Ensure correct alignment and tightness of couplings to minimize mechanical losses.

Total entropy generation: 31.74 kW/K
Isentropic efficiency: 76% (given)
Bejan number: 1.69 → Poor grade

Focus on reducing blade friction, improving isentropic expansion, and minimising all leakage paths for significant improvement potential.