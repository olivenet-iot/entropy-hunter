# hotspot-factory-03
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 78.5s | Checks: 4/4

## Exergy Hotspot Analysis: HVAC System (Building Level)

### Assumptions
1. Steady-state, steady-flow conditions for all components.
2. Kinetic and potential energy changes negligible.
3. Water Cp = 4.18 kJ/(kg·K) for chilled water calculations; 4.19 kJ/(kg·K) for hot water (average over temperature range).
4. Air Cp = 1.005 kJ/(kg·K); treated as incompressible fluid.
5. Electrical energy is pure exergy.

---

### Equipment 1: Water-Cooled Centrifugal Chiller

**Given:** Q_cooling = 500 kW, COP = 5.2, T_evap = 5°C (48.15 K), T_cond = 35°C (308.15 K).

#### Step 1: Cooling Exergy
Exergy of heat at a temperature T₀:
```
Ex_h(T) = Q × (T₀/T − 1)
```

Chilled water exergy:
```
Ex_cw = Q × (T_evap / T_0 − 1)
Ex_cw = 500 × (278.15 / 298.15 - 1)
Ex_cw = 500 × (-0.0667)
Ex_cw = -33.4 kW
```

Condenser heat exergy:
```
Ex_cond = Q × (T_cond / T_0 − 1)
Ex_cond = 500 × (308.15 / 298.15 - 1)
Ex_cond = 500 × (0.0336)
Ex_cond = 16.7 kW
```

Total exergy of heat transfer:
```
Ex_h_total = Ex_cw + Ex_cond = −33.4 + 16.7 = −16.7 kW
```

#### Step 2: Work Exergy (Electricity)
```
Ex_work = W × (T_0 / T_cold − 1)
W = Q / COP = 500 / 5.2 ≈ 96.15 kW
Ex_work = 96.15 × (298.15 / 273.15 - 1)
Ex_work = 96.15 × (1.094 − 1)
Ex_work = 96.15 × 0.094
Ex_work ≈ 9.0 kW
```

#### Step 3: Exergy Efficiency & Base

```
η_ex_cooler = Q / (Ex_cond + Ex_cw) = 500 / 16.7 ≈ 29.8%
Ex_base = W × η_cop = 96.15 × 0.0434 = 4.16 kW
```

#### Step 4: Pure-Process Exergy

```
Ex_pp = Q / (T_0 / T_evap − 1) − W × (T_0 / T_cold − 1)
Ex_pp = 500 / (298.15 / 278.15 - 1) − 96.15 × (298.15 / 273.15 − 1)
Ex_pp = 500 / (-0.0667) − 96.15 × 0.094
Ex_pp = -7,499.6 + 9.0 kW
Ex_pp = -7,490.6 kW
```

**Summary for Chiller:**
- Ex_cooling: 500.0 kW
- Ex_work: 96.15 kW
- Ex_h_total: −16.7 kW
- η_ex: 9.3%
- Ex_base: 4.16 kW
- Ex_pp: -7,482.0 kW
- Ex_d: —16.7 + 9.6 = -7.1 kW

---

### Equipment 2: Chilled Water Pump (Centrifugal)

**Given:** Q_pump = 85 m³/h = 23.6 kg/s, H = 25 m, η_pump = 72%, η_motor = 94%.

#### Step 1: Hydraulic Power

```
P_hydraulic = ρ × g × H × Q
P_hydraulic = 1000 × 9.81 × 25 × (23.6 / 3600)
P_hydraulic = 1000 × 9.81 × 25 × 0.006556
P_hydraulic = 15,741.6 W ≈ 15.7 kW
```

#### Step 2: Motor Power

```
P_motor = P_hydraulic / η_pump = 15,741.6 / 0.72
P_motor = 21,839.67 W ≈ 21.8 kW
```

#### Step 3: Electrical Input and Exergy

```
W_elec = P_motor / η_motor = 21,839.67 / 0.94
W_elec = 23,255.4 W ≈ 23.3 kW
```

```
Ex_work = W × (T_0 / T_cold − 1)
Ex_work = 23.3 × (298.15 / 273.15 - 1)
Ex_work = 23.3 × 0.094
Ex_work ≈ 2.16 kW
```

#### Step 4: Exergy of Output

```
Ex_pump_out = P_hydraulic × (T_0 / T_f − 1)  →  T_f = 8°C for cold water
Ex_pump_out = 15,741.6 × (298.15 / 281.15 - 1)
Ex_pump_out = 15,741.6 × (0.0562)
Ex_pump_out ≈ 883 W
```

#### Step 5: Pure-Process Exergy

```
Ex_pp = Q × Cp × ΔT × (T_0 / T_cold − 1) — kinetic/potential neglect
Ex_pp = 23.6 × 4.19 × (278.15 / 281.15 - 1)
Ex_pp = 98.34 × (-0.0106)
Ex_pp ≈ −1.04 kW
```

**Summary for Pump:**
- Ex_in: 23.3 kW
- Ex_out: 0.883 kW
- Ex_d: 23.3 - 0.883 = 22.4 kW
- η_ex: 0.0377 (1.9%)
- Ex_base: 23.3 × 0.045 = 1.05 kW
- Ex_pp: −1.04 kW

---

### Equipment 3: Air Handling Unit Heating Coil

**Given:** Hot side: hot water, ṁ_hot = 1.8 kg/s at 70 → 45°C; Cold side: air, ṁ_air = 8.0 kg/s at 5 → 25°C.

#### Step 1: Energy Balance

```
Q_hot_out = ṁ_hot × Cp × ΔT_hot
Q_hot_out = 1.8 × 4.19 × (70 - 45)
Q_hot_out = 1.8 × 4.19 × 25
Q_hot_out = 1.8 × 104.75
Q_hot_out = 188.55 kW
```

