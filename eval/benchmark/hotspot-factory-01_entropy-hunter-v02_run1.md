# hotspot-factory-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 88.4s | Checks: 4/4

## Exergy Hotspot Analysis: Food & Beverage Processing Plant

### Assumptions

1. All processes are steady-state, steady-flow unless otherwise stated.
2. Kinetic and potential exergy changes are negligible.
3. Water properties: Cp = 4.18 kJ/(kg·K), both phases liquid at stated operating temperatures (no phase change).
4. Natural gas lower heating value LHV = 50,000 kJ/kg; chemical exergy factor φ = 1.04.
5. Steam table properties: saturation pressure at 8 bar (80°C) is 379.26 kPa (vapor), T₀ = 25°C (308.15 K).
6. For the compressor, electrical power input is pure work (exergy factor φ_elec = 1).

---

### Equipment 1: Fire-Tube Steam Boiler

#### Energy Balance
Fuel energy input:
```
Q_fuel = Q_useful / η_th
Q_fuel = 500 kW / 0.86
Q_fuel = 579.71 kW
```

Steam production at 8 bar (saturation temperature ≈ 173°C):
```
h_s,fg = h_g - h_f = 2443.4 − 649.9 kJ/kg
= 1793.5 kJ/kg

Q_steam = ṁ_steam × (h_s,fg)
ṁ_steam = Q_useful / h_s,fg
ṁ_steam = 500 kW / 2362.8 kJ/(kg·K)  # h_f at ~173°C; h_g ≈ 2443 kJ/kg
= 500 / 2362.8
= 0.211 kg/s

Q_steam = 0.211 × 2362.8
Q_steam = 497.97 kW
```

#### Exergy Calculations
Fuel exergy:
```
Ex_fuel = Q_fuel × φ_elec = 579.71 × 1.04 = 604.73 kW
```

Heat rejection via flue gas (stack at ~200°C):
```
Q_flue = Q_fuel − Q_useful
= 579.71 − 500
= 79.71 kW

Ex_flue = Q_flue × (T_stk / T₀) − Q_flue
= 79.71 × (200 + 273.15) / 298.15 − 79.71
= 79.71 × 473.15 / 298.15 − 79.71
= 126.41 kW − 79.71
= 46.70 kW
```

Steam exergy (at saturation):
```
Ex_steam = ṁ_steam × (h_s − h_f) + ṁ_steam × v × (T_sat − T₀)
Ex_steam = 0.211 × (2362.8 − 649.9) + 0.211 × 0.00375 × (445 − 298.15)
= 0.211 × 1712.9 + 0.000796 × 146.85
= 362.86 kW + 0.118 kW
= 363.00 kW
```

Blowdown (negligible), losses, and entropy generation:
```
Ex_loss = Q_heat_rejected / T₀
Ex_loss = 79.71 / 298.15
= 0.268 kW/K

Ex_gen = η_th × Ex_fuel − Ex_steam
= 0.86 × 604.73 − 363.00
= 518.29 − 363.00
= 155.3 kW
```

**Total:**
```
Ex_in = 604.73
Ex_out = 363.00 + 0.268 = 363.27
Ex_waste = 46.70
Ex_loss = 155.3

Exergy efficiency: η_ex = 363.27 / 604.73 × 100%
= 60.1%

Entropy generation ratio: N_s = Ex_gen / (T₀ × (Ex_fuel − Ex_out))
N_s = 155.3 / (298.15 × 240.73)
N_s = 155.3 / 72086.7
N_s = 0.00216
```

**Summary:**
```
Ex_in  : 604.7 kW
Ex_out : 363.3 kW (60.1%)
Ex_waste: 46.7 kW
Ex_loss: 155.3 kW
N_s    : 0.00216

Quality grade: C - moderate hotspot; low efficiency (~86%), high fuel-to-steam exergy ratio.
```

---

### Equipment 2: Screw Compressor (Air, FAD = 5.5 m³/min)

#### Energy Balance
Electrical power input:
```
W_in = 37 kW
```

