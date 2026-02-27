# avun-turbine-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 57.9s | Checks: 4/4

# Exergy Destruction Analysis: Back-Pressure Steam Turbine

## Operating Conditions
- **Inlet pressure:** \( p_1 = 20 \) bar = 2.0 MPa
- **Inlet temperature:** \( T_1 = 300^\circ\text{C} \)
- **Outlet pressure:** \( p_2 = 3 \) bar = 0.3 MPa
- **Steam mass flow rate:** \( \dot{m} = 4 \) kg/s
- **Isentropic efficiency:** η_is = 72%
- **Generator efficiency:** η_gen = 93%
- **Operating condition:** full_load

## Assumptions
1. Steady-state, steady-flow (SSSF) operation.
2. Steam properties from IAPWS-IF97 steam tables.
3. Kinetic and potential exergy changes are negligible.
4. No heat loss to surroundings from turbine casing (adiabatic boundary).
5. Exergy of electricity = work product since this is a back-pressure turbine delivering shaft power.

## Step 1: Steam Properties at Inlet (State 1)

**T_1 = 300°C, p_1 = 2.0 MPa**

From steam tables at 20 bar (2.0 MPa):
- Saturation temperature \( T_{sat} = 158.86^\circ\text{C} \)
Since \( T_1 = 300^\circ\text{C} > T_{sat} \), the steam is superheated.

Superheated steam at 2.0 MPa, 300°C:
- Specific volume: \( v_1 = 0.8579 \) m³/kg
- Specific entropy: \( s_1 = 6.4620 \) kJ/(kg·K)
- Specific exergy: \( e_x(1) = 138.69 + (300 - 100) × 0.001104 = 138.69 + 200.54 = 339.23 \) kJ/kg
- Enthalpy: \( h_1 = 2788.6 \) kJ/kg
- Entropy: \( s_1 = 6.4620 \) kJ/(kg·K)

**Thermal exergy at inlet (state 1):**
\[ \overline{Ex}_x(1) = \dot{m} × e_x(1) = 4 × 339.23 = 1,356.92 \text{ kW} \]

## Step 2: Steam Properties at Outlet (State 2s — Isentropic Exit)

**p_2 = 0.3 MPa (3 bar), s_2s = s_1 = 6.4620 kJ/(kg·K)**

From steam tables at 3 bar:
- Saturation temperature: \( T_{sat} = 133.52^\circ\text{C} \)
- Specific volume: \( v_f = 0.0010896 \) m³/kg, \( v_g = 4.4709 \) m³/kg
- Specific entropy: \( s_f = 0.5312 \), \( s_g = 7.6217 \)

Since \( s_2s < s_g \) at 0.3 MPa, the state is subcooled liquid.
From the compressed liquid table at 0.3 MPa:
- Specific volume: \( v_f = 0.0010896 \) m³/kg
- Specific enthalpy: \( h_f = 442.57 \) kJ/kg

**Isentropic outlet state (2s):**
- \( s_{2s} = s_1 = 6.4620 \)
This is the entropy of compressed liquid at 3 bar.
- Specific volume: \( v_{2s} = v_f = 0.0010896 \) m³/kg
- Specific enthalpy: \( h_{2s} = 442.57 \) kJ/kg

**Isentropic work output (state 2s):**
\[ W_{is} = \dot{m} × (h_1 - h_{2s}) = 4 × (2,788.60 - 442.57) = 9,346.08 \text{ kW} \]

## Step 3: Actual Outlet State (State 2)

Using energy balance on the turbine:
\[ h_2 + v_2 × p_2 = h_1 - w_{is} \]
\[ h_2 + 0.0010896 × 300,000 = 2,788.60 - 9,346.08 \]
\[ h_2 + 326.88 = 1,852.52 \]
\[ h_2 = 1,525.64 \text{ kJ/kg} \]

**Actual outlet specific entropy:**
From steam tables at 3 bar:
- \( s_f = 0.5312 \), \( s_g = 7.6217 \)
Since the actual state is somewhere between compressed liquid and superheated, we interpolate to find the actual entropy.

Using the energy balance (entropy-based) method:
\[ s_2 = \frac{v_2 × h_1 - v_f × h_f}{h_1 - h_f} + s_f \]
From steam tables at 3 bar, for a subcooled liquid state near the saturation line, we estimate \( s_2 ≈ 0.5687 \) kJ/(kg·K).

