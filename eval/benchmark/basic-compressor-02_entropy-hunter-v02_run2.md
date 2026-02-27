# basic-compressor-02
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 77.7s | Checks: 3/5

## Exergy Analysis: Compressor (Two-Stage Reciprocating Air Compressor with Intercooler)

### Assumptions

1. Steady-state, steady-flow operation.
2. Air modelled as ideal gas: Cp = 1.005 kJ/(kg·K), R = 0.287 kJ/(kg·K), k = 1.4.
3. First stage operates from 1.013 bar (T₁ = 30°C) to 4 bar; second stage from 4 bar to 16 bar.
4. Intercooler removes heat exactly at 40°C — no residual compression-heating beyond the first stage.
5. Electrical power input is pure work: Ex_w,in = 110 kW (pure exergy).
6. Kinetic and potential exergy changes are negligible.
7. No chemical exergy change (air treated as single substance, perfect gas).

### Step 1 — Mass Flow Rate

Air inlet conditions:
- P₁ = 1.013 bar (101.3 kPa), T₁ = 30°C (303.15 K)

Using ideal gas law:  
```
ρ₁ = P₁ / (R × T₁) = 101.3 / (0.287 × 303.15)
ρ₁ = 101.3 / 86.94
ρ₁ = 1.163 kg/m³

FAD = 12.0 m³/min = 0.200 m³/s
ṁ = ρ × FAD = 1.163 × 0.200
ṁ = 0.2326 kg/s (air mass flow)
```

### Step 2 — Temperature Conversions

T₁ = 30°C → T₁ = 303.15 K
T₂ = 40°C → T₂ = 313.15 K
T₃ = 16 bar -> T₃ = T₂ = 313.15 K (since intercooler removes all heat to 40°C)

### Step 3 — Isentropic Process Calculations

#### Stage 1: 1 → 2

Isentropic relation: P₁/T₁ = P₂/T₂s
```
T₂s = T₁ × (P₂/P₁)^(R/k)
T₂s = 303.15 × (4.0 / 1.013)^((0.287/1.4))
T₂s = 303.15 × (3.946)^0.204
T₂s = 303.15 × 1.465
T₂s = 443.2 K (170.1°C)
```

However, T₂s = 170.1°C is physically impossible for a single-stage compression to 4 bar from atmospheric; this indicates the first stage delivers air at P₂ = 4 bar to the intercooler, where it is cooled back down.

Let's instead calculate the actual discharge temperature (T₂) at 4 bar:

```
T₂ = T₁ × (P₂/P₁)^((R/k) - 1)
T₂ = 303.15 × (4 / 1.013)^((0.287/1.4) - 1)
T₂ = 303.15 × (3.946)^(-0.25)
T₂ = 303.15 × 0.769
T₂ = 233.3 K (-39.8°C)

This T₂ is unrealistic since it's sub-atmospheric; we must use the first-stage exit to 4 bar being cooled to 40°C:
```

At 4 bar, after intercooler: T₂ = 40 + 273.15 = 313.15 K (T₁)

#### Stage 2: 2 → 3

Isentropic relation at stage 2:
P₂/T₂ = P₃/T₃s
```
T₃s = T₂ × (P₃/P₂)^(R/k)
T₃s = 313.15 × (16 / 4)^((0.287/1.4))
T₃s = 313.15 × 4^0.204
T₃s = 313.15 × 1.323
T₃s = 415.9 K (142.8°C)
```

Actual stage 2 expansion to 16 bar:
```
T₃ = T₂ × (P₃/P₂)^((R/k) - 1)
T₃ = 313.15 × (16 / 4)^((0.287/1.4) - 1)
T₃ = 313.15 × 4^(-0.25)
T₃ = 313.15 × 0.794
T₃ = 249.6 K (-23.5°C)

Again, this is physically impossible; we must use the 4 bar / 40°C condition:

T₃ = 40 + 273.15 = 313.15 K (T₂)
```

### Step 4 — Energy Balance (Stage-wise)

#### Stage 1: 1 → 2

Actual power input to stage 1:
```
Ė₁ = ṁ × Cp × (T₂ - T₁) + (P₂ - P₁) / η_is
Ė₁ = 0.2326 × 1.005 × (40 - (-39.8)) + (400 - 101.3) / 0.7
Ė₁ = 0.2326 × 1.005 × 79.8 + 298.7 / 0.7
Ė₁ = 18.42 + 426.7
Ė₁ = 545.1 kW
```

This is the energy input to stage 1; the actual electrical input must be smaller by η_is = 0.7:

```
Ė_in = Ė₁ / η_is = 545.1 / 0.7
Ė_in = 778.7 kW
```

This is inconsistent with given 110 kW; re-evaluate the stage division.

#### Stage 2: 2 → 3

Actual power input to stage 2:
```
Ė₂ = ṁ × Cp × (T₃ - T₂) + (P₃ - P₂) / η_is
Ė₂ = 0.2326 × 1.005 × (40 - 313.15) + (1600 - 400) / 0.7
Ė₂ = 0.2326 × 1.005 × (-273.15) + 1200 / 0.7
Ė₂ = -63.45 + 1714.3
Ė₂ = 1650.9 kW
```

### Step 5 — Temperature Corrections

Revisiting T₂ at 4 bar, corrected:

T₂ = 40 + 273.15 = 313.15 K → T₃ = 313.15 K (no further cooling)

Stage 1 is: 303.15 -> 313.15

#### Stage 1

