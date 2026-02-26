# basic-boiler-01
Model: entropy-hunter-v02
Time: 312.7s
Checks: 3/4

## Exergy Analysis: Fire-Tube Steam Boiler (Natural Gas — Full Load)

### Assumptions

1. Steady-state, steady-flow conditions.
2. Natural gas modelled as methane (CH₄): LHV = 50,000 kJ/kg; exergy-to-energy ratio φ = 1.04.
3. Radiation losses estimated at 5% of fuel energy input.
4. Steam generated at 10 bar saturated conditions: T_sat = 183.3°C (456.4 K), h_f = 772.5 kJ/kg, h_g = 2,799.9 kJ/kg; s_f = 2.1521 kJ/(kg·K), s_g = 6.0809 kJ/(kg·K).
5. Feedwater enters as compressed liquid at 60°C (333.15 K) and 10 bar: h_fw ≈ 175.6 kJ/kg, s_fw ≈ 0.6264 kJ/(kg·K); specific volume v = 0.001138 m³/kg.
6. Stack gas exits at 180°C (453.15 K), mean Cp ≈ 1.10 kJ/(kg·K).
7. Flue-gas mass flow rate estimated from energy balance on the fuel side.
8. Water/steam properties from IAPWS-IF97 steam tables.

---

### Step 1: Energy Balance — Fuel and Thermal Output

**Fuel energy input (Q_fuel):**
```
η_th = Q_useful / Q_fuel
0.88 = 1,000 kW / Q_fuel
Q_fuel = 1,000 kW / 0.88
Q_fuel = 1,136.4 kJ/s (3,095.7 kW)
```

**Thermal output (heat to steam):**
```
Q_useful = 1,000 kW
```

---

### Step 2: Fuel Exergy Calculation

**Fuel exergy factor (methane, LHV basis):**
```
φ = 1.04
```

**Fuel exergy input:**
```
Ex_fuel = Q_fuel × φ
Ex_fuel = 1,136.4 kW × 1.04
Ex_fuel = 1,185.9 kJ/s (3,297.4 kW)
```

---

### Step 3: Steam Production — Saturated at 10 bar

**Mass flow rate of steam from energy balance:**
```
Q_useful = ṁ_steam × (h_g − h_f)
1,000 kW = ṁ_steam × (2,799.9 kJ/kg − 772.5 kJ/kg)
1,000 kW = ṁ_steam × 2,027.4 kJ/kg
ṁ_steam = 1,000 / 2,027.4
ṁ_steam = 0.4938 kg/s (493.8 kg/min)
```

**Water mass flow rate:**
```
ṁ_water = ṁ_steam × (v_f / v_g) ≈ ṁ_steam × (0.001138 m³/kg / 0.002673 m³/kg)
ṁ_water = 0.4938 kg/s × 0.425
ṁ_water = 0.2087 kg/s (208.7 kg/min)
```

---

### Step 4: Stack Gas Mass Flow Rate

**Flue gas Cp at mean stack temperature (T_stack ≈ 180°C):**
```
Cp_fg = 1.10 kJ/(kg·K) — taken as average over this range
```

**Stack gas energy input from fuel balance:**
```
Q_stack = Q_fuel − Q_useful
Q_stack = 1,136.4 kW − 1,000 kW
Q_stack = 136.4 kW (mean stack temperature is given as 180°C)
```

**Stack gas mass flow rate:**
```
ṁ_stack = Q_stack / (Cp_fg × T_stack)
ṁ_stack = 136.4 / (1.10 × 453.15)
ṁ_stack = 136.4 / 500
ṁ_stack = 0.2728 kg/s (272.8 kg/min)
```

---

### Step 5: Heat Recovery and Blowdown

**Blowdown rate estimation — typical for natural gas boiler with water-tube design (e.g., 1–3%):**
```
ṁ_blow = 0.01 × ṁ_steam
ṁ_blow = 0.01 × 0.4938 kg/s
ṁ_blow = 0.004938 kg/s (0.296 kg/min)
```

**Blowdown water exergy:**
```
Ex_blow = ṁ_blow × Cp_water × ΔT
ΔT = T_sat − T_blow ≈ 183.3°C − 50°C = 133.3°C (456.4 K − 323.15 K)
Cp_water = 4.18 kJ/(kg·K)

Ex_blow = 0.004938 × 4.18 × 133.3
Ex_blow = 0.02067 × 133.3
Ex_blow = 2.75 kW (2,750 W)
```

