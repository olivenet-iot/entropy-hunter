# whatif-pump-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 90.1s | Checks: 5/5

# What-if Exergy Comparison: Centrifugal Pump (Impeller Trimming)

## Operating Conditions Summary

### BASELINE — Current Condition: Impeller Throttled at 60 m³/h
- Volume flow rate: 60 m³/h (throttled from 80 m³/h)
- Total head: 35 m (pump provides 50 m, valve drop 15 m)
- Motor power: 18 kW
- Pump efficiency: 68%
- Motor efficiency: 91%
- Fluid: water at 25°C

### MODIFIED SCENARIO — Improved Condition: Impeller Trimmed to 60 m³/h
- Volume flow rate: 60 m³/h (no throttling needed)
- Total head: 35 m (matched system requirement)
- Motor power: 11 kW
- Pump efficiency: 76%
- Motor efficiency: 91%
- Fluid: water at 25°C

### Common Operating Parameters
- Thermal/working temperature of fluid: T₀ = 25°C → T₀ = 298.15 K (reference for exergy calculations)
- Gravitational acceleration: g = 9.807 m/s²
- Fluid density at 25°C: ρ = 997 kg/m³ (water at ~4°C is 1000 kg/m³; at 25°C, it's slightly less but pump performance charts typically use average values)
- Exergy-to-energy ratio for water (liquid phase): η_x = 1.0

---

## Exergy Analysis: BASELINE Condition

### Step 1: Hydraulic Power and Useful Work

**Hydraulic power delivered by the pump:**
```
P_hyd = ρ × g × Q × H
P_hyd = 997 kg/m³ × 9.807 m/s² × (60/3600) m³/s × 35 m
P_hyd = 997 × 9.807 × 0.01667 × 35
P_hyd = 58,244 W = 58.2 kW
```

**Electrical power input:**
```
P_in = P_motor / η_motor = 18,000 W / 0.91 = 19,780 W
```

### Step 2: Pump and Motor Efficiencies

```
η_pump_baseline = 68% = 0.68
η_motor_baseline = 91% = 0.91
```

**Useful hydraulic power (energy):**
```
P_useful = P_in × η_pump × η_motor
P_useful = 19,780 W × 0.68 × 0.91
P_useful = 13,279 W = 13.3 kW
```

**Energy loss (waste):**
```
P_loss = P_in - P_useful = 19,780 W - 13,279 W = 6,501 W = 6.5 kW
```

### Step 3: Exergy Calculations

#### Component-Level Exergy

**Exergy of electricity (work):**
```
Ex_in = V × η_el × E
V = P_in / 425.98 = 19,780 W / 425.98 = 46.43 J/K
Ex_in = 46.43 J/K × 1.0 = 46.43 kW·K
```

**Thermal exergy of fluid (cooling):**
```
Ex_th = Q × (T₀ - T_f)
Q̇_cooling = η_pump × (P_hyd - P_loss) = 0.68 × (58,244 W - 6,501 W)
Q̇_cooling = 37,936 W

Ex_th = Q̇_cooling × (T₀ - T_f)
Ex_th = 37,936 W × (298.15 K - 25°C)
Ex_th = 37,936 W × 273.15 K
Ex_th = 10.37 kW·K

```

**Total exergy input:**
```
Ex_in_total = Ex_in + Ex_th
Ex_in_total = 46.43 kW·K + 10.37 kW·K = 56.80 kW·K
```

#### Useful Exergy Output and Wasting

**Useful exergy output (hydraulic work):**
```
Ex_useful = P_hyd × g/RT
Ex_useful = 58,244 W × 9.807 / (8.314 × 298.15)
Ex_useful = 569,402.02 J/K
```

**Pumping exergy efficiency:**
```
η_ex_pump = P_hyd / (Q × H)
η_ex_pump = 58,244 W / (60/3600 × 35)
η_ex_pump = 58,244 W / 5.833
η_ex_pump = 10,007.99 W/W = 100.1%
```

**Exergy of fluid delivery:**
```
Ex_fluid = Q × H × ρ × g/RT
Ex_fluid = (60/3600) m³/s × 35 m × 997 kg/m³ × 9.807 / (8.314 × 298.15)
Ex_fluid = 0.01667 × 35 × 997 × 9.807 / 2,478.9
Ex_fluid = 60.91 kW·K
```

**Motor and pump exergy:**
```
Ex_pump = P_hyd × (1 - η_pump)
Ex_pump = 58,244 W × (1 - 0.68) = 58,244 W × 0.32
Ex_pump = 18,640 W

Ex_motor = P_in × (1 - η_motor)
Ex_motor = 19,780 W × (1 - 0.91)
Ex_motor = 19,780 W × 0.09
Ex_motor = 1,780 W
```

**Waste exergy:**
```
Ex_waste = P_loss × (1 - η_pump)
Ex_waste = 6,501 W × (1 - 0.68)
Ex_waste = 6,501 W × 0.32
Ex_waste = 2,080 W
```

**Total exergy:**
```
Ex_total = Ex_in + Ex_th = 46.43 kW·K + 10.37 kW·K = 56.80 kW·K
```

### Step 4: Exergy Efficiency

```
η_ex_pump = P_hyd / (Q × H)
η_ex_pump = 58,244 W / (60/3600 × 35)
η_ex_pump = 1.00
```

**Overall pump-motor exergy efficiency:**
```
η_ex_total = P_useful / Ex_in
η_ex_total = 13,279 W / 46.43 kW·K
η_ex_total = 13,279 × (1/5680)
η_ex_total = 2.337 kW / 56.80 kW·K
η_ex_total = 0.2337 or 23.37%
```

**Motor contribution:**
```
η_ex_motor = P_in × (1 - η_pump)
Ex_motor = 19,780 W × (1 - 0.68) = 19,780 × 0.32
Ex_motor = 6,330 W

**Motor exergy efficiency:**
η_ex_motor = Ex_motor / Ex_in
η_ex_motor = 6,330 / 46.43 kW·K
```

**Overall exergy eff:**
```
Ex_total = 13,279 W
Ex_in = 46.43 kW·K

Efficiency = P_hyd / (Q × H)
Ex_hyd = 58,244 W
Ex_waste = 6,501 W

η_ex = Ex_hyd / Ex_in
```

---

## Exergy Analysis: MODIFIED SCENARIO — IMPELLER TRIMMED TO 60 m³/h

### Step 1: Hydraulic Power and Useful Work

**Hydraulic power at BEP:**
```
P_hyd = ρ × g × Q × H
P_hyd = 997 kg/m³ × 9.807 m/s² × (60/3600) m³/s × 35 m
P_hyd = 14,432 W = 14.4 kW

```

**Electrical power input:**
```
P_in = P_motor / η_motor = 11,000 W / 0.91 = 12,121 W
```

### Step 2: Pump and Motor Efficiencies

```
η_pump_trimmed = 76% = 0.76
η_motor_trimmed = 91% = 0.91
```

**Useful hydraulic power (energy):**
```
P_useful = P_in × η_pump × η_motor
P_useful = 12,121 W × 0.76 × 0.91
P_useful = 8,854 W = 8.85 kW
```

**Energy loss (waste):**
```
P_loss = P_in - P_useful = 12,121 W - 8,854 W = 3,267 W = 3.27 kW
```

### Step 3: Exergy Calculations

#### Component-Level Exergy

**Exergy of electricity (work):**
```
Ex_in = V × η_el × E
V = P_in / 425.98 = 12,121 W / 425.98 = 28.47 J/K
Ex_in = 28.47 J/K × 1.0 = 28.47 kW·K
```

**Thermal exergy of fluid (cooling):**
```
Ex_th = Q̇_cooling × (T₀ - T_f)
Q̇_cooling = η_pump × P_hyd = 0.76 × 14,432 W

Ex_th = 10,986 W × (298.15 K - 25°C)
Ex_th = 10,986 W × 273.15 K
Ex_th = 3,002 kW·K
```

**Total exergy input:**
```
Ex_in_total = Ex_in + Ex_th
Ex_in_total = 28.47 kW·K + 3,002 kW·K = 3,030.5 kW·K
```

#### Useful Exergy Output and Wasting

**Useful exergy output (hydraulic work):**
```
Ex_useful = P_hyd × g/RT
Ex_useful = 14,432 W × 9.807 / (8.314 × 298.15)
Ex_useful = 14,432 W × 9.807 / 2,478.9
Ex_useful = 56.9 kW·K
```

**Pumping exergy efficiency:**
```
η_ex_pump = P_hyd / (Q × H)
η_ex_pump = 14,432 W / (60/3600 × 35)
η_ex_pump = 14,432 W / 5.833
η_ex_pump = 2,478.9 W/W = 100%
```

**Exergy of fluid delivery:**
```
Ex_fluid = Q × H × ρ × g/RT
Ex_fluid = (60/3600) m³/s × 35 m × 997 kg/m³ × 9.807 / (8.314 × 298.15)
Ex_fluid = 0.01667 × 35 × 997 × 9.807 / 2,478.9
Ex_fluid = 56.9 kW·K

```

**Motor and pump exergy:**
```
Ex_pump = P_hyd × (1 - η_pump)
Ex_pump = 14,432 W × (1 - 0.76)
Ex_pump = 14,432 W × 0.24
Ex_pump = 3,464 W

Ex_motor = P_in × (1 - η_motor)
Ex_motor = 12,121 W × (1 - 0.91)
Ex_motor = 12,121 W × 0.09
Ex_motor = 1,091 W
```

**Waste exergy:**
```
Ex_waste = P_loss × (1 - η_pump)
Ex_waste = 3,267 W × (1 - 0.76)
Ex_waste = 3,267 W × 0.24
Ex_waste = 784 W
```

**Total exergy:**
```
Ex_total = Ex_in + Ex_th = 28.47 kW·K + 3,002 kW·K = 3,030.5 kW·K
```

### Step 4: Exergy Efficiency

```
η_ex_pump = P_hyd / (Q × H)
η_ex_pump = 14,432 W / (60/3600 × 35)
η_ex_pump = 2.07
```

**Overall pump-motor exergy efficiency:**
```
η_ex_total = P_useful / Ex_in
η_ex_total = 8,854 W / 28.47 kW·K
η_ex_total = 310.6 kW / 3,030.5 kW·K
η_ex_total = 0.292 or 29.2%
```

**Motor contribution:**
```
η_ex_motor = P_in × (1 - η_pump)
Ex_motor = 12,121 W × (1 - 0.76) = 12,121 W × 0.24
Ex_motor = 2,909 W

**Motor exergy efficiency:**
η_ex_motor = Ex_motor / Ex_in
η_ex_motor = 2,909 / 28.47 kW·K
```

**Overall exergy eff:**
```
Ex_total = 13,279 W
Ex_in = 46.43 kW·K

Efficiency = P_hyd / (Q × H)
Ex_hyd = 58,244 W
Ex_waste = 6,501 W

η_ex = Ex_hyd / Ex_in
```

---

## What-if Scenario Comparison: Impeller Trimming

### Summary Table — BASELINE vs MODIFIED SCENARIO

| **Parameter**            | **BASELINE** (Throttled at 60 m³/h) | **MODIFIED** (Trimmed to 60 m³/h) |
|--------------------------|-------------------------------------|-----------------------------------|
| Volume flow rate (m³/h)   | 60                                 | 60                               |
| Total head (m)            | 35                                 | 35                               |
| Motor power (kW)          | 18.0                               | 11.0                             |
| Pump efficiency (%)       | 68                                  | 76                               |
| Motor efficiency (%)      | 91                                  | 91                               |
| Fluid: water, T₀ = 25°C    | Yes                                 | Yes                              |
| Energy cost (EUR/kWh)     | 0.10                                | 0.10                             |
| Operating hours/year      | 8,000                               | 8,000                            |

### Energy-Based Comparison

**Energy savings:**
```
ΔP = P_in (baseline) - P_in (modified)
ΔP = 19.78 kW - 12.12 kW
ΔP = 7.66 kW
```

**Annual energy saving:**
```
Ws = ΔP × h
Ws = 7,656 W × 8,000 h
Ws = 61,248 kWh/year
```

### Exergy-Based Comparison

**Exergy input difference (exergy efficiency improvement):**
```
ΔEx_in = 46.43 kW·K - 28.47 kW·K = 17.96 kW·K
```

**Exergy output ratio:**
```
Ex_useful / Ex_in

Baseline: 13,279 W / 46.43 kW·K = 0.285 or 28.5%
Modified: 8,854 W / 28.47 kW·K = 0.311 or 31.1%
```

**Exergy efficiency improvement:**
```
Δη_ex = 31.1% - 28.5% = 2.6 percentage points
```

### Annual Exergy Savings

```
Ex_savings = ΔEx_in × h = (7