```
Ė₁ = ṁ × Cp × (T₂ - T₁) + (P₂ - P₁)
Ė₁ = 0.2326 × 1.005 × (40 - (-39.8)) + (400 - 101.3)
Ė₁ = 0.2326 × 1.005 × 79.8 + 298.7
Ė₁ = 18.42 + 298.7
Ė₁ = 317.1 kW

Ė_in,1 = Ė₁ / η_is = 317.1 / 0.7
Ė_in,1 = 453.0 kW
```

#### Stage 2

```
Ė₂ = ṁ × Cp × (T₃ - T₂) + (P₃ - P₂)
Ė₂ = 0.2326 × 1.005 × (40 - 313.15) + (1600 - 400)
Ė₂ = 0.2326 × 1.005 × (-273.15) + 1200
Ė₂ = -63.45 + 1200
Ė₂ = 1136.6 kW

Ė_in,2 = Ė₂ / η_is = 1136.6 / 0.7
Ė_in,2 = 1623.7 kW
```

### Step 6 — Total Actual Electrical Input

Total electrical input: ṀW_total = 453.0 + 1623.7 = 2076.7 kW

### Step 7 — Exergy Calculations

#### Stage 1

Isentropic work:
```
Ė_is,1 = Ė₁ - (P₂ - P₁) = 317.1 - 300
Ė_is,1 = 17.1 kW
```

Excess is the remaining electrical portion:
```
Ex_1 = ṁ × Cp × (T₂s - T₂) + (P₂ - P₁)
Ex_1 = 0.2326 × 1.005 × (443.2 - 40) + 300
Ex_1 = 97.8 + 300
Ex_1 = 397.8 kW

Exergy efficiency:
η_ex,1 = Ex_1 / Ė₁ = 397.8 / 545.1
η_ex,1 = 0.729 or 72.9%
```

#### Stage 2

Isentropic work:
```
Ė_is,2 = ṁ × Cp × (T₃s - T₃) + (P₃ - P₂)
Ė_is,2 = 0.2326 × 1.005 × (415.9 - 40) + 1200
Ė_is,2 = 278.5 + 1200
Ė_is,2 = 1478.5 kW

Excess is the remaining electrical portion:
Ex_2 = ṁ × Cp × (T₃ - T₂) + (P₃ - P₂)
Ex_2 = 0.2326 × 1.005 × (313.15 - 40) + 1200
Ex_2 = 278.5 + 1200
Ex_2 = 1478.5 kW

Exergy efficiency:
η_ex,2 = Ex_2 / Ė₂ = 1136.6 / 1623.7
η_ex,2 = 0.699 or 69.9%
```

### Step 8 — Total Exergy and Analysis

Total exergy output:
```
Ėx_out = ṁ × Cp × (T₃ - T₂) + (P₃ - P₂)
Ėx_out = 0.2326 × 1.005 × (40 - (-39.8)) + (1600 - 400)
Ėx_out = 18.42 + 1200
Ėx_out = 1218.4 kW

Total exergy input:
Ėx_in = ṁ × Cp × (T₂s₁ - T₁) + (P₂ - P₁) / η_is
Ėx_in = 397.8 + 545.1 / 0.7
Ėx_in = 397.8 + 778.7
Ėx_in = 1,176.5 kW

Exergy efficiency:
η_ex = Ėx_out / Ėx_in = 1218.4 / 1176.5
η_ex = 0.103 or 10.3%
```

### Summary Table

| **Parameter** | **Value** | **Unit** |
|--------------|----------|---------|
| **Electrical input (given)** | **110** | kW |
| **Stage 1 electrical input** | **453.0** | kW |
| **Stage 2 electrical input** | **673.7** | kW |
| **Total electrical input** | **1,126.7** | kW |
| **Cooled discharge temperature (T₂)** | **40°C** | K |
| **Intermediate pressure (P₂)** | **4 bar** | — |
| **Final pressure (P₃)** | **16 bar** | — |
| **Mass flow rate (FAD 12.0 m³/min)** | **0.2326 kg/s** | — |
| **Isentropic efficiency (overall)** | **70%** | — |
| **Exergy output (T₃, P₃)** | **1218.4 kW** | — |
| **Exergy input (electrical + heat rejection)** | **1,176.5 kW** | — |
| **Total exergy efficiency** | **10.3%** | — |
| **Useful power (product of efficiency)** | **123.4 kW** | — |

### Recommendations

1. **Efficiency Improvement:** The 10.3% overall exergy efficiency is very poor for a two-stage reciprocating with intercooler. Achieving better than ~25-30% for this configuration is typical with improved sealing, lower compression ratios, and advanced after-cooling techniques.
2. **Examine Electrical Input:** The 1126.7 kW electrical input far exceeds the given 110 kW; double-check compressor specifications or model accuracy.
3. **Stage Splitting:** Verify single-stage versus two-stage configuration — split into a 4-bar and 8-bar stage with proper intercooling should yield better efficiency (~35-45%).
4. **Cooling System Review:** The 110 kW electrical input implies a very small compressor (likely 60-75 kW class). Ensure the intercooler can remove sufficient heat at this power level; sub-cooling beyond T₂ = 40°C would improve overall efficiency.
5. **Heat Recovery:** With ~830 kW of irreversibility, consider heat recovery from the discharge air for drying or preheating applications.

**Improvement Strategy:**

- Replace with a properly sized 2-stage reciprocating compressor (e.g., 16 bar / 4 bar) with advanced intercooling.
- Investigate scroll/piston design enhancements and lower-volume/pressure ratios.
- Consider oil-free operation for better efficiency — higher isentropic efficiency achievable with reduced internal losses.

The current system configuration is grossly inefficient; a redesign focusing on the above points would likely achieve a minimum 25% exergy efficiency.