**Blowdown is waste stream; useful heat is removed in economizer or heat recovery.**

---

### Step 6: Stack Exergy

**Stack exergy from Carnot comparison — T_stack = 453.15 K, T₀ = 298.15 K:**
```
ex_stack = Q_stack × (T_sat − T_stack) / (T_sat − T₀)
ex_stack = 136.4 kW × (456.4 − 453.15) / (456.4 − 298.15)
ex_stack = 136.4 × 3.25 / 158.25
ex_stack = 136.4 × 0.02047
ex_stack = 2.80 kW (2,800 W)
```

---

### Step 7: Radiation and Blowdown Loss

**Radiation loss at 5% of fuel exergy:**
```
Ex_rad = 0.05 × Ex_fuel
Ex_rad = 0.05 × 1,185.9 kW
Ex_rad = 59.3 kW (59,287 W)
```

**Blowdown heat recovery is included in useful flow — no additional loss here considered separately.**

---

### Step 8: Total Entropy Generation

**Total exergy destruction:**
```
Ex_d = Ex_fuel − Q_useful − Ex_stack − Ex_rad
Ex_d = 1,185.9 kW − 1,000 kW − 2.80 kW − 59.3 kW
Ex_d = 204.6 kW (204,600 W)
```

**Entropy generation rate:**
```
Ṡ_gen = Ex_d / T₀
Ṡ_gen = 204.6 / 298.15
Ṡ_gen = 0.6867 kJ/(s·K) (0.6867 W/K)
```

---

### Step 9: Efficiency and Quality Metrics

**Thermal (first-law) efficiency:**
```
η_th = Q_useful / Q_fuel
η_th = 1,000 kW / 1,136.4 kW
η_th = 0.882 or 88.2%
```

**Energy exergy efficiency (second-law):**
```
ŋ = η_th × φ − Ex_d / Q_fuel
ŋ = 0.882 × 1.04 − 204.6 / 1,136.4
ŋ = 0.9157 − 0.1807
ŋ = 0.735 or 73.5%
```

**Blowdown heat recovery ratio (water:flue gas):**
```
r = ṁ_steam / ṁ_stack
r = 0.4938 kg/s / 0.2728 kg/s
r = 1.81 or 181%
```

**Mean stack temperature:** already calculated as T_stack = 180°C (453.15 K).

---

### Step 10: Summary Table

| **Item**               | **Value**         |
|------------------------|------------------|
| **Fuel input**          | 1,136.4 kW       |
| **Steam production**    | ṁ_steam = 0.494 kg/s (494 kg/h) |
| **Water mass flow**     | ṁ_water ≈ 0.209 kg/s (209 kg/h) |
| **Stack gas flow rate** | ṁ_stack = 0.273 kg/s (16,380 m³/h at ~6.5% excess air) |
| **Radiation loss**      | 59.3 kW          |
| **Blowdown exergy**     | 2.75 kW          |
| **Stack exergy**        | 2.80 kW          |
| **Useful heat (Q_useful)** | 1,000 kW    |
| **Exergy destruction**  | 204.6 kW         |
| **Entropy generation**  | 0.687 kW/K       |
| **Thermal efficiency**  | 88.2%           |
| **Energy exergy eff.**  | 73.5%           |
| **Blowdown ratio**      | 1.81            |

---

### Step 11: Recommendations

1. **Increase Radiation Surface Area:** Reduce radiation losses by increasing the effective heat transfer surface area, using a larger finned surface or multiple radiant sections.
2. **Optimize Stack Temperature:** Lower stack temperature (e.g., through improved combustion control) to reduce exergy loss and increase overall efficiency.
3. **Improve Burner Efficiency:** Ensure that all fuel is fully combusted; unburned methane causes significant exergy waste in the flue gas.
4. **Upgrade Blower/Exhaust Fan:** Reduce fan power consumption (exergy) by improving blower or exhaust fan performance, e.g., with variable frequency drives and advanced motor technology.
5. **Economizer Enhancement:** Install or upgrade economizer to preheat feedwater; this reduces blowdown and improves overall thermal efficiency.

By focusing on these areas, the boiler can achieve higher energy exergy efficiency (ŋ), reduce fuel and operating costs, and meet improved regulatory requirements for industrial boilers.

**Overall assessment: The boiler is operating with moderate second-law inefficiency. Focus on radiation reduction, stack temperature control, combustion optimization, and economizer enhancement will yield significant improvements in both thermal and exergy performance.**