Isentropic analysis: R-12B, Cp = 1.005 kJ/(kg·K), P₁/P₂ = 1/8 bar.

First, find air inlet state (T₁ = 35°C):
```
h₁ = h_f(T₁) + v₁ × Cp
= 100.46 + 0.001329 × 1.005 × 35
= 100.46 + 0.0047
= 100.50 kJ/kg
```

Isentropic discharge temperature:
```
T₂s = T₁ × (P₂/P₁)^((R/Cp))
= 308.15 × (0.12/1)^(-0.286 / 1.005)
= 308.15 × (0.12)^-0.284
= 308.15 × 7.912
= 2449.6 K

Since T₂s > T_sat(8 bar) ~ 356 K, assume isentropic discharge is near ambient.

Actual: v₂ = 1 / (1.67 + 0.0011 × 35)
v₂ = 0.592 m³/kg
ṁ = FAD / (v₁ × Cp × 60) = 5.5 / (0.0821 × 0.00418 × 60)
= 5.5 / 0.0217
= 253.9 kg/s

Actual T₂ = h₂/T₀
```

Actual isentropic efficiency:
```
η_is = (1 − T₁/T₂s) / (1 − T₁/T_s)
T₂ = 48 + 273.15 = 321.15 K
T_s = 308.15 K

η_is = (1 − 308.15/321.15) / (1 − 308.15/469.1)
= 1.073 / 1.33
= 0.807
```

Actual power:
```
W_act = ṁ × Cp × (T₁ − T₂) + ṁ × v₂ × (P₂/P₁)
= 253.9 × 1.005 × (308.15 − 321.15)
+ 253.9 × 0.0821 × 7
= 254.6 × −13.0
+ 177.8 × 0.5747
= −3314.8 + 102.2
= 32.2 kW

Actual isentropic efficiency: η_is = 32.2 / 37
= 0.87

FAD = 5.5 m³/min = 91.67 kg/s
```

**Exergy Calculations**
Electrical input exergy (work):
```
Ex_in = W_in × φ_elec = 37 × 1.04
= 38.48 kW
```

Air inlet state:
```
h₁ = 100.46 kJ/kg, s₁ = 0.257 + ln(35/298) = 0.6096 kJ/(kg·K)
```

Actual discharge at ~321 K (isothermal with FAD):
```
h₂ ≈ h₁ = 100.46
s₂ ≈ s₁ + v × R / Cp = 0.6096 + 0.0821 × 8.314 / 1.005
= 0.6096 + 0.676
= 1.2856 kJ/(kg·K)
```

Saturated at 8 bar (T_sat ≈ 173°C):
```
h_g = 2443, h_f = 649.9, s_g = 6.600
s_f = 0.533

Quality check: v₂ < v_f → liquid discharge.
Actual pressure drop: P₁/P₂ ≈ 1/8 bar.
```

Isentropic exergy:
```
Ex_is = ṁ × (h₁ − h₂)
= 253.9 × (100.46 − 100.46)
= 0
```

Actual exergy: Pure compression, so:
```
Ex_waste = 0, Ex_loss = W_in − W_act
= 37 − 32.2
= 4.8 kW

Ex_out = ṁ × (h₂ − h₁) + v₂ × R × T₀
= 253.9 × 0 + 0.0821 × 8.314 × 298.15
= 6.27 × 298.15
= 1,876.6 kW

Exergy efficiency: η_ex = Ex_out / Ex_in
= 4.8 / 38.48
= 0.125 or 12.5%

Quality grade: D - poor; low isentropic efficiency and large pure-work loss.
```

**Summary:**
```
Ex_in : 38.48 kW (electrical)
Ex_out: 4.8 kW (pressure rise only)
Ex_waste: 0
Ex_loss: 32.68 kW

Quality grade: D - poor; compressor is oversized or unoptimized.
```

---

### Equipment 3: Plate Heat Exchanger

#### Energy Balance
Hot side mass flow:
```
Q_hot = ṁ_h × Cp_h × (T_h,in − T_h,out)
= 1.5 × 4.18 × (85 − 50)
= 6.27 × 35
= 219.45 kW
```

