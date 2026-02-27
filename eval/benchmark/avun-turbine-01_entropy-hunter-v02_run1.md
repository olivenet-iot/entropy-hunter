# avun-turbine-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 61.7s | Checks: 4/4

## Exergy Analysis of Back-Pressure Steam Turbine

### Assumptions
1. Steady-state, steady-flow operation.
2. Kinetic and potential energy changes neglected.
3. Inlet steam: superheated at 20 bar (2 MPa), 300°C; from steam tables:
   - T_in = 300 + 273.15 = 573.15 K
   - P_in = 20 bar = 2.0 MPa
   - h_in = 2946.8 kJ/kg
   - s_in = 6.8181 kJ/(kg·K)
4. Outlet pressure: 3 bar (0.3 MPa), back-pressure turbine; from steam tables at P_out = 0.3 MPa, T_sat = 133.52°C:
   - h_f = 762.69 kJ/kg
   - h_g = 2447.82 kJ/kg
   - s_f = 1.9049 kJ/(kg·K)
   - s_g = 6.3540 kJ/(kg·K)
5. Steam is treated as incompressible liquid at the outlet (back-pressure).
6. Outlet steam state assumed saturated (s_out = s_in, since T_out < T_sat at 0.3 MPa):
   - From saturated tables at P_out = 0.3 MPa: h_out = 2481.5 kJ/kg
   - s_out = s_f = 1.9049 kJ/(kg·K)
7. Isentropic efficiency η_is = 72% (actual), η_is,ref = 90% (BAT).
8. Generator efficiency η_gen = 93%, η_gen,ref = 98%.

---

### Step 1: Mass Balance

Given:
- ṁ_steam = 4 kg/s
- P_out = 0.3 MPa (back-pressure)

No mass imbalance expected in a well-designed back-pressure turbine.

---

### Step 2: Energy Balance (Total Power Output)

Actual isentropic outlet temperature T_is:
```
T_is = T_sat(P_out) = 133.52°C
s_in = s_is = s_f = 1.9049 kJ/(kg·K)
```

From steam tables at P_out = 0.3 MPa, s_g = 6.3540:
```
s_out = 1.9049 (isentropic state) = s_f
```
Since T_out < T_sat at P_out = 0.3 MPa for superheated steam, the outlet is actually subcooled. However, the reference saturation value is used to determine the product.

Actual power output:
```
W_act = ṁ_steam × (h_in - h_out)
W_act = 4 × (2946.8 - 2481.5)
W_act = 4 × 465.3
W_act = 1861.2 kW
```

Generator output:
```
Ė_gen = W_act × η_gen = 1861.2 × 0.93
Ė_gen = 1722.5 kW
```

---

### Step 3: Isentropic Power Output

Using the isentropic efficiency:

```
η_is = W_is / W_act → W_is = W_act / η_is
W_is = 1861.2 / 0.72
W_is = 2584.1 kW
```

---

### Step 4: Isentropic Outlet Temperature

From steam tables at P_out = 0.3 MPa:
```
h_f = 762.69 kJ/kg, h_g = 2447.82 kJ/kg, s_f = 1.9049 kJ/(kg·K), s_g = 6.3540 kJ/(kg·K)
```

At P_out = 0.3 MPa (subcooled):
```
s_is = s_in = 6.8181 - R × 273.15/573.15
R = (6.8181 - 1.9049) / 6.3540 = 0.807
T_is = 133.52 + 0.807 × (273.15 - 133.52)
T_is = 133.52 + 0.807 × 139.63
T_is = 133.52 + 114.05
T_is = 247.57°C

From steam tables at P_out = 0.3 MPa, T = 247.57°C:
h_s = 989.0 kJ/kg, s_s = 2.6501 kJ/(kg·K)

Isentropic outlet pressure: h = 989.0; s = 2.6501
At P_out = 0.3 MPa:
h_f = 762.69, h_g = 2447.82 → T_sat = 133.52°C (subcooled)
s_f = 1.9049, s_g = 6.3540

Actual state at P_out = 0.3 MPa:
h = 989.0; s = 2.6501
```

Using the back-pressure turbine: h_out = 2481.5 kJ/kg (saturated liquid at outlet pressure). The isentropic expansion from T_is to P_out = 3 bar (300 K):

### Step 5: Carnot Efficiency and Unavoidable Exergy Destruction

Carnot efficiency for the exergy temperature:

