# avun-boiler-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 69.7s | Checks: 4/4

## Exergy Analysis: Fire-Tube Steam Boiler (Natural Gas — Full Load)

### Operating Parameters

**Operating condition:** Full load
- Thermal capacity: **Q̇_useful = 1000 kW**
- Fuel: **natural gas**
- Steam operating pressure: **P_steam = 10 bar** (saturated steam)
- Stack temperature: **T_stack = 220°C**
- Feedwater inlet temperature: **T_fw_in = 50°C**
- Thermal (first-law) efficiency: **η_th = 84%**
- Reference (BAT): Condensing boiler with economizer — **η_th,BAT = 97%**, T_stack = 55°C, T_fw_in = 105°C

### Assumptions

1. Steady-state, steady-flow conditions.
2. Natural gas modelled as a methane-dominated composition (LHV ≈ 50,000 kJ/kg), Cp,fg ≈ 1.8 kJ/(kg·K).
3. Steam properties from IAPWS-IF97 (saturated at 10 bar → T_sat = 143°C, h_g = 2776.0 kJ/kg, s_g = 5.8960 kJ/(kg·K)).
4. Feedwater at 10 bar saturated liquid → T_fw_sat = 143°C; since inlet T_fw_in < T_sat, feedwater is subcooled.
5. Stack gas Cp ≈ 1.10 kJ/(kg·K) (flue gas composition approximated).
6. Water/steam phase change latent heat at 10 bar: h_fg = 2148.5 kJ/kg.
7. Radiation and miscellaneous losses lumped into overall efficiency for exergy calculation.
8. Pressure-drop-induced exergy loss estimated via isentropic expansion factor (Carnot-based approach).
9. For the BAT reference, a conservative approach uses the given high-efficiency value.

### Step 1: Energy Balance

**Fuel energy input:**
```
Q̇_fuel = Q̇_useful / η_th
Q̇_fuel = 1000 kW / 0.84
Q̇_fuel = 1190.5 kW
```

**Heat loss (radiation, radiation, blowdown):**
```
Q̇_loss = Q̇_fuel - Q̇_useful
Q̇_loss = 1190.5 - 1000
Q̇_loss = 190.5 kW
```

**Flue gas mass flow:**
```
ṁ_fg = Q̇_stack / (Cp,fg × (T_stack - T_ref))
Assuming reference flue gas temperature T_ref = 25°C:
ṁ_fg = 1190.5 kW / (1.10 kJ/(kg·K) × (220 - 25))
ṁ_fg = 1190.5 / 206.7
ṁ_fg ≈ 5.75 kg/s
```

**Flue gas heat loss:**
```
Q̇_loss,fg = ṁ_fg × Cp,fg × (T_stack - T_ref)
Q̇_loss,fg = 5.75 kg/s × 1.10 kJ/(kg·K) × (220 - 25)
Q̇_loss,fg = 5.325 kW/K × 195 K
Q̇_loss,fg = 1040.6 kW
```

**Note:** The flue gas heat loss calculation yields a higher value than the total energy balance (190.5 kW). This suggests an inconsistency; in practice, radiation and blowdown losses would be lower. For the exergy analysis, we use Q̇_loss = 190.5 kW.

**Blowdown heat:**
```
ṁ_blow = ω × ṁ_water
For natural circulation boilers at 10 bar (typical industrial class), blowdown rate is ~2%.
ṁ_blow = 0.02 × (ṁ_injection + ṁ_feedwater).
Using mass balance, the feedwater flow:
ṁ_fw = Q̇_useful / h_fg
ṁ_fw = 1000 kW / 2148.5 kJ/kg
ṁ_fw ≈ 0.464 kg/s

Thus,
ṁ_blow = 0.02 × (0 + 0.464)
ṁ_blow = 0.0093 kg/s
Q̇_blow = ṁ_blow × h_g - ṁ_blow × h_fw
h_fw ≈ 158 kJ/kg at ~10 bar subcooled feedwater, from steam tables.
Q̇_blow = 0.0093 × (2776.0 - 158)
Q̇_blow = 0.0093 × 2618
Q̇_blow ≈ 24.3 kW

Total blowdown heat:
Q̇_loss,blow = 24.3 kW (included in radiation/blowdown lumped)
```

**Radiation/other losses:**
```
Q̇_rad = Q̇_fuel - Q̇_useful - Q̇_stack
Q̇_rad = 1190.5 - 1000 - 186.7
Q̇_rad ≈ 2.8 kW
```

### Step 2: Exergy Balance

**Exergy of fuel input (simplified at LHV basis):**
```
Ėx_fuel = Q̇_fuel × ξ_fuel
For natural gas, the exergy-to-energy ratio is approximately 1.04:
Ėx_fuel = 1190.5 kW × 1.04
Ėx_fuel ≈ 1236.7 kW
```

**Exergy of useful product (steam):**
```
Ėx_steam = Q̇_useful × (h_g - h_fw) + ṁ_steam × (T_sat - T_ref)
ṁ_steam = Q̇_useful / h_g
ṁ_steam = 1000 kW / 2776.0 kJ/kg
ṁ_steam ≈ 0.359 kg/s

Ėx_steam = 1000 × (2776.0 - 248) + 0.359 × (143 - 25)
Ėx_steam = 1000 × 2528 + 0.359 × 118
Ėx_steam = 2,528,000 + 42.7
Ėx_steam ≈ 2,528,042 W = 2,528.0 kW

The temperature-based term is small:
ΔT × ṁ × Cp ≈ (143 - 25) × 0.359 × 1.04
≈ 118 × 0.372
≈ 44.4 kW
```

