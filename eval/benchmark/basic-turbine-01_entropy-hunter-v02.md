# basic-turbine-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 66.9s | Checks: 4/4

## Exergy Analysis: Back-Pressure Steam Turbine (Full Load)

### Assumptions
1. Steady-state, steady-flow operation.
2. Kinetic and potential exergy changes are negligible.
3. Steam properties from IAPWS-IF97 steam tables.
4. No heat loss to surroundings (adiabatic casing assumption for back-pressure).
5. Exergy of electricity = electrical work delivered at the shaft.
6. Chemical exergy of water is zero (no composition change).

---

### Step 1: State Properties

**Inlet state (State 1): P₁ = 40 bar, T₁ = 400°C**

From steam tables at 40 bar and 400°C:
```
h₁ = 3261.8 kJ/kg
s₁ = 7.2965 kJ/(kg·K)
```

**Isentropic outlet state (State 2s): P₂ = 4 bar, s₂s = s₁**

From steam tables at 4 bar:
- At saturated liquid: T_sat = 130°C, h_fg = 1891.5 kJ/kg, s_f = 0.5670, s_g = 7.2825
- At superheated state with s = 7.2965: h₂s = 3164.9 kJ/kg

Since s₁ > s_f at 4 bar (saturated state), the outlet is **superheated**.

**Checking for feasibility:**
```
h₂s - h_g(40bar) = 3164.9 - 2735.0 = 429.9 kJ/kg
```

The specified s₁ = 7.2965 is feasible since the isentropic outlet temperature will be above 4 bar saturation.

From steam tables at P₂ = 4 bar, T = 180°C (actual state):
```
h_g(4bar) = 3164.9 kJ/kg
s_g(4bar) = 7.2825 kJ/(kg·K)
```

At 4 bar, 180°C:
```
h₂ = 2849.8 kJ/kg
s₂ = 7.3063 kJ/(kg·K)
```

**Verification:**
```
s₁ = 7.2965 < s_g(4bar) = 7.2825 (unrealistic, s₂ should be > 7.2825 for superheated state at 4 bar)
```

Since the problem statement specifies 78% isentropic efficiency and T₁ = 400°C, we need to calculate the actual isentropic outlet temperature.

Using energy balance on turbine (with isentropic approximation):
```
h₁ - h₂s = ṁ × Q_turb
Q_turb = ṁ × (h₁ - h₂s) = 5 × (3261.8 - 3164.9) = 504.5 kJ/kg

Energy exergy:
Ex_in = ṁ × (h₁ - T₀/(T_sat(4bar)) × s₁)
Ex_out = ṁ × (h₂s - T₀/(T_sat(4bar)) × s₂s)

Ex_is = ṁ × (h₁ - h₂s) = 504.5 kJ/kg
```

Revisiting with isentropic temperature:

```
T_sat(4bar) = 130°C → T₀/T_sat = 473/303 = 1.562

Ex_is = ṁ × (h₁ - h₂s + s₂s/(R·T₀/T_sat)) = 5 × (3261.8 - 3164.9 + 7.2825 / 0.004615) = 504.5 + 62.9 = 567.4
```

---

### Step 2: Actual Outlet State

From energy balance:
```
h₂ = h₁ - ṁ × (h₁ - h₂s)
h₂ = 3261.8 - 5 × (3261.8 - 3164.9) = 3261.8 - 504.5 = 2757.3 kJ/kg
```

At P₂ = 4 bar, T_sat = 130°C:
```
h_f(4bar) = 940.9 kJ/kg, h_fg = 2269.8 kJ/kg

Actual quality: x = (h₂ - h_f) / h_fg = (2757.3 - 940.9) / 2269.8 = 0.813
```

From steam tables at P₂ = 4 bar, T ≈ 180°C:
```
h = h_f + x × h_fg = 940.9 + 0.813 × 2269.8 = 940.9 + 1853.7 = 2794.6 kJ/kg
s = s_f + x × s_fg = 0.446 + 0.813 × 5.653 = 0.446 + 4.605 = 5.051 kJ/(kg·K)
```

**Actual state:** h₂ = 2794.6 kJ/kg, s₂ = 5.051 kJ/(kg·K)

---

### Step 3: Energy and Exergy Calculations

**Mass flow energy input:**
```
Ė_in = ṁ × (h₁ - h_f) = 5 × (3261.8 - 940.9) = 5 × 2320.9 = 11,604.5 kW
```

**Actual work output:**
```
Ė_turb = ṁ × (h₁ - h₂) = 5 × (3261.8 - 2794.6) = 5 × 467.2 = 2,336.0 kW
```

**Generator output:**
```
Ė_gen = η_gen × Ė_turb = 0.95 × 2,336.0 = 2,224.2 kW
```

**Isentropic work:**
```
Ė_is = ṁ × (h₁ - h₂s) = 5 × (3261.8 - 3164.9) = 504.5 kW
```

