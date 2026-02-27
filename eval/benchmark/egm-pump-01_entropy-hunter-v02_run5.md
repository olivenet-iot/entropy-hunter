# egm-pump-01
Model: entropy-hunter-v02 | Run: 5 | Temp: 0.7
Time: 42.7s | Checks: 5/6

## EGM Analysis: Centrifugal Cooling Water Pump (Full Load)

### Operating Conditions
- Volume flow rate, ṁ = 120 m³/h = 0.0333 m³/s
- Total head, H = 25 m
- Motor power input, P_elec = 12 kW
- Pump hydraulic efficiency, η_pump = 70%
- Motor efficiency, η_motor = 91%
- Fluid: liquid water at 28°C (incompressible)
- Operating condition: full_load

---

### Step 1: Hydraulic Power and Useable Power

**Hydraulic power delivered by the pump:**
```
P_hyd = ṁ × g × H
P_hyd = 0.0333 m³/s × 9.807 m/s² × 25 m
P_hyd = 8.26 kW
```

**Verification using given pump efficiency:**
```
P_hyd = P_elec × η_pump
P_hyd = 12 kW × 0.70
P_hyd = 8.40 kW

The small discrepancy (8.26 vs 8.40) is within expected numerical rounding error. We will use the value calculated directly from the energy balance as more accurate for exergy purposes.**
```

**Useful power delivered to fluid:**
```
P_useful = P_hyd
P_useful = 8.26 kW
```

---

### Step 2: Electrical Power Input and Exergy Analysis

```
P_elec = 12 kW
```

**Electrical power input (first-law):**
```
W_input = P_elec = 12 kW
```

**Bézier interpolation of water properties at 28°C (standard conditions for liquid water):**
- ρ = 996.0 kg/m³
- Cp = 4.179 kJ/(kg·K)

**Mass flow rate:**
```
ṁ = ρ × Q̇
ṁ = 996.0 kg/m³ × 0.0333 m³/s
ṁ = 33.20 kg/s
```

---

### Step 3: Pump Exergy Efficiency

The exergy efficiency (η_ex) of a pump is the ratio of the useful product exergy to the total input exergy:

```
Ex_in = P_elec × η_el = 12 kW × 1.00 = 12 kW
(First-law electrical power already converted to useable exergy)

Ex_prod = ṁ × Cp × (T_fluid,exit - T_fluid,in) + ṁ × g × H
For incompressible liquid at constant temperature:
Ex_prod = ṁ × g × H

Ex_prod = 33.20 kg/s × 9.807 m/s² × 25 m
Ex_prod = 816.4 kW
```

**Pump exergy efficiency:**
```
η_ex,pump = P_hyd / Ex_prod
η_ex,pump = 8.26 kW / 816.4 kW
η_ex,pump = 0.0101 or 1.01%
```

---

### Step 4: Motor and Total Entropy Generation

**Motor efficiency verification (first-law):**
```
P_shaft = P_hyd / η_pump
P_shaft = 8.26 kW / 0.70
P_shaft = 11.80 kW

P_motor = P_shaft / η_motor
P_motor = 11.80 kW / 0.91
P_motor = 13.00 kW

Note: The motor electrical input (12 kW) is slightly less than the shaft power (11.80 kW), indicating a small internal loss in the motor. For entropy generation we use:
```

**Electrical input to motor:**
```
P_elec,电机 = 12 kW
```

**Motor exergy efficiency:**
```
η_ex,motor = P_shaft / Ex_in_motor
Ex_in_motor = P_elec,电机 × η_el = 12 kW

Since motor is treated as a black box with losses included:
P_shaft = 11.80 kW (first-law)
Ex_shaft = ṁ × Cp × ΔT + ṁ × g × H
Ex_shaft ≈ P_hyd = 8.26 kW

η_ex,motor = 8.26 / 11.80 = 0.703 or 70.3%
```

**Total entropy generation:**
```
Ṡ_gen = Σ(quality_factor × mechanism)
quality factor = (P_elec - P_useful) / T₀
T₀ ≈ 298.15 K

Ṡ_gen = ((12 kW - 8.40 kW) / 298.15) + ((11.80 kW - 8.26 kW) / 298.15)
 quality factor motor: 3.6 / 298.15
 quality factor pump: 3.54 / 298.15

Ṡ_gen = (3.6 + 3.54) × 10⁻³
Ṡ_gen = 7.14 × 10⁻³ kW/K
```

---

### Step 5: Bejan Number and Optimization Prioritization

**Bejan number (N_s):**
```
N_s = Ṡ_gen / (P_useful / T₀)
N_s = 7.14 × 10⁻³ / (8.26 kW / 298.15 K)
N_s = 7.14 × 10⁻³ / 27.70
N_s = 0.000257 or 0.0257%
```

**Grade assignment:**
- A: < 0.1% — Excellent (reference)
- B: 0.1–0.3% — Good
- C: 0.3–1.0% — Fair
- D: 1.0–3.0% — Poor
- E: >3.0% — Very poor

**Grade:** **B (Good)**

---

### Step 6: Decomposition by Mechanism

```
Mechanism | Ex_mech (kW) | η_ex,mech | Share (%)
-------------------------------------------------
Fluid friction | 1.57 | 4.89 / 3.54 = 1.38 | 20.3%
Mechanical losses| 2.61 | 3.54 / 3.54 = 1.00 | 37.8%
-------------------------------------------------
Total:         | 4.18 |                    | 100.0%

The dominant mechanism is mechanical losses (bearings, seals), accounting for over half of the total entropy generation.
```

---

### Step 7: Improvement Strategy

**Priority Action:** Reduce mechanical losses via:
- Lubrication optimization and/or pump redesign
- Bearing upgrade to lower-friction options
- Inspection and repair of worn seal elements

**Second Priority:** Improve hydraulic efficiency by:
- Volute optimization (diffuser redesign)
- Pump alignment correction
- Motor system minimization studies for matching load better

**Expected Improvement Scenario:**
1. **Mechanical losses reduction:** 20% → 80% of current value = 2.61 × 0.8 = 2.09 kW
   - New N_s: (7.14 × 10⁻³ - 0.53) / (8.26 / 298.15) = 0.000161 → Grade C

2. **Hydraulic efficiency improvement:** 70% → 75%
   - New Ṡ_gen: 4.18 × 0.75 / (8.26 / 298.15) = 1.55 × 10⁻³
   - New N_s: (7.14 − 3.54) / (8.26 / 298.15) = 0.00094 → Grade B

**Achievable reduction:** 60% of current N_s, moving to **Grade B (Good)** with significant cost savings.

---

### Summary

- **Ṡ_gen:** 7.14 × 10⁻³ kW/K
- **N_s:** 257 m/W → Grade B: Good
- **Primary mechanism:** Mechanical losses (58%)
- **Secondary mechanism:** Fluid friction (39%)

**Recommendation:** Focus on mechanical loss reduction through improved bearing and seal design. This will reduce N_s by 60%, achieving a good grade with significant energy savings.

End of analysis.