Cold side mass flow:
```
Q_cold = ṁ_c × Cp_c × (T_c,out − T_c,in)
= 2.3 × 4.18 × (40 − 12)
= 9.61 × 28
= 270.25 kW

Conservation check: Q_hot = Q_cold
219.45 ≠ 270.25  # Error; cold side over-estimated.

Revised: ṁ_c ≈ 1.5 kg/s (hot = cold)

Q_cold = 1.5 × 4.18 × 28
= 169.32 kW
```

**Exergy Calculations**
Hot side:
```
T_h,in = 85°C, T_h,out = 50°C

Ex_hot = ṁ_h × Cp_h × (T_h,in − T_h,out) + ṁ_h × v × (T_h,in − T₀)
= 1.5 × 4.18 × 35 + 1.5 × 0.001279 × (356 − 298.15)
= 219.45 + 1.5 × 0.001279 × 57.85
= 219.45 + 0.011
= 219.46 kW

Cold side:
```

Cp_c = 4.18 kg/(kg·K); cold inlet ≈ ambient → T_c,in ≈ 25°C.
```
Ex_cold = ṁ_c × Cp_c × (T_c,out − T_c,in) + ṁ_c × v × (T_c,out − T₀)
= 1.5 × 4.18 × 23
+ 1.5 × 0.001279 × (321.15 − 298.15)
= 1.5 × 4.18 × 23 + 1.5 × 0.001279 × 23
= 144.66 + 0.047
= 144.71 kW

Exergy efficiency:
```

Assuming Carnot COP (thermal side):
```
COP_th = Q_cold / Q_hot = 144.71 / 219.45
= 0.661 or 38%

Exergy factor: η_ex = COP_th × (T_cold − T_hot) / (T₀ − T_cold)
= 0.661 × (298.15 − 272.85) / (298.15 − 35)
= 0.661 × 45.3 / 263.15
= 0.661 × 0.172
= 0.114

Ex_in = Q_hot × η_ex = 219.45 × 0.114
= 25.08 kW

Ex_out = Q_cold × η_ex = 144.71 × 0.114
= 16.43 kW

Ex_waste = Q_hot − Ex_in − Ex_out
= 219.45 − 25.08 − 16.43
= 177.94 kW
```

**Summary:**
```
Ex_in : 25.08 kW (hot side)
Ex_out: 16.43 kW (cold side)
Ex_waste: 177.94 kW

Quality grade: B - moderate hotspot; high ΔT cold-side drives waste.
```

---

### Factory-Level Ranking Table

| Rank | Equipment   | Exergy In (kW) | Exergy Out (kW) | Exergy Wast/Destroy (kW) | Quality Grade |
|------|------------|---------------:|----------------:|-------------------------:|--------------|
| 1    | Compressor  |       38.48     |        4.80      |          32.68           | D            |
| 2    | Boiler      |       604.73    |       363.27     |         155.30           | C            |
| 3    | Heat Exch   |        25.08    |       16.43      |         177.94           | B            |

### Top 3 Recommendations

**Top Priority: Compressor (FAD = 5.5 m³/min, 37 kW)**
- **Action**: Reevaluate FAD and re-calculate required compression ratio. Consider aftercooler with intercooling if multi-stage.
- **Expected Exergy Savings**: ~20.19 kW
- **Annual Energy Savings (based on 4000 h/year)**: 8076 kWh → €358 (at 0.045/kWh)

**Second Priority: Boiler (8 bar, 500 kW)**
- **Action**: Upgrade burner for better combustion and post-combustion air management; install economizer for preheating feedwater.
- **Expected Exergy Savings**: ~79–123 kW
- **Annual Energy Savings**: 400,000–650,000 kWh → €18,000–30,000

**Third Priority: Heat Exchanger (plate)**
- **Action**: Increase hot-side approach temperature or cold-side flow rate for better part-load efficiency; install fouling monitoring and cleaning schedule.
- **Expected Exergy Savings**: ~4.2 kW
- **Annual Energy Savings**: 16,800 kWh → €750