**Thermal exergy at outlet (state 2):**
\[ e_x(2) = h_1 - T_0 × v_2 + T_0 × v_f - s_2 × v_2 \]
Using the same reference temperature \( T_0 = 25^\circ\text{C} = 298.15 K \):
\[ e_x(2) = 2,788.60 - 298.15 × 0.341 + (298.15 × 0.0010896 + 6.4620) × 0.341 \]
\[ e_x(2) = 2,788.60 - 102.14 + 2.36 \]
\[ e_x(2) = 2,688.82 \text{ kJ/kg} \]

**Actual exergy output:**
\[ Ex_2 = \dot{m} × e_x(2) = 4 × (2,688.82 - 1,525.64) = 4 × 1,163.18 = 4,652.72 \text{ kW} \]

## Step 4: Generator and Total Exergy Destruction

**Useful electrical output (generator efficiency):**
\[ P_{elec,out} = η_gen × W_{mech} = 0.93 × 9,346.08 = 8,675.21 \text{ kW} \]

**Total exergy destruction:**
```
Ex_d = Ex_1 - Ex_2
Ex_d = (1,356.92 + 9,346.08) - 4,652.72 = 7,050.28 kW
```

**Generator efficiency verification:**
\[ η_gen = \frac{P_{elec,out}}{W_{mech}} = \frac{8,675.21}{9,346.08} = 0.929 ≈ 93% \]

## Step 5: Unavoidable and Avoidable Decomposition (Reference BAT)

**BAT isoperformance condition:** η_is = 90%, η_gen = 98%

### BAT Isentropic Turbine Output
\[ W_{is,BAT} = \dot{m} × (h_1 - h_{2,BAT}) \]
From the energy balance at BAT:
```
h_2,BAT + v_2,BAT × p_2 = h_1 - 9,346.08
h_2,BAT + 0.0010896 × 300,000 = 2,788.60 - 9,346.08
h_2,BAT + 326.88 = 1,852.52
h_2,BAT = 1,525.64 kJ/kg

s_2,BAT: From BAT steam tables at 3 bar, s_f = 0.5312, s_g = 7.6217 → s_2 ≈ 0.5687
```

**BAT useful output (generator efficiency):**
\[ P_{elec,out,BAT} = η_gen × W_{is,BAT} = 0.98 × 9,346.08 = 9,160.20 \text{ kW} \]

**Unavoidable exergy destruction:**
```
Ex_d,unav = Ex_1 - P_{elec,out,BAT}/η_gen
Ex_d,unav = (1,356.92 + 9,346.08) - (9,160.20 / 0.98)
Ex_d,unav = 10,702.90 - 9,346.08 = 1,356.92 kW
```

### Avoidable Exergy Destruction

```
Ex_d,avoid = Ex_d - Ex_d,unav
Ex_d,avoid = 7,050.28 - 1,356.92 = 5,693.36 kW
```

**Avoidable / Unavoidable ratio:**
\[ \frac{Ex_{d,avoid}}{Ex_{d,unav}} = \frac{5,693.36}{1,356.92} = 4.20 \]

## Summary

### Exergy Balance
```
Ex_in  = 10,702.90 kW
Ex_out = 8,675.21 kW
Ex_d   = 7,050.28 kW
Ex_x(1) = 1,356.92 kW (thermal)
Ex_x(2) = 4,652.72 kW (thermal)
```

### BAT Reference
- Unavoidable: 1,356.92 kW
- Avoidable: 5,693.36 kW

### Improvement Priority
**High priority:** Reduce the large avoidable component of 5,693.36 kW.

**Achievable savings:** At full_load, reducing avoidable exergy by 10% would save 569.34 kW (5,693.36 × 0.1).

**Technology upgrade options:**
- Optimized blade design
- Improved steam-side fouling control
- Higher stage count or advanced aerodynamic measures

By focusing on these measures, it is possible to bring the avoidable component closer to the BAT reference value of 1,356.92 kW.

### Final Assessment
**Avoidable:** 5,693.36 kW (74%)
**Unavoidable:** 1,356.92 kW (18%)
**Improvement priority: Medium-High**

With targeted optimization efforts, the avoidable fraction can be reduced significantly to approach BAT levels.