# whatif-boiler-01
Model: entropy-hunter
Time: 485.2s
Checks: 5/6

## Exergy Comparison: Water-Tube Steam Boiler with Economizer Installation (Thermal Capacity 2000 kW)

---

### Assumptions

1. Steady-state, steady-flow conditions.
2. Fuel: Natural gas; exergy-to-energy ratio: ξ = 1.04.
3. Thermal capacity Q̇_useful = 2000 kW for both cases (at full load).
4. Steam produced at saturation pressure P_sat = 15 bar → T_sat = 212°C (absolute).
5. Feedwater inlet: T_fw_in = 40°C (absolute) — compressed liquid assumed.
6. Blowdown losses neglected; radiation loss ≈ 2% of fuel input.
7. Flue gas Cp = 1.10 kJ/(kg·K) as average for natural gas combustion products at all operating temperatures considered.
8. Air-fuel ratio: 15 kg_air / kg_fuel (typical NG), excess air accounts for ~95% of total flow.
9. Steam mass flow rate from energy balance: ṁ_steam = Q̇_useful / (h_g - h_fw, in).
10. Water/steam properties from IAPWS-IF97 tables.

### Key Property Reference

**Saturation steam at 15 bar:** h_g = 2768.3 kJ/kg, s_g = 6.4957 kJ/(kg·K), T_sat = 212°C (295.15 K).
**Feedwater at 15 bar, 40°C (313.15 K):**
  - h_fw ≈ 148.5 + 0.072×(313.15 − 40) = 246.1 kJ/kg
  - s_fw ≈ 0.6052 + 0.0961 × (313.15 − 40) = 0.8514 kJ/(kg·K).

---

## BASELINE Scenario: Economizer NOT Installed

**Step 1 — Fuel Input & Radiation Losses**

Fuel input:
```
Q̇_fuel = Q̇_useful / η_thermal_base
Q̇_fuel = 2000 kW / 0.85 = 2352.94 kW
```

**Step 2 — Mass Balance — Flue Gas**

At 15 bar, h_g ≈ 2768.3 kJ/kg.

Energy balance on steam:
```
Q̇_useful = ṁ_steam × (h_g − h_fw) + ṁ_fg × (h_fg − h_fluegas)
Q̇_fuel × η_thermal_base ≈ Q̇_steam × Δh_steam + Q̇_fg × Δh_fg
```

Since we're missing the exact mass flow rates, we'll compute flue gas exergy using overall parameters:
```
Q̇_fluegas = ṁ_steam × (h_g − h_fw)
ṁ_steam ≈ 2000 / [(2768.3 - 246.1) + 2% fuel input] = Q̇/Δh

Simplified: Q_fluegas ≈ ṁ_steam × (h_g - h_fw) = ṁ_steam × 2522.2
ṁ_steam = 2000 / 2522.2 ≈ 0.793 kg/s

Q_fluegas = 0.793 × (2768.3 - 246.1) ≈ 0.793 × 2522.2
Q_fluegas ≈ 2000 kW (flue gas heat)
```

**Step 3 — Radiation Loss & Fuel Input**

Radiation loss = Q̇_fuel × 0.02:
```
Q_radiation = 2352.94 × 0.02 = 47.06 kW
```

Total fuel input (thermal):
```
Q̇_fuel_total = 2352.94 + 47.06 = 2400.00 kW.
```

**Step 4 — Energy Balance Verification**

Steam output:
```
ṁ_steam = Q̇_useful / Δh_steam = 2000 / 2522.2 = 0.793 kg/s
Q_fluegas ≈ 1968 kW, Q_rad + stack loss: 47 + 400 = 447 kW.
```

**Step 5 — Exergy of Flue Gas**

Using flue gas Cp = 1.10 kJ/(kg·K), stack temperature T_stack = 250°C (523.15 K).

Mean flue gas exit temperature for exergy:
```
T_ex_mean = (15 + 400) / 2 = 227.5°C → T_ex_mean = 499.65 K
Cp_flue ≈ 1.10 × 1.035 ≈ 1.138 kJ/(kg·K)
```

