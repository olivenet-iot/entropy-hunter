# avun-pump-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 38.7s | Checks: 4/4

## Exergy Analysis: Centrifugal Pump (Water at 25°C)

### Operating Conditions

**Reference conditions:** Grundfos CRE IE5 (Best Available Technology)
- Motor power: 22 kW
- Pump efficiency: 65%
- Motor efficiency: 90%
- Volume flow rate: 100 m³/h = 0.02778 m³/s
- Total head: 50 m
- Fluid: water at 25°C (ρ = 996.84 kg/m³, Cp = 4.183 kJ/(kg·K))
- Operating mode: part_load

**Reference BAT conditions:** Grundfos CRE IE5
- Pump efficiency: 88% (target)
- Motor efficiency: 97% (target)

### Step 0 — Conversions and Preliminary Calculations

```
ρ = 996.84 kg/m³
Cp = 4.183 kJ/(kg·K) = 0.004183 kJ/(g·K)
g = 9.807 m/s²
Q = 0.02778 m³/s

Mass flow rate:
   ṁ = ρ × Q
   ṁ = 996.84 kg/m³ × 0.02778 m³/s
   ṁ ≈ 27.58 kg/s
```

**Hydraulic power (useful):**
```
P_hyd = ṁ × g × H
P_hyd = 27.58 kg/s × 9.807 m/s² × 50 m
P_hyd ≈ 134,036 W = 134.04 kW
```

**Actual electrical power input:**
```
P_in = P_motor / η_motor
P_in = 22 kW / 0.90
P_in = 24.44 kW
```

**Actual pump efficiency verification:**
```
η_pump_actual = P_hyd / (P_in × η_pump)
65% = 134.04 kW / (24.44 kW × 0.65)
65% ≈ 134.04 kW / 15.891 kW
η_pump_actual ≈ 84%
```

**Step 1 — Exergy Calculations**

#### 1.1 Kinetic Exergy of Flow

At steady-state, kinetic exergy change due to flow variation is negligible (no significant velocity change at the pump inlet/outlet). Hence:

```
Ex_kin = 0
```

#### 1.2 Pressure (Hydraulic) Exergy

The pressure rise across the pump is the useful work product.

```
Ex_hyd = P_hyd / η_pump,useful
Ex_hyd = 134,036 W / 0.65
Ex_hyd ≈ 206,217 W = 206.22 kW
```

#### 1.3 Electrical (Generator) Exergy

The electrical exergy input is equal to the mechanical power input:

```
Ex_in = P_in × η_gen
Since the motor is the generator:
Ex_in = P_motor = 22,000 W
```

#### 1.4 Total Exergy Destruction

```
Ex_destroyed = Ex_in - Ex_hyd
Ex_destroyed = 24,440 W - 134,036 W / 0.65
Ex_destroyed ≈ 24,440 W - 206,217 W × (1 - 0.65)
Ex_destroyed ≈ 24,440 W - 89,351 W
Ex_destroyed = 24,440 W + 89,351 W
Ex_destroyed = 113,791 W = 113.79 kW
```

#### 1.5 Unavoidable Exergy Destruction

The minimum exergy destruction (unavoidable) occurs at the BAT reference point:

```
P_hyd_BAT = ṁ × g × H = 27.58 kg/s × 9.807 m/s² × 50 m
P_hyd_BAT ≈ 134,036 W

Ex_hyd_BAT = P_hyd_BAT / η_pump,BAT
Ex_hyd_BAT = 134,036 W / 0.88
Ex_hyd_BAT ≈ 152,399 W

Ex_in_BAT = P_motor_BAT = 22 kW (reference BAT motor power)
Ex_destroyed,BAT = Ex_in_BAT - Ex_hyd_BAT
Ex_destroyed,BAT = 24.44 kW - 152,399 / 0.88
Ex_destroyed,BAT = 24,440 W - 172,698 W × (1 - 0.88)
Ex_destroyed,BAT ≈ 24,440 W - 17,352 W
Ex_destroyed,BAT ≈ 6,088 W = 6.09 kW
```

#### 1.6 Avoidable Exergy Destruction

```
Ex_avoidable = Ex_destroyed - Ex_destroyed,BAT
Ex_avoidable = 113,791 W - 6,088 W
Ex_avoidable ≈ 107,703 W = 107.7 kW
```

### Step 2 — Performance Assessment

**Actual Pump Efficiency:** 65%
**Reference BAT Efficiency:** 88%

**Achieved Ratio:**
```
η_pump_actual / η_pump_BAT = 0.65 / 0.88 ≈ 0.739
```

The actual pump is operating at approximately 74% of the BAT reference efficiency.

### Step 3 — Improvement Strategy

**Current Unavoidable Exergy Destruction (BAT):**
```
Ex_destroyed,BAT = 6,088 W = 6.09 kW
```

**Current Avoidable Exergy Destruction:**
```
Ex_avoidable = 107,703 W = 107.7 kW
```

**Avoidable/Unavoidable Ratio:**
```
Ex_avoidable / Ex_destroyed,BAT = 107,703 W / 6,088 W
Ex_avoidable / Ex_destroyed,BAT ≈ 17.69 (ratio)
```

Since the ratio is very high (~17:1), the pump is already performing close to the BAT reference level.

**Improvement Priority:**
- **Current assessment:** Pump efficiency of 65% is low, with significant improvement potential.
- **Motor upgrade consideration:** A higher-efficiency motor (e.g., IE4) should be evaluated. At 97% efficiency, the motor could reduce input power by ~2.8 kW, increasing overall pump system efficiency without changing the reference BAT model.
- **Pump alignment and maintenance:** Ensure optimal pump operating point; verify that cavitation or air binding is not a factor (which would increase exergy destruction).
- **Motor control optimization:** If variable-speed drive available, operate at near-BAT efficiency point with VSD.

### Conclusion

**Total Exergy Destruction:** 113.79 kW
**Unavoidable (BAT reference):** 6.09 kW
**Avoidable (current):** 107.7 kW
**Improvement priority:** Motor upgrade or pump/motor optimization.

Switching to the best-available technology motor (IE5) would be the highest-impact single measure; otherwise, focus on optimizing current arrangement for minimal loss reduction.