**Thermal exergy efficiency:**
```
η_ex = Ė_turb / Ė_in = 2,336.0 / 11,604.5 × 100 = 20.0%
```

---

### Step 4: Exergy Balance

**Total exergy input (at T₀):**
```
Ex_in = ṁ × (h₁ - T₀/(T_sat(4bar)) × s₁)
Ex_in = 5 × (3261.8 - 1.562 × 7.2965) = 5 × (3261.8 - 11.40) = 5 × 3250.4 = 16,252.0 kW
```

**Actual exergy output:**
```
Ex_out = ṁ × (h₂ - T₀/(T_sat(4bar)) × s₂)
Ex_out = 5 × (2794.6 - 1.562 × 5.051) = 5 × (2794.6 - 7.87) = 5 × 2,786.8 = 13,934.0 kW
```

**Isentropic exergy output:**
```
Ex_is = ṁ × (h₂s - T₀/(T_sat(4bar)) × s₂s)
Ex_is = 5 × (3164.9 - 1.562 × 7.2825) = 5 × (3164.9 - 11.37) = 5 × 3,153.5 = 15,767.5 kW
```

**Exergy loss:**
```
Ex_loss = Ex_in − Ex_out = 16,252.0 − 13,934.0 = 2,318.0 kW
```

**Generator irreversibility (electrical-to-shaft):**
```
Ex_gen = Ė_gen / η_gen − Ė_turb = 2,224.2 / 0.95 − 2,336.0 = 2,342.3 − 2,336.0 = 6.3 kW
```

**Total irreversibility:**
```
Ex irr = Ex_loss + Ex_gen = 2,318.0 + 6.3 = 2,324.3 kW
```

**Efficiency ratios:**
```
η_ex = Ė_turb / Ė_in = 2,336.0 / 11,604.5 × 100 = 20.0%
η_is = Ė_is / Ė_in = 15,767.5 / 11,604.5 × 100 = 136.0% (isentropic efficiency is the ratio of actual to ideal work)
```

---

### Step 5: Summary Table

| **Item**             | **Value**       | **Unit** |
|----------------------|-----------------|----------|
| **Inlet conditions:**     |                |          |
| Pressure, P₁           | 40.000         | bar      |
| Temperature, T₁        | 400.000        | °C       |
| Mass flow rate, ṁ      | 5.000          | kg/s     |

| **Outlet conditions:**    |                |          |
| Pressure, P₂            | 4.000          | bar      |
| Exergy-out (actual)     | 13,934.0       | kW      |
| Isentropic exergy-out   | 15,768.0       | kW      |
| Isentropic efficiency   | 78.0%          |         |
| Thermal efficiency      | 20.0%          |         |

| **Energy balance:**            |                |          |
| Energy input (exergy basis)    | 16,252.0       | kW      |
| Turbine output                 | 2,336.0        | kW      |
| Generator efficiency           | 95%            |         |
| Electrical output              | 2,224.2        | kW      |

| **Exergy balance:**             |                |          |
| Total exergy input (exergy)    | 16,252.0       | kW      |
| Actual exergy output           | 13,934.0       | kW      |
| Isentropic exergy output       | 15,768.0       | kW      |
| Exergy loss                    | 2,318.0        | kW      |
| Generator irreversibility      | 6.3            | kW      |
| Total irreversibility          | 2,324.3        | kW      |

| **Efficiency ratio:**           |                |          |
| Isentropic efficiency (η_is)   | 78%            |         |
| Carnot efficiency (COP_ideal)  | 1 - T₂/T₁ = 0.602 |         |
| Thermal efficiency (η_th)      | 20%            |         |

---

### Step 6: Recommendations

**1. Improve isentropic efficiency:** The current isentropic efficiency of 78% is already quite good for a back-pressure turbine. However, further optimization can be achieved through:
   - Optimizing steam-side fouling removal.
   - Adjusting blade clearances and blade design.
   - Using advanced control strategies to reduce internal losses.

**2. Reduce generator losses:** The generator efficiency of 95% is excellent; however, continuous monitoring and maintenance are required to keep it at peak performance levels.

**3. Waste heat utilization:** The back-pressure turbine rejects significant thermal energy at the outlet (4 bar). Installing a waste heat recovery boiler or heat exchanger can capture this residual thermal energy for useful processes such as:
   - Process heating.
   - Absorption chillers.
   - De-superheating feedwater.

**4. Increase overall facility efficiency:** The back-pressure turbine operates with low steam flow, producing modest shaft power at full load (2.3 kW). Consider if upgrading to a higher capacity back-pressure or extracting more useful heat from the condensate stream could improve overall thermal-to-electricity conversion efficiency.

---

**Conclusion:**
The back-pressure steam turbine is operating efficiently for its intended purpose with an actual η_th = 20% and high generator efficiency. Further optimization efforts should focus on maintaining/raising the isentropic efficiency while maximizing useful energy recovery from the exhaust stream.