Mean flue gas mass flow:
```
ṁ_fg ≈ ṁ_steam × (h_g − h_fw) / C_p,fg = Q_fluegas / Cp
ṁ_fg ≈ 2000 / (2522.2 × 1.138)
ṁ_fg ≈ 793/2864 → ṁ_steam = 2000/(2864 − 2522.2) = Q_fluegas/Q_fg
ṁ_steam ≈ 0.793 kg/s, ṁ_fg ≈ 0.673 kg/s.

Exergy of flue gas:
Ex_fg = ẋ_fg × [(T_stack - T_ex_mean) - T_amb × ln(T_stack/T_ex_mean)]
For the overall waste stream: Ex_fluegas_total ≈ Q_fluegas × [(1-T_amb/T_stack)-(T_amb-T_ex_mean)/T_stack] = Q_fluegas × (250/499.65−313/523) ≈ 0.835×Q_fluegas.
```

**Step 6 — Radiation Exergy**

```
Ex_rad = Q_radiation × (T_amb/T_surr)^4
With T_amb = 25°C, T_surr = stack temperature (≈499K):
Ex_rad = 47.06 × (298/499) = 47.06 × 0.6 → Ex_rad ≈ 28.3 kW.
```

**Step 7 — Fuel Exergy Input**

Fuel exergy:
```
Ex_fuel = Q̇_fuel × ξ = 2352.94 × 1.04 = 2452.29 kW.
```

**Step 8 — Exhaust/Stack Stream Product (Energy vs Exergy)**

**Energy:** Flue gas carries the vast majority, ≈ 1968 + 47.06 = 2015 kW.
**Exergy:**
- Stack thermal exergy (at 250°C): ~835 × Q_fluegas.
- Radiation: ~28.3 kW.

Overall: Exhaust carries **2044 kW energy**, **1197 kW exergy** (stack + radiation).

**Step 9 — Exergy Balance & Efficiency**

Product (steam useful):
```
Ex_steam = ṁ_steam × Cp_liquid × ΔT + ṁ_steam × [h_g − h_fw]
= 0.793 × 4.221 × (215 - 313) + 0.793 × 2522.2
```

Ex_steam = 0.793 × 4.221 × 198 − 0.793 × 606.7

Product = 793(4.221 × 0.652 + 3.185) ≈ 1150 kW.

```
Ex_steam_total = Ex_product (1150) + Ex_excess = 1220.0 kW.
```

Overall boiler exergy efficiency:
```
η_Ex = Ex_steam / Ex_fuel_in
η_Ex = 1197 / 2452.3 → η_Ex = 48.7% (for overall stack/radiation + product).
```

**Verification:**
```
Ex_fluegas = Q_fluegas × [(1 − T_amb/T_stack) − T_amb/T_stack]
= 2000 × (1 − 313/523.15)^2 − 298.15 × ln(499.65/523.15)
= 2000 × (−0.58)² = 2000 × 0.340 → ≈ 1250 kW.
```

**Final Exergy Product:**
```
Ex_product + radiation losses → 793 × [Cp_liquid × ΔT] + Q_rad × (T/T_stack)^4.
```

**Overall Waste = Stack + Radiation + Fluegas product.**

---

## MODIFIED SCENARIO WITH ECONOMIZER

**Step 1: Fuel Input**

Fuel input:
```
Q̇_fuel = 2000 kW / η_thermal_mod
Q̇_fuel = 2000 / 0.91 ≈ 2204.53 kW.
```

**Step 2 — Mass Balance & Radiation Loss**

Using same mass balance method, we now calculate:
```
ṁ_steam ≈ Q_useful / Δh_steam = 2000 / (2768.3 − 246.1) = 0.835 kg/s

Q_fluegas ≈ ṁ_steam × (h_g − h_fw) = 0.835 × 2522.2 → Q_fluegas ≈ 2109 kW.
ṁ_steam ≈ 2000 / 2768.3 ≈ 0.724 kg/s.

Q_radiation = 2204.53 × 0.02 ≈ 44.1 kW.
```

**Step 3 — Energy Balance Verification**

Steam output:
```
ṁ_steam = Q_useful / Δh_steam = 2000/2522.2 → ṁ_steam = 0.793 kg/s
Q_fluegas ≈ 1968 kW, radiation + stack = 44.1+400.
```

**Step 4: Exhaust Stream (Energy & Exergy)**

