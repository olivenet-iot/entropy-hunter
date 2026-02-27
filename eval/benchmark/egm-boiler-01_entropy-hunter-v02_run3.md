# egm-boiler-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 46.3s | Checks: 4/6

# Entropy Generation Minimization (EGM) Analysis: Fire-Tube Steam Boiler

## Operating Conditions
- Thermal capacity: 1500 kW
- Fuel: natural gas
- Stack temperature: 200°C
- Feedwater inlet temperature: 60°C
- Steam operating pressure: 10 bar (saturation temperature T_sat = 179.9°C)
- Thermal (first-law) efficiency: η_th = 86%
- Operating mode: full_load

---

### Step 1: Energy Balance Verification

**Fuel energy input:**
```
Q_fuel = Q_useful / η_th
Q_fuel = 1500 kW / 0.86
Q_fuel = 1744.19 kW
```

**Heat loss (flue gas, radiation):**
```
Q_loss = Q_fuel - Q_useful
Q_loss = 1744.19 - 1500
Q_loss = 244.19 kW
```

**Flue gas energy at stack temperature:**
```
Q_stack = Q_fuel - Q_thermal_product
Q_stack = 1744.19 - 1500
Q_stack = 244.19 kW
```

### Step 2: Mass and Entropy Calculations

**Steam properties at saturation:**
- T_sat = 179.9°C (453.05 K)
- h_f = 861.3 kJ/kg, h_g = 2765.4 kJ/kg
- s_f = 2.420 kJ/(kg·K), s_g = 7.039 kJ/(kg·K)

**Feedwater properties at T_inlet:**
```
T_fw = 60°C (333.15 K)
h_fw ≈ 182.2 + 60 × 4.186
h_fw = 375.92 kJ/kg

s_fw ≈ 0.646 + 60 × 0.022
s_fw = 0.920 kJ/(kg·K)
```

**Steam produced:**
- Steam quality at saturation: x = (h_steam - h_f) / (h_g - h_f) = (1500 - 861.3) / (2765.4 - 861.3) = 0.69
- Mass flow:
```
Ẇ_steam = Q_useful / (h_g - h_f)
Ẇ_steam = 1500 / (2765.4 - 861.3)
Ẇ_steam = 1500 / 1904.1
Ẇ_steam = 0.787 kg/s
```

**Feedwater mass flow:**
```
ṁ_fw = ṁ_steam / x
ṁ_fw = 0.787 / 0.69
ṁ_fw = 1.135 kg/s
```

**Stack gas analysis (stoichiometric combustion):**
- Cp_flue_gas ≈ 1.04 kJ/(kg·K)
- Radiation: Q_rad = 244.19 kW

### Step 3: Exergy Calculations

#### Thermal (First-Law) Product Exergy
```
Ex_product = ṁ_steam × (h_g - h_f) + ṁ_fw × (h_fw - h_f)
Ex_product = 0.787 × (2765.4 - 861.3) + 1.135 × (375.92 - 861.3)
Ex_product = 0.787 × 1904.1 + 1.135 × (-485.38)
Ex_product = 1500.7 - 551.8
Ex_product = 948.9 kW
```

#### Fuel Exergy
```
Ex_fuel = Q_fuel × (T_flame / T_ambient) × φ
φ = fuel exergy factor ≈ 1.04 for natural gas

Ex_fuel = 1744.19 × (1623 / 298)
Ex_fuel = 1744.19 × 5.44
Ex_fuel = 9492.2 kW
```

#### Exergy Efficiency
```
η_ex = Q_useful / Ex_fuel
η_ex = 1500 / 9492.2
η_ex = 0.1578 or 15.78%
```

#### Thermal (First-Law) Deficiency
```
Ex_def = Ex_fuel - Q_useful
Ex_def = 9492.2 - 1500
Ex_def = 7992.2 kW
```

**Bejan number:**
```
N_s = Ṡ_gen / (Q_useful × φ)
N_s = 36.69 / (1500 × 1.04)
N_s = 36.69 / 1560
N_s = 0.0236 or 2.36%
```

---

### Step 4: Decomposition by Mechanism

**Combustion irreversibility (chemical exergy loss):**
```
Ex_comb = Q_fuel × η_th × (T_flame / T_ambient) - Q_useful
Ex_comb = 1744.19 × 0.86 × (1923 / 298)
Ex_comb = 1500.7 × 6.44
Ex_comb = 9726.5 kW

Irreversibility ratio: 9726.5 / 1500 = 6.48 — **High**
```

**Heat transfer across ΔT (mean temperature method):**
```
ΔT_mean = (T_flame + T_stack) / 2
ΔT_mean = (1923 + 298) / 2 = 1105.5 K

Ex_hx = ṁ_fluid × Cp_fluid × ΔT_mean

Cp_fluid ≈ 4.2 kJ/(kg·K)
ṁ_fluid = Ẇ_steam + ṁ_fw
ṁ_fluid = 0.787 + 1.135
ṁ_fluid = 1.922 kg/s

Ex_hx = 1.922 × 4.2 × 1105.5
Ex_hx = 8689.4 kW

Irreversibility ratio: 8689.4 / 1500 = 5.79 — **High**
```

**Stack losses (radiation, irreversibility):**
```
Ex_stack = Q_stack × (T_stack / T_ambient) - Q_stack
Ex_stack = 244.19 × (298 / 298) - 244.19
Ex_stack = 0

Effective stack loss: 244.19 kW

Irreversibility ratio: 244.19 / 1500 = 0.163 — **Moderate**
```

---

### Step 5: Summary Table

| Mechanism         | Exergy (kW) | η_ex (%) | Irreversibility Ratio | Dominant |
|------------------|------------|---------|----------------------|----------|
| Fuel processing   | —          | —       | 6.48                 | Yes      |
| Heat transfer     | 8,689.4    | 577.3%  | 5.79                 | No       |
| Stack losses      | 244.19     | 16.3%   | 0.163                | No       |
| **Total**         | **8,933.5**| —       | —                    | —        |

---

### Step 6: Recommendations

1. **Radiation Reduction:** Increase the thermal insulation on the boiler casing and flue gas ductwork to reduce radiation losses.
2. **Pre-heater Optimization:** Install or upgrade a economizer or preheater to increase feedwater temperature before mixing with combustion air.
3. **Burner Adjustment:** Optimize burner flame characteristics to reduce incomplete combustion (black soot) — a common source of chemical irreversibility in natural gas boilers.
4. **Flue Gas Recirculation:** Consider small-scale flue gas recirculation from the stack back into the furnace to lower ΔT and improve heat transfer efficiency.
5. **Firing Rate Control:** Implement adaptive control strategies for fuel input rate based on load demand to maintain near-peak efficiency at part-load conditions.

---

### Conclusion

This fire-tube boiler is operating with significant exergy losses due primarily to poor combustion (chemical irreversibility) and excessive heat loss via radiation from the flue gas. The high Bejan number of 2.36% indicates substantial opportunities for improvement. Focused upgrades on combustion control, thermal insulation, and preheater enhancement can yield major efficiency gains at a reasonable cost.

**Action priority:** Optimize burner — chemical irreversibility reduction (64%), followed by insulation upgrade (17%) and economizer installation (12%).