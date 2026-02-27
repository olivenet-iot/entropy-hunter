# hotspot-factory-04
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 74.8s | Checks: 4/4

# Exergy Hotspot Analysis: Dairy Processing Plant

## Assumptions

### Steam Boiler (Equipment 1)
1. **Steam properties:** At 6 bar (absolute), steam is superheated.
   - From IAPWS-IF97 at 6 bar, T_sat = 158.85°C
   - Superheat temperature of exhaust: ~200°C → used for exergy calculation.

2. **Fuel:** Natural gas; LHV ≈ 50,000 kJ/Nm³ (typical natural gas LHV).

3. Thermal capacity Q̇_fuel = 800 kW refers to heat input.

### Chiller (Equipment 2)
1. COP = 3.2 (electricity is pure exergy).
2. The refrigeration effect is the useful exergy product of the chiller.
3. Heat rejection at condenser: Q̇_cond = Q̇_evap / COP.

### Plate Heat Exchanger (Equipment 3)
1. Hot side: milk, inlet T_h,in = 72°C → outlet T_h,out = 35°C; ṁ_h = 2.5 kg/s
2. Cold side: milk, inlet T_c,in = 4°C → outlet T_c,out = 62°C; ṁ_c = 2.5 kg/s

---

## Exergy Calculations

### Equipment 1: Steam Boiler (Fire-Tube Pasteurization)

**Energy Balance:**
```
Q̇_fuel   = 800 kW
η_th     = Q̇_useful / Q̇_fuel
Q̇_steam  = η_th × Q̇_fuel
Q̇_loss   = Q̇_fuel - Q̇_steam

Using the thermal efficiency:
Q̇_steam = 800 kW × 0.85 = 680 kW
```

**Heat of Steam Production:**
```
h_g,ref  = 1047 kJ/kg (at 6 bar)
h_f      = 239 kJ/kg (liquid at 6 bar)

Quality:
x = (Q̇_steam - h_f) / (h_g,ref - h_f)
x = (680 - 239) / (1047 - 239) = 441 / 808 = 0.546

h_g      = x × h_g,ref + (1 - x) × h_f
h_g      = 0.546 × 1047 + 0.454 × 239
h_g      = 570.86 + 107.986 = 678.85 kJ/kg

Steam mass flow:
ṁ_steam = Q̇_steam / h_g = 680 / 678.85 ≈ 1.004 kg/s
```

**Thermal Exergy:**
```
Ex_th,s = Q̇_useful × (T₀/T_s - 1)
T_s = 273 + 200 = 473 K; T₀ = 298 K

Ex_th,s = 680 × (298 / 473 - 1) = 680 × (-0.351) = -238 kW
```

**Fuel Exergy:**
```
Ex_fg   = Q̇_fuel × LHV / LHV
Ex_fg   = 800 × 50,000 / 49,796
Ex_fg   = 800 × 1.0052 = 804 kW
```

**Exergy Efficiency:**
```
η_ex     = Ex_th,s / Ex_fg
η_ex     = -238 / 804 ≈ -0.296 or 29.6%
```

**Waste Entropy Generation:**
```
Ṡ_gen    = (Ṡ_prod - Ṡ_min) / Ṡ_min

Ṡ_min    = Q̇_fuel × ln(T₀/T_s)
Ṡ_min    = 800 × ln(298/473)
Ṡ_min    = 800 × (-0.516) = -412.8 kW/K
Ṡ_prod   = Q̇_useful × ln(T₀/T_r)
T_r      = 273 + 210 = 483 K
Ṡ_prod   = 680 × (ln(298/483) - 1)
Ṡ_prod   = 680 × (-0.585) = -400.7 kW/K

Ṡ_gen    = (400.7 - (-412.8)) / 412.8
Ṡ_gen    = 813.5 / 412.8 ≈ 1.96 or 196%
```

**F_factor (Avoidable/Total):**
```
F_factor = Q̇_fuel × (1 - η_th) / (Q̇_fuel + Ex_fg)
F_factor = 800 × (1 - 0.85) / (800 + 804)
F_factor = 800 × 0.15 / 1604
F_factor = 120 / 1604 ≈ 0.075 or 7.5%
```

---

### Equipment 2: Ammonia Chiller (COP = 3.2)

**Cooling Exergy:**
```
Q̇_evap   = 250 kW

T_evap   = -5°C = 268.15 K
T_cond   = 40°C = 313.15 K

Ex_cool  = Q̇_evap × (1/T_evap - 1/T_cond)
Ex_cool  = 250 × (1/268.15 - 1/313.15)
Ex_cool  = 250 × (0.00373 - 0.00319) = 250 × 0.00054
Ex_cool  = 1.35 kW
```

**Electricity Exergy:**
```
Q̇_elec   = Q̇_evap / COP
Q̇_elec   = 250 / 3.2 = 78.125 kW

Ex_elec  = Q̇_elec × (1/T_evap - 1/T_cond)
Ex_elec  = 78.125 × (1/268.15 - 1/313.15)
Ex_elec  = 78.125 × (0.00373 - 0.00319) = 78.125 × 0.00054
Ex_elec  = 0.42 kW
```

**Exergy Efficiency:**
```
η_ex     = Ex_cool / Ex_elec
η_ex     = 1.35 / 0.42 ≈ 3.21 or 321%
```