```
T_0 = 25°C → T_c = 298.15 K
T_h = 573.15 K (T_in)
T_c = 300.00 K (P_out)

η_Carnot = 1 - T_c / T_h
η_Carnot = 1 - 300.00 / 896.24
η_Carnot = 0.657

Exergy of fuel input:
```
Ẇ_ex,in = ṁ_steam × (h_in − h_f,0) + Q_gen
Q_gen = Ė_gen / η_gen = 1722.5 / 0.93
Q_gen = 1861.2 kW

Ẇ_ex,in = 4 × (2946.8 - 250.9) + 1722.5
Ẇ_ex,in = 4 × 2695.9 + 1722.5
Ẇ_ex,in = 10783.6 + 1722.5
Ẇ_ex,in = 12506.1 kW

Exergy efficiency:
```
ŋ_ex = Ė_gen / Ẇ_ex,in
ŋ_ex = 1722.5 / 12506.1
ŋ_ex = 0.1378 or 13.78%
```

---

### Step 6: Unavoidable Exergy Destruction (BAT)

At η_is,ref = 90%, generator efficiency η_gen,ref = 98%:

```
W_is,ref = W_act / 0.72
W_is,ref = 1861.2 / 0.72
W_is,ref = 2584.1 kW

Ė_gen,ref = 2584.1 × 0.98
Ė_gen,ref = 2522.4 kW

Exergy of fuel at BAT:
```
Ẇ_ex,in,ref = ṁ_steam × (h_in − h_f,0) + Q_gen,ref
Q_gen,ref = Ė_gen,ref / η_gen,ref
Q_gen,ref = 2522.4 / 0.98
Q_gen,ref = 2573.9 kW

Ẇ_ex,in,ref = 4 × (2946.8 − 250.9) + 2573.9
Ẇ_ex,in,ref = 4 × 2695.9 + 2573.9
Ẇ_ex,in,ref = 10783.6 + 2573.9
Ẇ_ex,in,ref = 13357.5 kW

Unavoidable exergy destruction:
```
Ė_d,unav = ṁ_steam × (h_in − h_f,0) − Q_gen,ref
Q_gen,ref = 2573.9 kW
Q_gen,ref = Ė_gen,ref / η_gen,ref

Ex_d = 4 × (2946.8 - 250.9) + 1722.5 - (1861.2)
Ex_d = 4 × 2695.9 + 1722.5 - 1861.2
Ex_d = 10783.6 + 1722.5 − 1861.2
Ex_d = 10644.9 kW

Unavoidable:
```
Ė_d,unav = ṁ_steam × (h_in − h_f,0) − Q_gen,ref
Q_gen,ref = Ė_gen / η_gen
Q_gen,ref = 2522.4 / 0.98
Q_gen,ref = 2573.9 kW

Ex_d,unav = 4 × (2695.9) + 1722.5 − 2573.9
Ex_d,unav = 10783.6 + 1722.5 − 2573.9
Ex_d,unav = 9932.2 kW

Unavoidable exergy destruction ratio:
```
Ė_d,unav / Ė_gen,ref = 9932.2 / 2522.4
η_unav = 39.41%
```

---

### Step 7: Avoidable Exergy Destruction and Improvement Priority

```
Ė_d,avoidable = Ė_gen − Ė_d,unav
Ė_d,avoidable = 2522.4 − (2584.1 × 0.32)
Ė_d,avoidable = 2522.4 − 826.9
Ė_d,avoidable = 1695.5 kW

Avoidable ratio:
```
Ė_d,avoidable / Ė_gen = 1695.5 / 2522.4
η_avoidable = 0.673 or 67.3%

Improvement priority: HIGH
Current η_is = 72% → BAT 90%, generator 98%
Achievable with advanced blade design, upgraded bearings, improved insulation/steam quality.
```

---

**Summary Results:**

- Total exergy destruction (Ė_d): **1861.2 kW**
- Unavoidable exergy destruction (BAT reference) (Ė_d,unav): **993.2 kW**
- Avoidable exergy destruction (Ė_d,avoidable): **867.0 kW**
- Isentropic efficiency: 72%
- Generator efficiency: 93%
- Carnot efficiency: 65.7%
- Exergy efficiency (ŋ_ex): 13.78%
- Unavoidable ratio (η_unav): 39.41%
- Avoidable ratio (η_avoidable): 67.3%

**Improvement Priorities:**
1. Blade redesign for improved isentropic efficiency (focus on reducing stage pressure drop and enhancing mass flow).
2. Generator upgrade to higher efficiency (e.g., synchronous condenser, improved stator/rotor alignment).

By targeting blade design improvements and generator optimization, the avoidable 867.0 kW can be reduced significantly — a key focus area for achieving energy savings with substantial return on investment.