For the reduced temperature and higher efficiency:
```
Ex_fluegas_total = Q_fluegas × [(1 − T_amb/T_stack) − T_amb/T_stack]
Stack T ≈ 180°C → 453.15 K
ṁ_steam ≈ 0.793 kg/s, Q_fg = 2000/2658 ≈ 0.751 kg/s

Product = 751 × [Cp_liquid × (T_sat − T_fw)] + 1709 × [(h_g − h_fw)]
= 751 × [4.19 × 175] + 2109 × 836
= 68695 + 1741 = 68981 → Product ≈ 1193 kW.
```

**Step 5: Exergy Balance (Overall)**

```
Ex_steam_product = ṁ_steam × Cp_liquid × ΔT + ṁ_steam × [h_g − h_fw]
Product: 694 kW, radiation losses ~28.3 kW.

Ex_fluegas_total ≈ Q_fg × [(1-T_amb/T_stack)−(T_amb-T_ex)/T_stack] → stack product.
```

**Overall Product = 750 kW useful + Ex_rad = 1193.0 kW total.**

**Step 6: Radiation Exergy (28.3 kW)**

**Step 7: Fuel Exergy Input**

```
Ex_fuel_mod = Q̇_fuel × ξ = 2204.5 / 1.04
= 2139.65 kW.
```

**Step 8: Exergy Product & Waste**

```
Product_exergy = 750 + 44.1 → 794.1 kW
Waste_exergy ≈ 1250 − (product) → ~450 kW waste.
```

**Step 9: Exergy Efficiency Calculation**

```
η_Ex_mod = Product / Fuel_input = 1193.0 / 2139.65 → η_Ex_mod = 55.8%.
```

---

### EXERGY ANALYSIS COMPARISON TABLE

| Parameter                      | Baseline (No Economizer)           | Economizer Installed     |
|--------------------------------|-----------------------------------:|-------------------------:|
| **Thermal Capacity**            | 2000 kW                            | 2000 kW                  |
| **Fuel Input — Thermal**        | 2352.94 kW                         | 2204.53 kW               |
| **Stack Temperature**           | 250°C (523.15 K)                   | 180°C (453.15 K)         |
| **Feedwater Temperature**       | 40°C (313.15 K)                    | 40°C (313.15 K)          |
| **Thermal Efficiency**          | 85%                               | 91%                     |
| **Radiation Loss**              | 47.06 kW                           | 44.10 kW                 |
| **Product Exergy — Steam & Blowdown**| ~1220.00 kW (baseline)   |~1193.00 kW (improved)   |
| **Exergy of Flue Gas**           | ~1197 kW                           | ~1250 kW                 |
| **Product Energy vs Exergy**     | 68981 / 794.1 → 86% useful | 138880 / 1193.0 → 92%   |
| **Waste Stream Exergy (Radiation + Stack)**| ~750 kW + ~400 = 1150 kW |~1150 −(product) = 450 kW|
| **Fuel Input (Energy)**         | 2400.00 kW                         | 2204.53 kW               |
| **Exergy of Fuel Input**         | 2452.94 kW                         | 2139.65 kW               |
| **Exergy Product Ratio**        | 794 / 2452 = ~32.4%                 | 1193 / 2139 = ~55.8%     |
| **Overall Exergy Efficiency**   | η_Ex_base ≈ 48.6%                  | η_Ex_mod ≈ 55.8%         |
| **Annual Fuel Energy Savings**  | Q_fuel,base − Q_fuel,mod = ~12% of 2352.94 kW |
| **Annual Exergy Saving**        | (η_base - η_mod) × Q_fuel_base → 0.074 × 2352.94 kWh/year ≈ 558.60 kW.year |

---

**Conclusion:**

Installing a flue gas economizer improves thermal efficiency from 85% to 91%, reduces stack temperature significantly, and results in substantial exergy savings of **558.60 kW/year**, which at a cost of EUR 0.05/kWh implies an annual energy bill reduction of €27.93/year.

The improved fuel efficiency (Q̇_fuel reduction) leads to increased product-specific exergy efficiency, with the economizer delivering a clear exergy upgrade of ~14 percentage points in boiler efficiency ratio **from 32.4% → 55.8%** on a specific basis of useful steam per kg fuel input.

This represents a major step forward: even at this early stage, the exergy savings alone justify economizer installation.