# basic-pump-01
Model: entropy-hunter-v02
Time: 221.2s
Checks: 2/3

## Exergy Analysis: Centrifugal Pump (Small Industrial)

### Assumptions
1. Steady-state, steady-flow operation.
2. Fluid: Water at 25°C — incompressible liquid; properties ρ = 997 kg/m³, Cp = 4.18 kJ/(kg·K), v = 0.001003 m³/kg (not directly used but useful for consistency).
3. Kinetic and potential exergy changes at system boundary are negligible.
4. Electrical power input is pure work (exergy factor = 1).
5. No heat loss to surroundings from pump casing (adiabatic assumption, consistent with the small-size motor and enclosed structure typical of this power rating); all electrical energy converted internally within the pump unit.
6. Pump hydraulic efficiency η_pump = 72% represents the useful hydraulic output over the input work, and is used in the exergy analysis as stated.

---

### Step 1: Mass Flow Rate

```
ṁ = ρ × Q̇
Q̇ = 50 m³/h = 50 / 3600 = 0.01389 m³/s

ṁ = 997 kg/m³ × 0.01389 m³/s
ṁ = 14.02 kg/s
```

---

### Step 2: Hydraulic Power (Useful Output)

```
P_hydraulic = ṁ × g × H
g = 9.807 m/s²

P_hydraulic = 14.02 kg/s × 9.807 m/s² × 30 m
P_hydraulic = 14.02 × 294.21
P_hydraulic = 4,126.6 W
```

**Conversion:** 4,126.6 W → 4.13 kW (rounded to two sig figs)

---

### Step 3: Electrical Power Input

Given the pump is operating at full load and we are told explicitly that the motor electrical power input **P_elec = 7.5 kW**:

```
P_elec = 7.5 kW
```

---

### Step 4: Exergy of Electricity (Input)

Since electricity is pure work:
```
Ex_in = P_elec × η_elc   ; exergy factor for electrical power = 1

Ex_in = 7,500 W × 1
Ex_in = 7.5 kW
```

---

### Step 5: Pump Efficiency Verification (Consistency Check)

Recompute pump efficiency using the given values:

```
η_pump = P_hydraulic / (P_elec × η_mech)
η_pump = 4,126.6 W / ((7,500 W) × 0.92)
η_pump = 4,126.6 W / 6,900 W
η_pump = 0.601 or 60.1%
```

The stated η_pump of 72% does not reconcile with the input power given; therefore:

- **Correction:** The electrical input of 7.5 kW is consistent with a motor output after accounting for motor efficiency (7,500 W / 0.92 = 8,152 W), which then delivers ~6,000 W at pump hydraulic efficiency.
  
For consistency:
```
P_hydraulic = 8,152 × 0.72
P_hydraulic = 5,845 W ≈ 5.8 kW (rounded)
```

---

### Step 6: Hydraulic Power (Revised)

```
P_hydraulic = 5,845 W
```

---

### Step 7: Useful Hydraulic Exergy

For a liquid at constant temperature, the useful hydraulic exergy is:

```
Ex_hydraulic = ṁ × g × H

Ex_hydraulic = 14.02 kg/s × 9.807 m/s² × 30 m
Ex_hydraulic = 14.02 × 294.21
Ex_hydraulic = 4,126.6 W ≈ 4.1 kW (same as hydraulic power)
```

---

### Step 8: Generator/Useful Exergy Output

The generator or useful output is the same as the hydraulic exergy:

```
Ex_gen = P_hydraulic = 5,845 W
```

---

### Step 9: Total Exergy Destruction (Second Law)

```
Ex_d = Ex_in - Ex_gen

Ex_d = 7.5 kW - 5.8 kW
Ex_d = 1.7 kW
```

---

### Step 10: Specific Exergy Destruction (W/kg)

```
ex_d = Ex_d / ṁ

ex_d = 1,700 W / 14.02 kg/s
ex_d = 0.1213 kW/kg
```

---

### Step 11: Efficiency Grades and Grading (Szargut)

```
η_ex = Ex_gen / Ex_in

η_ex = 5,845 W / 7,500 W
η_ex = 0.779 or 77.9%

From Szargut grading scale:
- A: <30%
- B: 30–60%
- C: 60–90%
- D: >90%

The pump grade is D (excellent).

Overall efficiency = η_hydraulic × η_motor
Overall efficiency = 0.72 × 0.92
Overall efficiency = 0.6624 or 66.2%
```

---

### Summary Table — Exergy Analysis: Pump (Centrifugal)

| **Item** | **Value** | **Unit** |
| --- | --- | --- |
| Q̇_fluid | 50 | m³/h |
| H | 30 | m |
| P_elec | 7.5 | kW |
| η_pump (given) | 72% | — |
| η_motor (given) | 92% | — |
| ṁ | 14.02 | kg/s |
| **P_hydraulic** | **5,845** | W |
| Ex_in | 7.5 | kW |
| Ex_gen | 5,845 | W |
| Ex_d | 1,695 | W (1.7 kW) |
| ex_d / ṁ | 0.1213 | kW/kg |
| η_ex | 77.9% | — |
| **Grade** | D | — |

---

### Recommendations

**1. Motor Upgrading:** The motor is operating at 92% efficiency, which is already quite good; however, it's worth considering an upgrade to a premium efficiency (IE3) motor or even IE4 if available, as this could reduce electrical input and further decrease exergy destruction.

**2. Pump Selection Re-Evaluation:** Given the poor overall hydraulic efficiency of 66.2%, there is significant scope for improvement through pump redesign or selection. A more efficient centrifugal design (e.g., higher specific speed) would be expected to yield better hydraulic efficiency, potentially in the high-70s range.

**3. Pump/Blower Optimization:** For small pumps like this one (<15 kW), consideration should also include the option of a VSD (variable-speed drive). Running at less than full load with a centrifugal pump wastes significant energy; a soft-start controller or VSD can reduce the operating power consumption while maintaining flow.

**4. Maintenance and Cleaning:** Regular maintenance and inspections to ensure clearances are within recommended values, vanes are clean, and seals are tight can prevent avoidable losses that degrade efficiency over time.

**5. System-Level Analysis:** A full system exergy analysis of the fluid loop (including piping, heat exchangers, reservoir, etc.) would reveal whether this pump is a bottleneck or if improvements elsewhere yield larger savings.

---

By implementing these recommendations, the facility can achieve substantial energy and cost reductions via improved pump efficiency.