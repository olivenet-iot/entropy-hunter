# avun-pump-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 39.6s | Checks: 4/4

## Exergy Analysis: Centrifugal Pump (Water at 25°C)

### Assumptions

1. Steady-state, steady-flow operation.
2. Fluid: liquid water at 25°C — treated as incompressible.
3. The fluid temperature rise due to friction is small and neglected (ΔT ≈ 0 K or negligible for exergy purposes).
4. Electrical power input is pure work (exergy = energy).
5. Kinetic and potential exergy changes at system boundary are negligible.
6. Water density: ρ = 997 kg/m³.
7. Gravitational acceleration: g = 9.81 m/s².

---

### Mass Flow Rate

```
ṁ = ρ × Q̇
ṁ = 997 kg/m³ × (100 / 3600) m³/s
ṁ = 997 × 0.02778 m³/s
ṁ = 27.65 kg/s
```

---

### Hydraulic Power

The useful hydraulic power delivered to the fluid:

```
P_hyd = ṁ × g × H
P_hyd = 27.65 kg/s × 9.81 m/s² × 50 m
P_hyd = 27.65 × 490.5 W
P_hyd = 13,559.5 W = 13.56 kW
```

---

### Total Pump Exergy Efficiency

```
η_pump = P_hyd / (η_pump × η_motor × P_elec)
13.56 = 100 × 0.65 × 0.90 × P_elec
P_elec = 13.56 / (0.65 × 0.90)
P_elec = 13.56 / 0.585
P_elec = 23.22 kW
```

---

### Electrical Input Verification

```
P_in = η_pump × η_motor × P_elec
P_in = 0.65 × 0.90 × 23.22 kW
P_in = 14.83 kW (not matching the stated motor input of 22 kW, so use that)
```

---

### Exergy of Electrical Input

Since electrical power is pure work:

```
Ex_in = P_in = 22 kW
```

---

### Useful (Hydraulic) Exergy Output

```
Ex_hyd = ṁ × g × H
Ex_hyd = 997 kg/s × 9.81 m/s² × 50 m
Ex_hyd = 49,382.5 W
Ex_hyd = 49.38 kW
```

---

### Total Exergy Destruction

```
Ex_d = Ex_in − Ex_hyd
Ex_d = 22 − 49.38
Ex_d = 16.70 kW (incorrect sign, must be positive)
Ex_d = 22 − 13.56
Ex_d = 8.44 kW
```

**Correction:** The above calculation is incorrect as the useful hydraulic exergy (ex_hyd) should not exceed the electrical input (ex_in). Let's redo:

```
Ex_hyd = P_hyd = 13.56 kW (useful hydraulic power delivered)

Ex_d = Ex_in − Ex_hyd
Ex_d = 22 − 13.56
Ex_d = 8.44 kW
```

---

### Avoidable/Unavoidable Decomposition

Using the BAT reference:

**BAT:**
- η_pump_BAT = 0.88
- η_motor_BAT = 0.97

#### BAT Hydraulic Power

```
P_hyd,BAT = ṁ × g × H
P_hyd,BAT = 27.65 kg/s × 9.81 m/s² × 50 m
P_hyd,BAT = 13,545 W
P_hyd,BAT = 13.55 kW (rounded)
```

#### BAT Electrical Input

```
η_pump_BAT = P_hyd,BAT / (η_pump_BAT × η_motor_BAT × P_elec,BAT)
13.55 = 0.88 × 0.97 × P_elec,BAT
P_elec,BAT = 13.55 / (0.88 × 0.97)
P_elec,BAT = 13.55 / 0.8536
P_elec,BAT ≈ 15.91 kW
```

---

#### Unavoidable Exergy Destruction

At BAT efficiency:

```
Ex_hyd,BAT = P_hyd,BAT = 13.55 kW
Ex_d,unav = Ex_in − Ex_hyd,BAT
Ex_d,unav = 22 − 13.55
Ex_d,unav = 8.45 kW
```

---

#### Avoidable Exergy Destruction

The avoidable component is the difference between actual and BAT:

```
Ex_d.av = Ex_d − Ex_d,unav
Ex_d.av = 8.44 − 8.45
Ex_d.av ≈ 0.01 kW
```

---

### Summary Table

| Item | Value |
|------|-------|
| **Flow rate** | 100 m³/h |
| **Total head** | 50 m |
| **Motor power (input)** | 22 kW |
| **Pump efficiency** | 65% |
| **Motor efficiency** | 90% |
| **Fluid** | Water, 25°C |
|
| **Hydraulic power (useful)** | 13.56 kW |
| **Exergy input (electrical)** | 22 kW |
| **Exergy output (hydraulic)** | 13.56 kW |
| **Total exergy destruction** | 8.44 kW |
|
| **BAT reference (Grundfos CRE IE5)** | — |
| **BAT hydraulic power** | 13.55 kW |
| **Unavoidable exergy destruction** | 8.45 kW |
| **Avoidable exergy destruction** | 0.01 kW |
|
| **Improvement potential** | Extremely low (< 1%) — pump is already very close to BAT with minimal improvement opportunity at these operating conditions. |

---

### Conclusion

The system is performing surprisingly well, with a total exergy destruction of only 8.44 kW. Given the stated motor power (22 kW), the pump configuration appears highly optimized relative to the reference BAT.

**Avoidable exergy destruction:** 0.01 kW
**Unavoidable exergy destruction:** 8.45 kW

The small avoidable component indicates that further efficiency improvements at this operating point would be marginal and likely require costly upgrades such as motor replacement or pump optimization (e.g., cavitation suppression, impeller re-cutting). The actual pump efficiency of 65% is already close to the BAT reference (88%), so any additional gains will be minimal.

**Recommendation:** Given that the system is operating within a few percentage points of the benchmark, focus should shift toward routine maintenance and operational optimization. Regular inspections for leaks, bearing wear, and alignment checks can help maintain this high level of efficiency.

For significant further improvements at similar relative cost-effectiveness:
1. **Motor upgrade** (e.g., high-efficiency IE3 or IE4)
2. **VFD tuning** — soft-start/soft-stop operation to reduce transient power surges.
3. **Cavitation prevention measures** (increased NPSH margin, higher operating pressure if possible).

The 0.01 kW avoidable exergy improvement would result in:

```
ΔEx_d.av / Ex_in = 0.01 / 22
= 0.00045 or 0.045%
```

At this tiny level, the focus should remain on system-level optimization rather than equipment-specific modifications.

---

**End of Analysis**