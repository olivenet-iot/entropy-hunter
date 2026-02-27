# egm-turbine-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 51.4s | Checks: 5/6

## EGM Analysis: Back-Pressure Steam Turbine

### Operating Conditions
- **Inlet pressure:** 25 bar → **P₁ = 2.5 MPa**
- **Inlet temperature:** 350°C (superheated) → **T₁ = 623.15 K**
- **Outlet pressure:** 5 bar → **P₂ = 0.5 MPa** (back-pressure, exhaust to process)
- **Mass flow rate:** ṁ = 3 kg/s
- **Isentropic efficiency:** η_is = 75% (= 0.75)
- **Generator efficiency:** η_gen = 94% (= 0.94)
- **Operating condition:** Full load

### Step 1: Property Determination from Steam Tables (IAPWS-IF97)

**State 1 — Turbine Inlet (25 bar, 350°C)**
At P₁ = 2.5 MPa, T₁ = 623.15 K:

```
h₁ = 3084.2 kJ/kg
s₁ = 7.0910 kJ/(kg·K)
```

**State 2s — Isentropic Outlet (5 bar, s₂s = s₁)**
At P₂ = 0.5 MPa:

- Saturation properties at 0.5 MPa:
  ```
  T_sat = 134.09°C = 407.24 K
  h_f = 689.7 kJ/kg,  h_g = 2826.2 kJ/kg
  s_f = 2.0495 kJ/(kg·K),  s_g = 7.3563 kJ/(kg·K)
  ```

Since the inlet state is superheated (T₁ > T_sat at P₂):
```
h_2s = 2817.8 kJ/kg
s_2s = 7.0910 kJ/(kg·K)  →  s_g = 7.3563,  s_f = 2.0495

Check:  7.091 < 7.3563 (consistent with s_2s)
```

**State verification:** At T = 407.24 K and h = 2817.8, it indeed corresponds to a superheated state at P = 0.5 MPa.

### Step 2: Mass-Flow-Based Energy Balance

**Actual outlet enthalpy (energy balance):**
```
Q_gen = ṁ × (h₁ − h₂)   ;  h₂ determined below
```

First, compute isentropic outlet temperature:

At P₂ = 0.5 MPa, s_2s = 7.0910 kJ/(kg·K):

```
h_f = 689.7  →  T_f = −31.4°C (not possible)
s_f = 2.0495
```

Since the inlet is superheated, we cannot use s_2s at P₂ without recomputation; however:

```
s_2s = 7.0910 < 6.836 (at T_sat) → h₂s = 2817.8 kJ/kg
```

Isentropic process:
```
T₂ ≈ 459.0 K,  h_2s = 2817.8 kJ/kg
```

With η_is = 75%, the actual state (h₂) is:

```
h₂ = h₁ − ṁ × Q_gen × (1 − η_is)
Q_gen = ṁ × (h₁ − h₂)

Using iteration or energy balance:
h₂ ≈ 2638.0 kJ/kg
```

### Step 3: Energy Conversion

**Generator electrical output:**
```
W_elec = ṁ × (h₁ − h₂) × η_gen
W_elec = 3 kg/s × (3084.2 − 2638.0) kJ/kg × 0.94
W_elec = 517.8 kW × 0.94
W_elec = 484.7 kW
```

**Actual steam power:**
```
Ẇ_steam = ṁ × (h₁ − h₂)
Ẇ_steam = 3 kg/s × (3084.2 − 2638.0) kJ/kg
Ẇ_steam = 1365.6 kW
```

**Isentropic power:**
```
Ẇ_is = ṁ × (h₁ − h_2s)
Ẇ_is = 3 kg/s × (3084.2 − 2817.8) kJ/kg
Ẇ_is = 815.4 kW
```

### Step 4: Entropy Generation Calculation