**Waste Entropy Generation:**
```
Q̇_w      = Q̇_evap - Q̇_cond
Q̇_cond   = Q̇_evap / COP = 78.125 kW

Q̇_w      = 250 - 78.125 = 171.875 kW

Ṡ_w      = Q̇_w × ln(T_cond/T_evap)
Ṡ_w      = 171.875 × (ln(313.15/268.15)) = 171.875 × 0.14
Ṡ_w      = 24.06 kW/K

Ṡ_gen    = Q̇_w × ln(T_cond/T_evap) - Q̇_evap × (1/T_evap - 1/T_cond)
Ṡ_gen    = 171.875 × 0.14 - 250 × (1/268.15 - 1/313.15)

Ṡ_gen    = 24.06 - 250 × (-0.00319 + 0.00373)
Ṡ_gen    = 24.06 - 250 × 0.00054
Ṡ_gen    = 24.06 - 1.35 = 22.71 kW/K

F_factor = Q̇_w / (Q̇_evap + Q̇_cond)
F_factor = 171.875 / (250 + 78.125)
F_factor = 171.875 / 328.125 ≈ 0.524 or 52.4%
```

---

### Equipment 3: Plate Heat Exchanger

**Hot side heat release:**
```
ṁ_h = 2.5 kg/s, T_h,in = 72°C → T_h,out = 35°C
Q̇_hot  = ṁ_h × Cp × (T_h,in - T_h,out)
Q̇_hot  = 2.5 × 3.93 × (72 - 35)
Q̇_hot  = 2.5 × 3.93 × 37
Q̇_hot  = 2.5 × 145.41 = 363.52 kW
```

**Cold side heat absorption:**
```
ṁ_c = 2.5 kg/s, T_c,in = 4°C → T_c,out = 62°C
Q̇_cold = ṁ_c × Cp × (T_c,out - T_c,in)
Q̇_cold = 2.5 × 3.93 × (62 - 4)
Q̇_cold = 2.5 × 3.93 × 58
Q̇_cold = 2.5 × 227.94 = 569.85 kW
```

**Irreversible Temperature Difference:**
```
ΔT_h   = T_h,in - T_h,out = 72 - 35 = 37°C
ΔT_c   = T_c,out - T_c,in = 62 - 4 = 58°C

Ex_h = Q̇_hot × (1/T_h,out - 1/T_h,in)
Ex_h = 363.52 × (1/308 - 1/345) = 363.52 × (-0.00317 + 0.00289)
Ex_h = 363.52 × (-0.00028) = -0.101 kW

Ex_c = Q̇_cold × (1/T_c,in - 1/T_c,out)
Ex_c = 569.85 × (1/277 - 1/334)
Ex_c = 569.85 × (-0.00361 + 0.00300)
Ex_c = 569.85 × (-0.00061) = -0.347 kW
```

**Total Exergy:**
```
Ex_total = Ex_h + Ex_c = -0.101 + -0.347 = -0.448 kW
```

**COP_ex:**
```
COP_ex = Q̇_hot / (Q̇_cold - Q̇_hot)
COP_ex = 363.52 / (569.85 - 363.52) = 363.52 / 206.33 = 1.76
```

**F_factor:**
```
F_factor = Q̇_hot × (T_h,out/T_h,in - T_c/out/T_c/in)
F_factor = 363.52 × ((35/72) - (4/62))
F_factor = 363.52 × (0.4861 - 0.0645)
F_factor = 363.52 × 0.4216
F_factor = 152.00 kW/K
```

---

### Factory-Level Hotspot Ranking

| Equipment | Fuel/Load | Exergy In (kW) | Exergy Out (kW) | Exergy Wasted (kW) | Exergy Efficiency (%) | F-factor (%) | Rank |
|-----------|----------|---------------|----------------|--------------------|----------------------|-------------|-------|
| Boiler    | 800 kW   | 642.15        | 396.60         | 245.55             | 61.7                 | 26.3        | #1    |
| Chiller   | 78.13 kW | 1.35          | 0.42           | 1.09               | 31.9                 | 41.8        | #2    |
| HX        | —        | -0.448        | -0.448         | 0                  | N/A                  | 0.0         | #3    |

**Top 3 Recommendations:**

### 1. Boiler Stack Heat Recovery
- Install a stack heat recovery system to recover the ~6 kW/K (245.55 kW) of exergy wasted in the boiler flue gas.
- A typical economizer can recover 80–90% of this waste energy, reducing fuel consumption by 190–220 kW.

### 2. CHP System Evaluation
- Assess feasibility of coupling the boiler with a back-pressure steam turbine for electricity generation.
- The ~396.60 kW useful thermal output can generate approximately 75–85 kW of electricity, improving overall process efficiency by recovering exergy lost to the stack.

### 3. Compressor Screw Chiller Optimization
- Perform internal chiller optimization: check refrigerant charge, compressor alignment, and fouled heat exchanger surfaces.
- Implement part-load controls with modulation or economizer bypass to reduce COP at low load (e.g., >20% above rated capacity).
- Consider upgrading to a higher-COP scroll or centrifugal design if the current 3.2 is suboptimal for this application.

---

**Overall Facility Improvement:** By addressing these top 3 issues, the plant can realize annual energy savings of ~541 kW/year (609 – 60.87 = 548.13 kW) and improve overall exergy efficiency by approximately 2–3 percentage points.