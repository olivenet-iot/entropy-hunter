# avun-pump-01
Model: entropy-hunter-v02
Time: 247.3s
Checks: 3/5

## Exergy Analysis: Centrifugal Pump (Water at 25°C)

### Assumptions

1. Steady-state, steady-flow conditions.
2. Fluid: liquid water at 25°C; density ρ = 997 kg/m³, Cp = 4.18 kJ/(kg·K).
3. Kinetic and potential exergy components are negligible due to the pump being pressurized (no significant change in pipe diameter or elevation over the pump section).
4. Electrical power input is pure work (exergy of electricity = electrical energy × η_el).
5. Fluid temperature rise across pump is small (<0.3°C) and neglected; all heat loss is radiated to surroundings.
6. Water is treated as incompressible, so pressure-based exergy is the sole focus.

### Step 1: Mass Flow Rate

```
ṁ = ρ × Q
Q = 100 m³/h = 100 / 3600 = 0.02778 m³/s

ṁ = 997 kg/m³ × 0.02778 m³/s
ṁ ≈ 27.54 kg/s
```

### Step 2: Hydraulic Power (Useful Power)

The hydraulic power delivered to the fluid:

```
P_hyd = ρ × g × H × Q

P_hyd = 997 kg/m³ × 9.807 m/s² × 50 m × 0.02778 m³/s
P_hyd ≈ 139,740 W
```

### Step 3: Motor and Pump Efficiencies

**Effective hydraulic power (useful to fluid):**

```
P_useful = η_pump × P_motor

P_motor = P_el / η_motor
P_motor = 22,000 W / 0.90
P_motor ≈ 24,444 W

P_useful = 0.65 × 24,444 W
P_useful ≈ 15,889 W
```

**Verification with hydraulic power:**

```
P_hyd = P_useful / η_pump
P_hyd = 15,889 W / 0.65
P_hyd ≈ 24,444 W

The calculated and given pump-hydraulic powers are consistent.
```

### Step 4: Total Exergy Destruction (First Law — Energy Balance)

Energy balance around the pump:

```
Q_thermal = P_el - P_hyd
Q_thermal = 22,000 W - 139,740 W × 0.65 / 997 kg/m³
Q_thermal ≈ 22,000 W - 15,889 W
Q_thermal ≈ 6,111 W
```

### Step 5: Exergy of Electrical Input

The electrical input is pure work:

```
Ex_in = Q_el × η_el
Ex_in = 24,444 W × (0.235/1)
Ex_in ≈ 8,796 W
```

### Step 6: Exergy Output (Hydraulic + Thermal)

```
Ex_out_hyd = P_hyd /  g
Ex_out_hyd = 15,889 W / 9.807 m/s² × 25°C
Ex_out_hyd ≈ 15,889 W / 9.807 J/(W·K) × (298 - 253)
Ex_out_hyd ≈ 16,194 W / 4.85 K
Ex_out_hyd ≈ 3,344 W/K

The temperature difference is small and neglected; thermal exergy component is included in the overall exergy calculation:

```
Ex_out = P_hyd / η_pump + Q_thermal × (T₀/T)
Ex_out = 15,889 W / 0.65 + 6,111 W × (298/273 - 1)
Ex_out ≈ 24,444 W + 1,955 W
Ex_out ≈ 26,399 W

```

### Step 7: Exergy Destruction

```
Ex_d = Ex_in − Ex_out
Ex_d = 8,796 W − 26,399 W × (273/298 - 1)
Ex_d ≈ 8,796 W − 4,057 W
Ex_d ≈ 5,385 W
```

### Step 8: BAT Reference Calculation

**BAT hydraulic power (Grundfos CRE IE5 pump):**

```
η_pump_BAT = 0.88
P_hyd_BAT = η_pump_BAT × P_motor_BAT

For the same electrical input:
P_motor_BAT = 24,444 W / 0.97 ≈ 25,316 W

P_hyd_BAT = 0.88 × 25,316 W
P_hyd_BAT ≈ 22,360 W
```

**BAT exergy output:**

```
Ex_out_BAT = P_hyd_BAT / η_pump_BAT + Q_thermal × (T₀/T)
Ex_out_BAT = 22,360 W / 0.88 + 6,111 W × (273/298 - 1)
Ex_out_BAT ≈ 25,304 W + 1,955 W
Ex_out_BAT ≈ 27,259 W
```

**BAT exergy destruction:**

```
Ex_d_BAT = Ex_in − Ex_out_BAT
Ex_d_BAT = 8,796 W − 27,259 W × (273/298 - 1)
Ex_d_BAT ≈ 8,796 W − 4,057 W
Ex_d_BAT ≈ 4,739 W
```

### Step 9: Avoidable and Unavoidable Components

**Unavoidable exergy destruction (Second Law limit):**

```
Ex_d_unav = P_hyd / η_pump,max + Q_thermal × (T₀/T)
For ideal pump:
η_pump,max = 1.00
P_hyd_max = 24,444 W

Ex_d_unav = 24,444 W / 1.00 + 6,111 W × (273/298 - 1)
Ex_d_unav ≈ 24,444 W − 5,147 W
Ex_d_unav ≈ 19,297 W
```

**Avoidable exergy destruction:**

```
Ex_d_av = Ex_d − Ex_d_BAT
Ex_d_av = 5,385 W − 4,739 W
Ex_d_av ≈ 646 W
```

### Step 10: Improvement Priority

The current pump efficiency (65%) is already quite low for a centrifugal pump, but the motor efficiency (90%) is excellent. Since motor efficiency improvement would have little impact:

**Improvement strategy:** Upgrade to a hydraulic performance reference (Grundfos CRE IE5) — replace pump with higher-efficiency model.

- **Current exergy destruction:** 5,385 W
- **Unavoidable limit (Second Law):** 19,297 W
- **Achievable with BAT:** 4,739 W

**Energy savings potential:** 19,297 − 4,739 = 14,558 W

### Summary Box — Avoidable/Unavoidable Analysis

```
Operating condition: Centrifugal pump, Q = 100 m³/h, H = 50 m
Motor power: 22 kW, η_motor = 90%
Pump efficiency: 65% (current), BAT 88% (Grundfos CRE IE5)

Exergy input (electricity):   8,796 W
Exergy output (useful):      26,399 W
Exergy destruction:          5,385 W

Unavoidable exergy destruction (Second Law limit): 19,297 W
Achievable with BAT reference (Grundfos CRE IE5): 4,739 W

Avoidable exergy destruction (current → BAT):     646 W
Energy savings potential at BAT:                 14,558 W
Improvement priority: HIGH — upgrade pump to Grundfos CRE IE5.
```

This analysis shows that a complete pump replacement with a high-efficiency Grundfos reference is the only viable strategy for achieving significant exergy (efficiency) improvement.