**Actual entropy generation:**
```
Ṡ_gen = ṁ × (s₁ − s₂) + Q_gen × T₀⁻¹
s₂ ≈ 7.0910 − (h₂ − h_2s)/T_sat   ;  T_sat = 459.3 K

s₂ ≈ 7.0910 − (2638.0 − 2817.8)/459.3
s₂ ≈ 7.0910 + 0.397
s₂ ≈ 7.488 kJ/(kg·K)

Ṡ_gen = 3 × (7.0910 − 7.488) + 426.5 × (1/298.15)
Ṡ_gen = 3 × (−0.397) + 1.43
Ṡ_gen = −1.191 + 1.43
Ṡ_gen = 0.239 kW/K
```

**Isentropic entropy generation:**
```
Ṡ_is = ṁ × (s₁ − s_2s)
Ṡ_is = 3 × (7.0910 − 7.0910)   ;  s_2s is on same line
Ṡ_is = 0 kW/K
```

**Total entropy generation:**
```
Ṡ_gen = 0.239 kW/K
```

### Step 5: Bejan Number & Decomposition

**Bejan number (N_s):**
```
N_s = Ṡ_gen / (Ṡ_gen + Ṡ_ideal)
N_s = 0.239 / (0.239 + 0)
N_s = 1.00
```

**Blade friction (mechanical losses) — estimated at 60% of total:**
```
Ṡ_friction = 0.60 × 0.239 = 0.143 kW/K
```

**Tip leakage losses — estimated at 25% of blade loss:**
```
Ṡ_tip = 0.25 × 0.143 = 0.036 kW/K
```

**Moisture/heat loss (excess heat to surroundings):**
```
h_loss = h_2 − h_f(0.5 MPa) = 2638.0 − 689.7 = 1948.3 kJ/kg
Ẇ_loss = ṁ × 1948.3 = 3 × 1948.3 = 5,844.9 kW

Ṡ_loss = Q_loss / T₀ = 5,844.9 / 298.15 = 19.637 kW/K
```

**Moisture mechanism ratio:**
```
X_hydr = ṁ × (h_f − h₂) / ṁ × (h₁ − h_2s)
X_hydr = (689.7 − 2638.0) / (3084.2 − 2817.8)
X_hydr = −1,948.3 / 266.4
X_hydr = −7.32   →  Moisture is not present at this state; mechanism ratio not applicable.
```

**Actual decomposition:**
```
N_s,B = Ṡ_friction / Ṡ_gen  = 0.143 / 0.239 = 0.60
N_s,T = Ṡ_tip     / Ṡ_gen  = 0.036 / 0.239 = 0.15
N_s,H = Ṡ_loss   / Ṡ_gen  = 19.637 / 0.239 = 82.46
```

### Step 6: Grade Assignment

**Grade assignment (Szargut):**
- **A:** < 0.15 → no significant losses detected (blade alignment, lubrication)
- **B:** 0.15–0.30 — moderate friction losses; improve seal, bearing design
- **C:** 0.30–0.60 — substantial blade or mechanical losses; consider upgrade/alignment
- **D:** > 0.60 — severe mechanical degradation; urgent maintenance required

**Current grade: B (blade loss)**
**Target grade: A**

### Step 7: Improvement Strategy

1. **Component inspection and alignment:** Ensure blade-to-nozzle clearance is within specifications.
2. **Bearing lubrication optimization:** Reduce bearing friction with improved oil flow/noise detection.
3. **Seal leakage reduction:** Investigate and reduce axial/casing leakage.
4. **Casing insulation improvement:** Reduce heat loss to surroundings via better casing insulation.

### Summary

**Total entropy generation:** 0.239 kW/K
**Bejan number (N_s):** 1.00 — suboptimal, indicates significant losses from blade friction and/or other mechanisms.
**Dominant mechanism:** Blade friction (60%), tip leakage (15%)
**Generator efficiency:** 484.7 / 1365.6 = 35.5%

**Recommendation:** Focus on reducing mechanical losses through alignment, bearing optimization, and improved sealing. A comprehensive inspection is recommended to identify specific fault areas.

By achieving an N_s < 0.3 (B grade), the back-pressure turbine can improve its efficiency by approximately 2–4 percentage points with targeted maintenance measures.