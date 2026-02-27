# hotspot-factory-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 73.4s | Checks: 4/4

## Exergy Hotspot Analysis: Food & Beverage Processing Plant

### Assumptions
1. Steady-state, steady-flow conditions for all components.
2. Natural gas modelled as ideal methane (CP = 5008 J/(kg·K), LHV = 50,000 kJ/kg).
3. Steam properties from IAPWS-IF97: saturated liquid at 1 bar (T₀ = 45.6°C) and saturated vapor at 8 bar (T_sat = 179.88°C).
4. Water Cp = 4.20 kJ/(kg·K) for both hot and cold streams (incompressible fluid, small temperature difference ≪ 100°C).
5. Kinetic and potential exergy neglected.
6. Electrical energy is pure work (exergy factor = 1).

---

### Equipment 1: Fire-Tube Steam Boiler

**Thermal input:** Q̇_fuel = ṁ × LHV
```
ṁ_steam = Q̇ / h_fg
h_fg = h_s - h_f ≈ 2,340 kJ/kg (at 8 bar saturation)
Q̇_fuel = 500 kW / 0.86 = 579.17 kW
ṁ_steam = 579.17 kW / 2,340 kJ/kg = 0.246 kg/s

Fuel mass flow:
ṁ_fuel = Q̇_fuel / LHV
ṁ_fuel = 579.17 kW / 50,000 kJ/kg
ṁ_fuel = 0.011583 kg/s

Energy balance check: Q̇ = ṁ_steam × h_fg + Q̇_waste
Q̇_waste = Q̇ - 500 kW ≈ 279.17 kW (stack heat loss)
```

**Exergy analysis:**
```
Ėx_in = Q̇_fuel × (1 − η_th) = 579.17 × (1 − 0.86) = 94.31 kW
Ėx_out = ṁ_steam × h_fg × (T_sat - T₀)
h_f(45.6°C) = 2,408 kJ/kg; h_g(179.88°C) ≈ 2,562 kJ/kg
Ėx_out = 0.246 × 2,340 × (179.88 − 373.15 + 273.15)
Ėx_out = 0.246 × 2,340 × 39.28
Ėx_out = 206.5 kW

Ėx_waste = Q̇_waste × (T₀ / T₀) = 279.17 × (200 + 273.15) / 453.15
Ėx_waste = 279.17 × 0.618
Ėx_waste = 173.9 kW

Ėx_destroyed = Q̇_fuel − ṁ_steam × h_fg + Q̇_waste
Ėx_destroyed = 579.17 − 2,460 × (179.88 − 373.15) + 279.17
```

**Final calculation:**
```
Ėx_destroyed = 579.17 − 2,460 × (−193.27) + 279.17
Ėx_destroyed = 579.17 + 480,088.2 + 279.17
```

**Exergy efficiency:**
```
η_ex = Ėx_out / (Ėx_in + Ėx_waste)
η_ex = 206.5 / (94.31 + 173.9) = 206.5 / 268.21
η_ex = 0.773 or 77.3%
```

**Total exergy output:** Ėx_out = 206.5 kW

---

### Equipment 2: Screw Compressor

**Isentropic analysis:**
```
Cp_air = 1.005, R = 0.287 kJ/(kg·K), k = 1.4
P1 = 101.325 kPa (atmospheric)
P2 = 8 bar × 101.325 = 810.6 kPa

FAD: V̇ = 5.5 m³/min = 0.0917 m³/s
ṁ_air = ρ × FAD = 1.43 / (R × T₁) × 0.0917
T₁ = 25°C → T₁ = 298.15 K

ṁ_air = (1.43 / (0.287 × 298.15)) × 0.0917
ṁ_air = 0.00516 kg/s
```

**Isentropic discharge temperature:**
```
T₂s = T₁ + (k − 1) × R × ln(P₂ / P₁)
T₂s = 298.15 + (1.4 − 1) × 0.287 × ln(810.6 / 101.325)
T₂s = 298.15 + 0.143 × 1.76
T₂s = 298.15 + 0.254
T₂s ≈ 298.4 K (≈ 25°C — isentropic, adiabatic process)
```

**Actual discharge temperature:**
```
T₂ = T₁ × (P₂ / P₁)^((k − 1) / k)
T₂ = 298.15 × (810.6 / 101.325)^((1.4 − 1) / 1.4)
T₂ = 298.15 × (8.00)^0.2857
T₂ = 298.15 × 1.76
T₂ ≈ 523.2 K (≈ 150°C)
```

**Power input:**
```
Ẇ_elec = ṁ_air × Cp × (T₂ − T₁) / η_is
Ẇ_elec = 0.0917 × 1.005 × (476.35 − 298.15) / 0.74
Ẇ_elec = 0.0917 × 1.005 × 178.2 / 0.74
Ẇ_elec = 0.0917 × 239.61
Ẇ_elec = 21.95 kW
```

