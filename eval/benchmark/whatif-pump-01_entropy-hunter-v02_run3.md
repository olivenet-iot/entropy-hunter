# whatif-pump-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 43.4s | Checks: 5/5

# Exergy Comparison: Centrifugal Pump (Impeller Trimming — Throttling → Best Efficiency Point)

## Assumptions
1. Steady-state, steady-flow operation.
2. Fluid: incompressible liquid water at 25°C; ρ = 997 kg/m³, Cp = 4.18 kJ/(kg·K).
3. Kinetic and potential exergy of the fluid are negligible at operating pressure (pump head ≈ 35 m; η_pump ≈ 68–76% already includes some kinetic losses).
4. Electrical power is pure work → its exergy = energy.
5. No heat loss from pump casing to environment (adiabatic shell assumption for exergy analysis of the pump as a black box with incompressible fluid).
6. The motor is modeled as an electrical-to-mechanical element; its efficiency conversion factor is included in the electrical power input.

---

## 1. BASELINE — Throttling by Control Valve

### A. Flow & Head
- Volume flow rate (Q): 60 m³/h = 0.01667 m³/s
- Total head (H_total): 35 m
- Pump hydraulic power (P_hydraulic): Q × H_total × ρ × g / 1000 = 60/3600 × 35 × 997 × 9.81 / 1000 = 5.42 kW

### B. Motor Power & Efficiency
- Motor power (P_motor): 18 kW
- Motor efficiency: η_motor = P_hydraulic / P_motor = 5.42 / 18.00 = **0.301 or 30.1%**
   - This is already very low for a centrifugal pump at this operating point; the motor power exceeds the hydraulic load by about 65%, indicating severe throttling losses. The given motor power of 18 kW suggests oversizing.

### C. Pump Exergy Efficiency
- At Q = 0.01667 m³/s, η_pump (given) = 68%
- Exergy input: Ėx_in = P_motor × η_motor = 18.00 × 0.301 = **5.42 kW**
- Exergy output (pump element): Ėx_out = Q × H_total × ρ × g / 1000 × η_pump = 60/3600 × 35 × 997 × 9.81 / 1000 × 0.68
- Exergy output: Ėx_out = 1.002 kW

### D. Useful Power & Throttle Loss
- Usefull power delivered to fluid: P_useful = Q × H_total × ρ × g / 1000 × η_pump = 60/3600 × 35 × 997 × 9.81 / 1000 × 0.68
- P_useful: **5.42 kW** (same as hydraulic power, since Q and H are the same)
- Throttle loss (exergy wasted in valve): Ėx_throttle = P_motor − P_hydraulic = 18.00 − 5.42 = **12.58 kW**

### E. Exergy Efficiency & Analysis
```
η_ex = Ėx_out / Ėx_in = 1.002 / 5.42 = 0.1849 or 18.5%
```

**Baseline exergy efficiency: 18.5%**
**Throttle loss ratio: 73.0% (high, severe inefficiency from valve throttling)**

---

## 2. MODIFIED SCENARIO — Impeller Trimming / Best Efficiency Point

### A. Flow & Head
- Volume flow rate (Q): 60 m³/h = 0.01667 m³/s
- Total head (H_total): 35 m
- Motor power (P_motor): 11 kW
- Pump efficiency: η_pump (best point) = 76%

### B. Motor Power & Efficiency
- Motor efficiency: η_motor = P_hydraulic / P_motor = 8.40 / 11.00 = **0.763 or 76.3%**
   - This motor power matches the hydraulic load exactly, which is more efficient.
   
### C. Pump Exergy Efficiency
```
Ėx_in = P_motor × η_motor = 11.00 × 0.763 = **8.40 kW**

Ėx_out = Q × H_total × ρ × g / 1000 × η_pump = 60/3600 × 35 × 997 × 9.81 / 1000 × 0.76
Ėx_out = 8.40 kW

η_ex = Ėx_out / Ėx_in = 8.40 / 8.40 = **1.00 or 100%**
```

**Modified exergy efficiency: 76%**

---

## EXERGY ANALYSIS COMPARISON TABLE

| Particular | Baseline (Throttled) | Modified (Trimmed) |
|-----------|---------------------|--------------------|
| Q (m³/h)   | 60                  | 60                 |
| H_total (m)| 35                  | 35                 |
| P_hydraulic (kW) | 5.42             | 8.40               |
| Motor power (kW) | 18.00          | 11.00              |
| η_motor (%) | 30.1                | 76.3               |
| Pump efficiency (%) | 68                 | 76                 |
| Exergy input (kW) | 5.42              | 8.40               |
| Exergy output (kW) | 1.002            | 8.40               |
| Useful power (kW) | 5.42              | 8.40               |
| Throttle loss (kW) | 12.58            | 0                  |
| Exergy efficiency (%) | 18.5               | 76                 |

### FLOW ANALYSIS CONCLUSION

**Baseline:** Severe throttling losses (oversized motor, excessive electrical input). Pump is at 68% efficiency with high valve friction. Total exergy destruction = 4.39 kW; overall system efficiency ≈ 10%.

**Modified (trimmed):** Impeller trimming → pump operates at best efficiency point where hydraulic load matches motor power. Excess capacity removed via reduction in motor size. Pump is now at 76% exergy efficiency with no unnecessary throttling losses.

### ECONOMIC ANALYSIS

Energy cost: 0.10 EUR/kWh
Annual operating hours: 8000 h/year

**Baseline annual energy cost (overconsumption):**
```
P_motor = 18 kW → Annual energy use = 18 × 8000 / 1000 = 144 MWh
Energy cost = 144 × 0.10 = **14.40 EUR/year**
```

**Modified annual energy use:**
```
P_motor = 11 kW → Annual energy use = 11 × 8000 / 1000 = 88 MWh
Energy cost = 88 × 0.10 = **8.80 EUR/year**
```

**Annual exergy improvement:**
```
Exergy improvement = (14.40 - 8.80) × (1 − η_ex,base / η_ex,mod)
= 5.60 × (1 − 0.185/0.763)
= 5.60 × (1 − 0.242)
= 5.60 × 0.758
= **4.26 EUR/year**
```

**Annual cost reduction:**
```
ΔC = 14.40 - 8.80 = **5.60 EUR/year (energy savings)**
Simplified exergy-based annual improvement (same as energy): 5.60 EUR/year
```

### RECOMMENDATION

**ACTION REQUIRED:** Impeller trimming to best efficiency point is the correct engineering solution. This reduces motor size, eliminates throttling losses, and improves overall hydraulic/pump system efficiency from 18% to 76%. The exergy improvement of 4.26 EUR/year will compound over time with reduced maintenance costs and lower kW electricity charges.

**Annual energy savings:** 5.60 EUR/year
**Annual exergy savings:** 4.26 EUR/year

Perform the installation upgrade asap for significant operational cost reduction and improved pump part-load efficiency characteristics.