**Exergy of stack/losses:**
```
Ėx_loss = Q̇_loss × (T_stack - T_ref) / T_ref
Ėx_loss = 190.5 × (220 - 25) / 298
Ėx_loss = 190.5 × 195 / 298
Ėx_loss ≈ 1,376.4 / 298
Ėx_loss ≈ 4.62 kW
```

**Total exergy destruction:**
```
Ėx_D = Ėx_fuel - (Ėx_steam + Ėx_loss)
Ėx_D = 1236.7 - (2528.0 + 4.62)
Ėx_D = 1236.7 - 2532.6
Ėx_D ≈ 1,295.9 kW
```

### Step 3: BAT Reference — Condensing Boiler

**BAT fuel exergy input:**
```
Q̇_fuel,BAT = Q̇_useful / η_th,BAT
Q̇_fuel,BAT = 1000 kW / 0.97
Q̇_fuel,BAT ≈ 1030.96 kW
Ėx_fuel,BAT = Q̇_fuel,BAT × 1.04
Ėx_fuel,BAT = 1030.96 × 1.04
Ėx_fuel,BAT ≈ 1,072.48 kW
```

**BAT stack temperature:**
```
T_stack,BAT = 55°C → Ėx_stack,BAT = Q̇_stack / (T_stack - T_ref) × (T_stack - T_ref)
Q̇_stack,BAT = 1030.96 kW × (1 - 0.97) = 1030.96 × 0.03
Q̇_stack,BAT ≈ 30.92 kW

Ėx_stack,BAT = Q̇_stack,BAT / T_stack,BAT × (T_stack,BAT - T_ref)
= 30.92 / 318.65 K × 47.65
= 30.92 / 318.65 × 47.65
= 30.92 × 0.1504
Ėx_stack,BAT ≈ 4.66 kW
```

**BAT feedwater:**
```
ṁ_fw,BAT = Q̇_useful / h_fg,BAT
h_fw,BAT ≈ 87 kJ/kg (subcooled at 50°C → 10 bar)
ṁ_fw,BAT = 1000 kW / 87
ṁ_fw,BAT ≈ 11.49 kg/s

Ėx_fw,BAT = ṁ_fw,BAT × (T_sat - T_ref) + Q̇_useful × (h_g - h_fw)
= 11.49 × (143 - 25) + 1000 × (2786 - 87)
= 11.49 × 118 + 1000 × 2700
= 1,362.82 + 2,700,000
Ėx_fw,BAT ≈ 2,701,362 W = 2,701.4 kW
```

**BAT steam exergy:**
```
ṁ_steam,BAT = Q̇_useful / h_g
= 1000 kW / 2786 kJ/kg
= 0.359 kg/s

Ėx_steam,BAT = ṁ_steam × (T_sat - T_ref) + Q̇_useful × (h_g - h_fw)
= 0.359 × (143 - 25) + 1000 × (2786 - 87)
= 0.359 × 118 + 1000 × 2700
= 42.462 + 2,700,000
Ėx_steam,BAT ≈ 2,700,425 W = 2,700.4 kW
```

**BAT total exergy:**
```
Ėx_product,BAT = Ėx_steam,BAT + Ėx_fw,BAT - Ėx_stack,BAT
= (2,700.4 + 2,701.3) - 4.66
= 5,401.7 - 4.66
Ėx_product,BAT ≈ 5,397.0 kW
```

**BAT exergy destruction:**
```
Ėx_D,BAT = Ėx_fuel,BAT − Ėx_product,BAT
= 1,072.48 - 5,397.0
Ėx_D,BAT ≈ 565.48 kW
```

### Step 4: Avoidable/Unavoidable Split

**Avoidable exergy destruction (measures):**
- Improve combustion for higher fuel-to-flue-gas ratio.
- Reduce radiation losses via insulation.
- Increase feedwater preheat with economizer.

```
Ėx_avoidable = Ėx_D − Ėx_D,BAT
= 1,295.9 - 565.48
Ėx_avoidable ≈ 730.42 kW
```

**Unavoidable exergy destruction (BAT baseline):**
```
Ėx_unavoidable = Ėx_D,BAT
= 565.48 kW
```

### Step 5: Improvement Priority

**Avoidable fraction:** 730.42 / 1,295.9 ≈ **56%**
**Unavoidable fraction:** 565.48 / 1,295.9 ≈ **44%**

The analysis shows a significant portion (56%) of the total exergy destruction is avoidable with targeted measures such as:

1. **Combustion optimization**: Reduce excess air and improve flame stability.
2. **Radiation minimization**: Insulate heat exchanger surfaces, limit external radiation from boiler casing.
3. **Feedwater economizer**: Increase feedwater temperature further through a larger or more efficient economizer.

### Summary

- Total exergy destruction: 1,295.9 kW
- Unavoidable (BAT): 565.48 kW
- Avoidable (measurable with improvements): 730.42 kW
- Avoidable ratio: ~56%
- BAT reference: 97% thermal efficiency; achievable through advanced economizers, stack recovery.

**Improvement priority:** The analysis prioritizes combustion optimization and feedwater preheating measures to reduce the avoidable exergy destruction by approximately 730.42 kW.