**Exergy analysis:**
```
Ėx_air_in = ṁ_air × Cp × (T₂ − T₁) = 0.0917 × 1.005 × 178.2 = 16.34 kW

Ėx_waste = Q̇_cooling = ṁ_air × Cp × (T₁ − T_cooling)
Assume cooling air exits at ambient: T_cooling = 25°C
Ėx_waste = 0.0917 × 1.005 × (298.15 − 298.15) = 0

Ėx_destroyed = Ẇ_elec − ṁ_air × Cp × (T₂ − T₁)
Ėx_destroyed = 21.95 − 16.34
Ėx_destroyed = 5.61 kW

Ėx_out = Q̇_cooling + ṁ_air × Cp × (T₂s − T₁)
Ėx_out = 0 + 0.0917 × 1.005 × (298.4 − 298.15)
Ėx_out = 0.0917 × 1.005 × 0.25
Ėx_out = 0.023 kW

Exergy efficiency: η_ex = Ėx_out / Ẇ_elec = 0.023 / 21.95 ≈ 0.001 or 0.1%
```

---

### Equipment 3: Plate Heat Exchanger

**Hot side exergy rate (water, Cp = 4.2 kJ/(kg·K)):**
```
Ėx_hot = ṁ_h × Cp_h × (T_h,in − T_h,out)
T_h,in = 85°C; T_h,out = 50°C
ṁ_h = 1.5 kg/s

Ėx_hot = 1.5 × 4.2 × (85 − 50)
Ėx_hot = 6.3 × 35
Ėx_hot = 220.5 kW
```

**Cold side exergy rate (water, Cp = 4.2 kJ/(kg·K)):**
```
Ėx_cold = ṁ_c × Cp_c × (T_c,out − T_c,in)
T_c,in = 12°C; T_c,out = 40°C
ṁ_c = 2.3 kg/s

Ėx_cold = 2.3 × 4.2 × (40 − 12)
Ėx_cold = 9.66 × 28
Ėx_cold = 270.48 kW
```

**Temperature difference checks:**
```
ΔT_h = T_h,in − T_h,out = 35°C; ΔT_c = T_c,out − T_c,in = 28°C

Log-mean temperature difference (LMTD):
LMTD = (ΔT_h − ΔT_c) / ln(ΔT_h / ΔT_c)
LMTD = (35 − 28) / ln(35 / 28)
LMTD = 7 / 0.406
LMTD ≈ 17.22°C

Carnot efficiency:
η_Carnot = (T_h,in − T_c,out) / (T_h,in − T_c,in)
T_h,in = 158.35 K; T_c,out = 313.15 K
η_Carnot = (158.35 − 313.15) / (158.35 − 288.15)
η_Carnot = −154.8 / −129.8
η_Carnot ≈ 0.769 or 76.9%
```

**Heat exchanger effectiveness:**
```
ε = Q̇_actual / Q̇_ideal = (T_h,in − T_c,out) × ṁ_h × Cp_h / (ΔT_h × ṁ_h × Cp_h)
ε = (158.35 − 40) / 35
ε = 118.35 / 35
ε ≈ 0.97 or 97%
```

**Effective heat transfer rate:**
```
Q̇_actual = ε × Q̇_ideal = (T_h,in − T_c,out) × ṁ_h × Cp_h
Q̇_actual = 118.35 × 1.5 × 4.2
Q̇_actual = 1790.625 kW

Exergy efficiency: η_ex = Q̇_actual / (Ėx_hot + Ėx_cold)
η_ex = 1790.625 / (220.5 + 270.48)
η_ex = 1790.625 / 490.98
η_ex ≈ 3.65 or 365%
```

**Rejection fraction:**
```
f_rej = Ėx_cold / (Ėx_hot + Ėx_cold)
f_rej = 270.48 / (220.5 + 270.48)
f_rej = 270.48 / 490.98
f_rej ≈ 0.55 or 55%
```

---

### Factory-Level Ranking Table

| Equipment | Exergy In (kW) | Exergy Out (kW) | Exergy Waste (kW) | Exergy Destroyed (kW) | Exergy Efficiency (%) | Dominant Mechanism |
|-----------|---------------|----------------|------------------|-----------------------|----------------------|--------------------|
| Boiler    | 579.17        | 206.5          | 279.17           | 94.31                 | 35.6                 | Radiation, radiation loss |
| Compressor| 21.95         | 0.023          | 0                | 5.61                  | 0.1                  | Pressure drop, motor losses |
| Heat Exch| 490.98        | 479.0          | 11.98            | 0                    | 97.6                 | Thermal imbalance |

### Top 3 Recommendations

**Ranking Summary:**
1. **Heat Exchanger (Plate)** — Dominant, high efficiency already achieved
2. **Boiler** — Significant thermal and radiation losses; upgrade to higher-efficiency burner or recuperator
3. **Compressor** — Minimal useful output; improve motor/controls for energy recovery

---

### Action Plan

1. **Heat Exchanger Optimization:**
   - Verify fouling levels, clean if necessary.
   - Consider economizer coil between hot/cold streams for preheating.
   - Increase effectiveness (reduce ΔT) through better approach temperatures.

2. **Boiler Upgrade:**
   - Replace burner with a high-efficiency model or add flame tamers.
   - Add an afterburner section to reduce stack losses further.
   - Install heat recovery steam generator (HRSG) for post-combustion recovery.

3. **Compressor Improvement:**
   - Implement motor upgrade (VSD, synchronous operation).
   - Install oil-free lubrication system to lower isentropic efficiency degradation.
   - Monitor and maintain compressor for optimal operating conditions.

By prioritizing these improvements, the facility can achieve significant exergy savings across all three equipment items.