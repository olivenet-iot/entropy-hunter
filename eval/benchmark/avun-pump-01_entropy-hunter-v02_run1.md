# avun-pump-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 31.8s | Checks: 3/4

## Exergy Analysis of Centrifugal Pump — Pump Set

### Operating Conditions

**Operating mode:** Full load / design point

**Fluid:** Water at 25°C (ρ = 997 kg/m³, Cp = 4.18 kJ/(kg·K), v = 0.001004 m³/kg)
**Volume flow rate:** Q = 100 m³/h = 0.02778 m³/s
**Total head:** H = 50 m
**Motor power input:** P_elec = 22 kW
**Pump efficiency:** η_pump = 65%
**Motor efficiency:** η_motor = 90%

### Step 1: Mass Flow Rate

```
ṁ = ρ × Q
ṁ = 997 kg/m³ × 0.02778 m³/s
ṁ = 27.703 kg/s
```

### Step 2: Hydraulic Power (Useful Work)

```
P_hyd = ṁ × g × H
P_hyd = 27.703 kg/s × 9.807 m/s² × 50 m
P_hyd = 136,298 W = 136.3 kW
```

### Step 3: Actual Electrical Power Input

```
P_elec = P_hyd / η_pump
P_elec = 136,298 W / 0.65
P_elec = 209,764 W = 209.8 kW
```

### Step 4: Motor Electrical Input (Verification)

```
P_motor = P_elec / η_motor
P_motor = 209,764 W / 0.90
P_motor = 233,071 W = 233.1 kW

Since the motor input is not given directly: We use this value for further calculations.
```

### Step 5: Electrical Exergy Input (First Law)

```
Ex_in = P_motor × η_el
Ex_in = 233,071 W × 1
Ex_in = 233.1 kW
```

### Step 6: Useful Work (Hydraulic Exergy) — Output

```
Ex_useful = ṁ × g × H
Ex_useful = 27.703 kg/s × 9.807 m/s² × 50 m
Ex_useful = 136,298 W = 136.3 kW
```

### Step 7: Total Exergy Destruction

```
Ex_dstr = Ex_in - Ex_useful
Ex_dstr = 233.1 kW - 136.3 kW
Ex_dstr = 96.8 kW
```

### Step 8: Avoidable / Unavoidable Decomposition (BAT Reference)

First, calculate the BAT operating point:

**BAT pump efficiency:** η_pump,BAT = 88%
**BAT motor efficiency:** η_motor,BAT = 97%

```
P_hyd_BAT = ṁ × g × H
P_hyd_BAT = 27.703 kg/s × 9.807 m/s² × 50 m
P_hyd_BAT = 136,298 W

P_elec,BAT = P_hyd_BAT / η_pump,BAT
P_elec,BAT = 136,298 W / 0.88
P_elec,BAT = 154,795 W = 154.8 kW

Ex_in,BAT = P_motor,BAT × η_el
Ex_in,BAT = 154,795 W × 1
Ex_in,BAT = 154.8 kW

Ex_useful_BAT = ṁ × g × H (same as above)
Ex_useful_BAT = 136,298 W = 136.3 kW

Ex_dstr,BAT = Ex_in,BAT - Ex_useful_BAT
Ex_dstr,BAT = 154.8 kW - 136.3 kW
Ex_dstr,BAT = 18.5 kW
```

**Unavoidable exergy destruction (BAT reference):**
```
Ex_dstr,unav = ṁ × g × H × (1 - η_pump,BAT)
Ex_dstr,unav = 27.703 kg/s × 9.807 m/s² × 50 m × (1 - 0.88)
Ex_dstr,unav = 136,298 W × 0.12
Ex_dstr,unav = 16,356 W = 16.4 kW
```

**Avoidable exergy destruction:**
```
Ex_dstr,avoid = Ex_dstr - Ex_dstr,unav
Ex_dstr,avoid = 96.8 kW - 16.4 kW
Ex_dstr,avoid = 80.4 kW
```

### Step 9: Avoidable / Unavoidable Split

**Unavoidable:** 16.4 kW (BAT reference)
**Avoidable:** 80.4 kW (improvable through efficiency enhancement)

### Step 10: Improvement Priority

Since the current pump efficiency is subpar at 65% while BAT offers an impressive 88%, this pump set should be a high priority for upgrade. The achievable reduction in exergy destruction with BAT-level optimization:

```
ΔEx_dstr = Ex_dstr - Ex_dstr,BAT
ΔEx_dstr = 96.8 kW - 18.5 kW
ΔEx_dstr = 78.3 kW

This represents a **40% reduction** in total exergy destruction with state-of-the-art equipment, which is very significant for industrial facilities.
```

### Summary

- **Total exergy destruction:** 96.8 kW
- **Unavoidable (BAT reference):** 16.4 kW
- **Avoidable:** 80.4 kW
- **Improvement priority:** HIGH — Upgrade to pump and motor combination at least matching BAT level of 88% pump efficiency and 97% motor efficiency.

Upgrade action is strongly recommended for significant energy savings (avoidable = 80.4 kW) and compliance with advanced standards such as IE5 premium motors.