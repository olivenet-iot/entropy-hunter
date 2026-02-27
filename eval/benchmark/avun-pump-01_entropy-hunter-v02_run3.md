# avun-pump-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 38.6s | Checks: 3/4

## Exergy Analysis: Centrifugal Pump (Water at 25°C)

### Operating Conditions
- **Volume flow rate:** ṁ = 100 m³/h = 0.0278 m³/s
- **Total head:** H = 50 m
- **Motor power input:** P_elec = 22 kW
- **Pump efficiency (actual):** η_pump = 65%
- **Motor efficiency (actual):** η_motor = 90%
- **Fluid:** liquid water at 25°C, ρ = 997.04 kg/m³, Cp = 4.186 kJ/(kg·K)
- **Grundfos CRE IE5 reference:** pump efficiency = 88%, motor efficiency = 97%

### Step 1: Mass Flow Rate and Hydraulic Power

```
ṁ = ρ × Q̇
ṁ = 997.04 kg/m³ × (0.0278 m³/s)
ṁ = 27.635 kg/s

Hydraulic power:
P_hydr = ṁ × g × H
P_hydr = 27.635 kg/s × 9.807 m/s² × 50 m
P_hydr = 13,474 W = 13.47 kW
```

### Step 2: Actual (Measured) Pump Power

```
P_pump_actual = P_elec / η_motor
P_pump_actual = 22,000 W / 0.90
P_pump_actual = 24,444 W
```

### Step 3: Verify the Actual Pump Efficiency

```
η_pump_actual = P_hydr / P_pump_actual
η_pump_actual = 13,474 W / 24,444 W
η_pump_actual = 0.55 or 55%
```

**Note:** The actual pump efficiency (55%) is lower than the stated 65%. However, for consistency with the input data provided:

```
P_pump_actual = P_hydr / η_pump
P_pump_actual = 13,474 W / 0.65
P_pump_actual = 20,730 W
```

Now recalculate motor power and efficiency with this corrected input:

```
P_elec = P_pump_actual / η_motor
P_elec = 20,730 W / 0.90
P_elec = 23,033 W = 23.03 kW (input power from motor)
```

### Step 4: Useful Power and Exergy

**Useful hydraulic power (product):**
```
P_hydr = 13,474 W
```

**Electrical input exergy:**

For liquid water at 25°C:
- Pressure rise: ΔP = ρ × g × H = 9.807 × 50 = 490.35 Pa
- Temperature difference (for Carnot analysis): negligible for incompressible liquid, so we use mechanical exergy

```
Ex_elec = P_elec / η_el
Ex_elec = 23,033 W / 0.90
Ex_elec = 25,592 W = 25.6 kW
```

### Step 5: Thermal (Unavoidable) Exergy

For a pump with mechanical input:

```
Ex_th = T₀ × ṁ × ΔT
Since ΔT ≈ 0 for liquid water at 25°C:
Ex_th = 0
```

**Avoidable vs. Unavoidable:**

#### Avoidable exergy destruction (from inefficiencies)
```
Ex_d,avoidable = P_pump_actual − P_hydr
Ex_d,avoidable = 24,444 W − 13,474 W
Ex_d,avoidable = 10,970 W = 10.97 kW
```

#### Unavoidable exergy destruction (mechanical losses, internal irreversibility)
```
Ex_d,unavoidable = η_pump × P_hydr − P_hydr
Ex_d,unavoidable = 0.65 × 13,474 W − 13,474 W
Ex_d,unavoidable = 8,757.1 W − 13,474 W
Ex_d,unavoidable = 2,194.3 W = 2.19 kW
```

### Step 6: Efficiency Improvement Analysis

**Current efficiency ratio (actual):**
```
η_ratio_actual = η_pump / η_motor
η_ratio_actual = 0.65 / 0.90
η_ratio_actual = 0.722 or 72.2%
```

**Reference efficiency ratio (BAT):**
```
η_ratio_BAT = 88% / 97% = 0.897 or 89.7%
```

**Achievable improvement:**
```
Δη_ratio = η_ratio_BAT − η_ratio_actual
Δη_ratio = 0.897 − 0.722
Δη_ratio = 0.175 or 17.5 percentage points
```

**Achievable energy savings (P_elec):**
```
ΔP_elec = Δη_ratio × P_elec
ΔP_elec = 0.175 × 23,033 W
ΔP_elec = 4,039.8 W = 4.04 kW
```

**Achievable exergy savings:**
```
Ex_savings = Δη_ratio × Ex_elec
Ex_savings = 0.175 × 25,592 W
Ex_savings = 4,465.1 W = 4.47 kW
```

### Summary

**Total exergy destruction:**
```
Ex_d = Ex_d,avoidable + Ex_d,unavoidable
Ex_d = 10,970 W + 2,194 W
Ex_d = 13,164 W = 13.16 kW
```

**Unavoidable (BAT reference):**
```
Ex_d,unav_BAT = η_pump,BAT × P_hydr − P_hydr
Ex_d,unav_BAT = 0.88 × 13,474 W − 13,474 W
Ex_d,unav_BAT = 11,695.92 W − 13,474 W
Ex_d,unav_BAT = 2,140.12 W = 2.14 kW
```

**Avoidable component:**
```
Ex_d,avoidable = Ex_d − Ex_d,unav_BAT
Ex_d,avoidable = 13,164 W − 2,140.12 W
Ex_d,avoidable = 11,023.88 W = 11.02 kW
```

**Improvement priority:**
- **Avoidable:** 11.02 kW (optimizing pump/motor efficiency)
- **Unavoidable:** 2.14 kW (mechanical losses, internal irreversibility)

The focus should be on reducing the avoidable component by upgrading to a more efficient pump and motor combination that meets or exceeds the BAT reference of Grundfos CRE IE5.

**Achievable improvement:** Reduce avoidable exergy destruction by 17.5 percentage points to reach the BAT reference; expected energy savings = 4.04 kW (P_elec), exergy = 4.47 kW.