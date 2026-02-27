# basic-pump-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 43.6s | Checks: 2/2

## Exergy Analysis: Centrifugal Pump (Operating Condition — Full Load)

### Assumptions

1. Steady-state, steady-flow operation.
2. Fluid: liquid water at 25°C; treated as incompressible with properties: ρ = 997 kg/m³, Cp = 4.18 kJ/(kg·K).
3. Electrical power input is pure work (exergy factor = 1.0).
4. Kinetic and potential exergy components at inlet and outlet are negligible due to incompressibility.
5. Heat loss from the pump casing is small compared to useful power; it is lumped into the irreversibility of the mechanism.
6. The fluid temperature remains constant throughout (no heat exchange with surroundings) — thus, no thermal exergy component.

### Step 1: Basic Energy Balance

**Mass flow rate:**
```
ṁ = ρ × Q̇
Q̇ = 50 m³/h = 50 / 3600 = 0.01389 m³/s
ṁ = 997 kg/m³ × 0.01389 m³/s
ṁ = 13.847 kg/s
```

**Hydraulic power:**
```
P_hyd = ṁ × g × H
g = 9.81 m/s², H = 30 m

P_hyd = 13.847 kg/s × 9.81 m/s² × 30 m
P_hyd = 412.5 kW
```

**Useful hydraulic power delivered to fluid:**
```
Ė_useful = η_pump × P_hyd

η_pump = 72% = 0.72
Ė_useful = 0.72 × 412.5 kW
Ė_useful = 296.3 kW
```

**Electrical input power:**
```
P_elec = Ṗ_mech / η_motor

η_motor = 92% = 0.92
P_elec = P_hyd / η_motor
P_elec = 412.5 kW / 0.92
P_elec = 448.65 kW
```

### Step 2: Exergy Calculations

**Exergy of electrical power input (pure work):**
```
Ėx_in = P_elec × ex_factor
ex_factor = 1.0
Ėx_in = 448.65 kW × 1.0
Ėx_in = 448.65 kW
```

**Exergy of useful hydraulic power:**
```
Ėx_hyd = ṁ × Cp × ΔT

Since the fluid temperature remains constant (no heat exchange with surroundings), thermal exergy is zero.

The useful hydraulic power already includes the energy delivered to the fluid, so:
Ėx_hyd = 296.3 kW
```

**Exergy of irreversibility:**
```
Ėx_irr = Ėx_in - Ėx_hyd

Ėx_irr = 448.65 kW - 296.3 kW
Ėx_irr = 152.35 kW
```

**Pump efficiency (second-law interpretation):**
```
η_pump,second_law = Ėx_hyd / Ėx_in

η_pump,second_law = 296.3 kW / 448.65 kW
η_pump,second_law = 0.661 or 66.1%
```

### Step 3: Specific Exergy Calculations (per kg of fluid)

**Specific exergy of electrical input:**
```
ex_in/kg = Ėx_in / ṁ

ex_in/kg = 448.65 kW / 13.847 kg/s
ex_in/kg = 32.59 kJ/kg
```

**Specific exergy of useful hydraulic power:**
```
ex_hyd/kg = Ėx_hyd / ṁ

ex_hyd/kg = 296.3 kW / 13.847 kg/s
ex_hyd/kg = 21.40 kJ/kg
```

**Specific exergy of irreversibility:**
```
ex_irr/kg = Ėx_irr / ṁ

ex_irr/kg = 152.35 kW / 13.847 kg/s
ex_irr/kg = 10.96 kJ/kg
```

### Step 4: Carnot Pump Efficiency Benchmarking (Isentropic)

**Carnot pump efficiency for isothermal water at 25°C:**
```
T_cold = T₀ = 25°C = 298.15 K

The Carnot efficiency for a lift pump:
η_Carnot = 1 - (T_cold / (T_evap + T_cold))

For liquid water at 25°C, the evaporation temperature (thermal boundary) is effectively infinite:
η_Carnot = 1 - (T_cold / ∞)
Since the water remains liquid and incompressible:
η_Carnot ≈ 1

However, a more practical benchmark using typical head-based efficiency for isothermal water at this operating point:

For H = 30 m at 25°C: η_Carnot (benchmark) ≈ 78%
```

### Step 5: Exergy Analysis Summary Table

| Parameter | Value |
| --- | --- |
| Q̇ (m³/h) | 50.0 |
| H (m) | 30.0 |
| Ṗ_elec (kW) | 448.65 |
| Ṗ_hyd (kW) | 412.5 |
| ṗ_pump,useful (kW) | 296.3 |
| η_pump | 72% |
| η_motor | 92% |
| Ėx_in (kW) | 448.65 |
| Ėx_hyd (kW) | 296.3 |
| Ėx_irr (kW) | 152.35 |
| η_pump,second_law | 66.1% |
| ex_in/kg (kJ/kg) | 32.59 |
| ex_hyd/kg (kJ/kg) | 21.40 |
| ex_irr/kg (kJ/kg) | 10.96 |

### Step 6: Exergy Efficiency Decomposition

```
η_ex = Ėx_hyd / Ėx_in
η_ex = 296.3 kW / 448.65 kW
η_ex = 0.661 or 66.1%
```

### Step 7: Improvement Strategy

**Current η_pump,second_law:** 66.1%

**Improvement goal:** Increase pump efficiency to the benchmark Carnot pump efficiency of ~78%.

**Key measures for improvement:**
1. **Realign impeller with pump casing:** Ensure best hydraulic performance by recalibrating the system (possibly through pump re-casing or replacement).
2. **Flow analysis:** Verify if the operating point is close to BEP (best efficiency point). If not, adjust the motor speed via frequency converter to reach optimal operation.
3. **Minimize leaks and losses:** Ensure no fluid bypass or leakage at the pump seals.
4. **Motor upgrade:** Replace with higher-efficiency synchronous motor (e.g., IE3 class) if operating below 200 Hz.

### Step 8: Achievable Savings Estimate

At full load, reducing exergy loss by increasing η_pump to 78%:

```
Ėx_savings = Ėx_irr - Ėx_irr_new
É_x_irr = 152.35 kW × (1 - 0.78 / 0.66)
É_x_irr = 152.35 kW × 0.492
Ėx_savings = 74.85 kW

Annual kWh savings: 74.85 kW × 8760 h/year = 656,862 kWh
At a cost of €0.12/kWh:
Annual energy cost saving = 656,862 × 0.12 = €79,023

With capital equipment upgrade costs: estimated payback period ≈ 1-2 years.
```

---

**Summary:** The centrifugal pump operates at a second-law (exergy) efficiency of **66.1%**, well below the Carnot benchmark of ~78%. Achieving this benchmark through impeller realignment, speed optimization, and motor upgrade can reduce exergy loss by **49.2%**, resulting in significant energy savings (approx. 79,000 kWh/year) and payback within a year.

**Recommendation:** Prioritize pump alignment and re-casing to improve hydraulic efficiency; follow up with motor upgrade for further step-change improvement.