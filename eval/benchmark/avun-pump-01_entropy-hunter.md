# avun-pump-01
Model: entropy-hunter
Time: 217.0s
Checks: 3/5

## Avoidable/Unavoidable Exergy Destruction Analysis: Centrifugal Pump

**Operating conditions:**
- Volume flow rate: 100 m³/h (Q = 2.78 m³/min)
- Total head: 50 m (H = 50 m)
- Motor power input: 22 kW
- Pump efficiency: ηpump = 65%
- Motor efficiency: ηmotor = 90%
- Fluid: water at 25°C
- Gravitational acceleration: g = 9.81 m/s²

**Reference (BAT):**
- Pump: Grundfos CRE IE5, ηpump,BAT = 88%, ηmotor,BAT = 97%

---

### Step 1: Basic Energy Calculations

#### Shaft Power
The shaft power delivered to the fluid is:
```
P_shaft = Q × H × ρ × g / 3600
```

Water density at 25°C, ρ = 997 kg/m³. Converting volume flow rate:

```
Q = 100 m³/h = 100/3600 = 0.0278 m³/s
```

Shaft power:
```
P_shaft = 0.0278 × 50 × 997 × 9.81 / 3600
P_shaft = 139.06 kW
```

However, the actual motor power input is given as P_motor = 22 kW. The ratio of actual to rated shaft power gives us an idea of operating efficiency:
```
η_actual = (Q × H) / (3600 × η_pump × η_motor)
η_actual = (100 × 50) / (3600 × 0.65 × 0.90)
η_actual = 5000 / 1854
η_actual = 2.704 W/W → η_actual = 0.270 kW/kW = 27%
```

The motor consumes 22 kW but only delivers a shaft power of:
```
P_shaft = P_motor × η_motor = 22 × 0.90 = 19.8 kW
```

Cross-checking:
```
P_actual_check = Q × H × ρ × g / 3600 = 5000 / 3600 = 13.89 W = 0.01389 kW
Actual pump efficiency (from input data): ηpump,actual = P_shaft_actual / (Q × H) = 0.0198 / 0.01389 = 1.423 → 65%
```

This is consistent with the given parameters — the pump delivers only ~0.019 kW to fluid, but consumes 22 kW. The remaining power (22 - 1.98 = 20.02 kW) goes into internal irreversibilities (friction in motor/pipe), which is typical for a severely off-BEP centrifugal pump.

For the analysis I will use the **measured input/output data**:
- Actual electrical consumption: P_motor = 22 kW
- Actual fluid power delivered: P_shaft = Q × H × ρ × g / 3600 (already calculated as 0.0198 kW, or 19.8 W)

### Step 2: Exergy Balance

#### Exergy of Electricity (Fuel Input)
The exergy content per unit energy for electricity:
```
ex_fuel = 1.04 × P_elec = 1.04 × 22 = 22.88 kW
```

#### Exergy of Fluid (Product) — Minimum-Exergy Product

For incompressible liquid at negligible pressure rise:
```
ex_product = ρ × g × H
ex_product = 997 × 9.81 × 50 / 3600
ex_product = 49,221.46 / 3600
ex_product = 13.67 kW
```

#### Exergy Destruction

The total exergy destruction is the difference between fuel input and product output:
```
ex_destr_total = P_fuel - ex_product
ex_destr_total = 22.88 - 0.0198
ex_destr_total = 22.86 kW
```

#### Split into Avoidable and Unavoidable Portion

**Unavoidable Exergy Destruction (BAT Reference)**: This is the exergy destroyed when operating at BAT reference conditions:
```
P_shaft_BAT = Q × H × ρ × g / 3600 = 19.8 W
P_elec_BAT = P_shaft_BAT / η_motor,BAT = 19.8 / 0.97 = 20.4 kW

ex_destr_BAT = P_fuel_BAT - ex_product
ex_destr_BAT = 20.4 - 13.67
ex_destr_BAT = 6.73 kW
```

**Avoidable Exergy Destruction**: The portion of total destruction that can be improved by tuning the pump or motor:
```
ex_avoidable = ex_destr_total - ex_destr_BAT
ex_avoidable = 22.86 - 6.73
ex_avoidable = 16.13 kW
```

### Step 3: What-If Scenario — Pump Upgrade

Let's consider replacing the pump with a Grundfos CRE IE5:

At BAT efficiency:
- P_shaft,BAT = Q × H × ρ × g / 3600 = 19.8 W
- η_pump,BAT = 0.88, η_motor,BAT = 0.97

The shaft power is still only 19.8 kW; however, the total electrical consumption will now be:
```
P_motor,BAT = P_shaft,BAT / (η_motor,BAT × η_pump,BAT)
P_motor,BAT = 0.0198 / (0.97 × 0.88) = 0.0251 kW/kW
P_motor,BAT = 0.0198 / 0.8436 = 0.0234 kW × 22 kW = 5.19 kW
```

Fuel input:
```
P_fuel,BAT = 23.1 W
ex_product = 13.67 W (same as above, since H and fluid properties are unchanged)
```

Exergy destroyed at BAT with improved pump:
```
ex_destr_BAT_upg = P_fuel,BAT - ex_product
ex_destr_BAT_upg = 23.1 - 13.67
ex_destr_BAT_upg = 9.43 kW
```

### Summary

**Baseline (Current):**
- Exergy destruction: 22.86 kW
- Avoidable exergy reduction: 16.13 kW

**BAT Improvement Target:**
- Exergy destruction: 9.43 kW

The current system has significant avoidable inefficiencies, primarily due to the pump operating far off-BEP with excessive motor losses. A pump upgrade to a high-efficiency centrifugal (Grundfos CRE) is essential; it would reduce exergy destruction by **16.13 kW** — over 70% of the current waste.

**Improvement Priority:**
- Upgrade pump: Replace existing pump with Grundfos CRE IE5
- Ensure motor is oversized or operates in part-load range, and consider motor upgrade or VFD for optimized speed control