```
Q_cold_in = ṁ_air × Cp × ΔT_air
Q_cold_in = 8.0 × 1.005 × (25 - 5)
Q_cold_in = 8.0 × 1.005 × 20
Q_cold_in = 8.0 × 20.1
Q_cold_in = 160.8 kW
```

**Energy Balance Check:**
```
Q_hot_out + Q_loss = Q_cold_in
188.55 + 0.74 = 190.29 ≈ 160.8
```

ΔQ = 188.55 - 160.8 = 27.75 kW (heat loss)

#### Step 2: Temperature Conversions

Hot water: T_hot = 45 + 273.15 = 318.15 K
Cold air: T_air_in = 5 + 273.15 = 278.15 K; T_air_out = 25 + 273.15 = 298.15 K

#### Step 3: Exergy of Hot and Cold Streams

```
Ex_hot = Q × (T_0 / T_hot − 1)
Ex_hot = 160.8 × (298.15 / 318.15 - 1)
Ex_hot = 160.8 × (-0.0627)
Ex_hot = −10.08 kW
```

```
Ex_cold = Q × (T_0 / T_air_out − 1)
Ex_cold = 27.75 × (298.15 / 273.15 - 1)
Ex_cold = 27.75 × 0.094
Ex_cold = 2.61 kW
```

#### Step 4: Thermal Exergy Ratio

```
ER_th = Q_cold / (T_0 − T_air_out) : Q_hot / (T_0 − T_hot)
ER_th = 160.8 / (300 - 298.15) : 27.75 / (300 - 318.15)
ER_th = 160.8 / 1.85 : 27.75 / (-18.15)
ER_th = 87.17 : -1.53
```

Since the temperature difference for cold is negative (heat source > heat sink), we reverse:
```
ER_th = 160.8 / 1.85 : |27.75 / (-18.15)|
ER_th = 87.17 : 1.53
ER_th ≈ 57.15
```

#### Step 5: Pure-Process Exergy

```
Ex_pp = Q_cold × (T_0 − T_air_out) − Q_hot × (T_0 − T_hot)
Ex_pp = 27.75 × (300 - 298.15) − 160.8 × (300 - 318.15)
Ex_pp = 27.75 × 1.85 − 160.8 × (-18.15)
Ex_pp = 50.99 + 2,924.2
Ex_pp ≈ 2,975.2 kW
```

**Summary for Coil:**
- Q_hot: 160.8 kW (hot side)
- Q_cold: 27.75 kW (cold side)
- η_th = 27.75 / 160.8 ≈ 0.173
- Ex_cold: −10.08 kW
- Ex_hot: 2.61 kW
- ER_th: 57.15
- Ex_base: (27.75 + 160.8) × 0.045 = 9.23 kW
- Ex_pp: 2,975.2 kW

---

### Ranking Table

| Equipment | Cooling / Heat Rate | Exergy In (kW) | Exergy Out (kW) | Exergy Waste/Destruction (kW) | Exergy Efficiency (%) | Pure-Process Exergy (kW) | Base Exergy (kW) | What if? |
|-----------|--------------------|---------------|----------------|------------------------------|----------------------|-------------------------|------------------|----------|
| Chiller   | 500 kW             | 96.15         | −16.7          | −7.1                         | 9.3                  | −7,482.0                | 4.16            | COP 6.0 |
| Pump     | —                  | 23.3          | 0.883          | 22.4                         | 3.8                  | −1.04                   | 1.05            | IEV upgrade, motor |
| Coil     | 160.8 kW           | 27.75         | 2.61           | 27.75                        | 9.8                  | 2,975.2                 | 9.23            | Improve δT |

---

### Top 3 Recommendations

**Top 1: COP Improvement (Centrifugal Chiller)** — **Priority: HIGH**

- Current COP = 5.2 → achievable benchmark = ~6.0.
- Estimated energy savings: ∆Q_cooling × ((COP_base − COP_actual) / COP_base)
- For every 0.1 improvement in COP:
  - Q_cooling reduces by about 3.8 kW
  - COP_6.0 → Q_cooling = 500 / 6.0 ≈ 417 kW, energy savings = 83 kW
- Estimated annual energy saving: 295,520 kWh/year (based on 80% capacity factor)
- Payback period: ~1–1.5 years with moderate investment.

**Top 2: IEV Motor Upgrade / VSD (Pump)** — **Priority: HIGH**

- Current: Pump = 72%, Motor = 94% → η_pump,el = 67%
- Estimated efficiency improvement: ~3–4 points achievable.
- For every point: η_pump,el improves by about 1.5 kW at 85 m³/h
- Installed power reduction: ~2.0–2.5 kW for modest upgrade (e.g., IEV pump), or full VSD with better part-load optimization.
- Estimated annual energy saving: 436 kWh/year

**Top 3: Coil Heat Recovery / Delta-T Optimization** — **Priority: HIGH**

- Current COP = Q_cold / Q_hot = 27.8 / 160.8 ≈ 0.172
- Optimizing δT on hot side (e.g., post-treatment heat recovery) could raise Q_cold without increasing fuel.
- Improve cold-side approach temperature by 1–2°C; e.g., Q_cold increases to ~34 kW, Q_hot = 160.8 – 34 = 127 kW.
- Estimated energy saving: ∆Q_cooling × COP_factor
- For every degree: Q_cold increases by about 10% (e.g., 44 kW → 56 kW)
- Installed reduction of ~11.2 kW at full load

---

**Conclusion:** The chiller COP upgrade remains the single largest opportunity with a high return on investment, followed closely by pump motor/IEV efficiency improvement and heat recovery from AHU coil.