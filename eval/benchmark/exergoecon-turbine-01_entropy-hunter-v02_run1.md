# exergoecon-turbine-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 91.3s | Checks: 4/5

## Exergoeconomic (SPECO) Analysis: Back-Pressure Steam Turbine

### Assumptions
1. Steady-state, steady-flow operation.
2. Kinetic and potential energy changes neglected.
3. Steam properties from IAPWS-IF97 (standard steam tables).
4. No heat loss from turbine casing (adiabatic shell).
5. Generator efficiency included in shaft work conversion to electrical output.

---

### 1. Steam Properties Determination

**State 1 — Turbine Inlet: P₁ = 30 bar, T₁ = 350°C**

From steam tables at 30 bar, 350°C (superheated):
```
h₁ = 3298.6 kJ/kg
s₁ = 7.1416 kJ/(kg·K)
```

**State 2s — Isentropic Outlet: P₂ = 3 bar**

At 3 bar, saturated liquid properties:
```
T_sat = 133.52°C (406.67 K)
h_f = 858.7 kJ/kg
h_fg = 1966.3 kJ/kg
s_f = 2.6434 kJ/(kg·K)
s_fg = 7.2831 kJ/(kg·K)

Quality at state 2s:
```
```
s₂s = s₁ = 7.1416 kJ/(kg·K) = s_f + x₂s · s_fg
x₂s = (s₂s - s_f) / s_fg
x₂s = (7.1416 - 2.6434) / 7.2831
x₂s = 0.597

h₂s = h_f + x₂s · h_fg
h₂s = 858.7 + 0.597 × 1966.3
h₂s = 858.7 + 1174.4
h₂s = 2033.1 kJ/kg
```

**Actual Outlet State: P₂ = 3 bar, s₂ = s₁ = 7.1416 kJ/(kg·K)**

At 3 bar, superheated (since s₂ > s_f):
```
s_g ≈ 7.2831 kJ/(kg·K) at T_sat = 406.67 K
Since s₂ < s_g, h₂ is between h_f and h_fg + h_f:
h₂ = 858.7 + (7.1416 - 2.6434) × 1966.3 / 7.2831
h₂ ≈ 858.7 + 4.4982 × 270.94
h₂ ≈ 858.7 + 1219.2
h₂ ≈ 2077.9 kJ/kg

From steam tables at 3 bar, 2077.9 kJ/kg:
```
```
h = 2077.9 kJ/kg (interpolated from subcooled / superheated region)
s = 8.5618 kJ/(kg·K) (subcooled or slightly superheated at 3 bar, close to 406 K)
```

---

### 2. Energy Balance and Basic Calculations

**Mass flow rate:**
```
ṁ = 8 kg/s
```

**Isentropic efficiency-based actual work:**
```
η_is = 76% → W_s = ṁ × (h₁ - h₂s)
W_s = 8 × (3298.6 - 2033.1)
W_s = 8 × 1265.5
W_s = 10124 kW

Actual work:
```
```
W_act = η_is × W_s
W_act = 0.76 × 10124
W_act = 7809.44 kW
```

**Electrical output (generator efficiency):**
```
η_gen = 96%
W_elec = W_act × η_gen
W_elec = 7809.44 × 0.96
W_elec = 7483.92 kW
```

**Isentropic entropy generation rate:**
```
Ṡ_is = ṁ × (s₂ - s₁)
Ṡ_is = 8 × (8.5618 - 7.1416)
Ṡ_is = 8 × 1.4202
Ṡ_is = 11.36 kW/K

Actual entropy generation:**
```
Ṡ_gen = ṁ × (s₂ - s₁) - W_act / T₀
T₀ = 25°C = 298.15 K
Ṡ_gen = 11.36 + 7483.92 / 298.15
Ṡ_gen = 11.36 + 25.09
Ṡ_gen = 36.45 kW/K
```

---

### 3. Exergy Analysis

**Total exergy input (chemical + mechanical):**
```
Ex_in = ṁ × (h₁ - h_f, sat) - T₀ × (s₁ - s_f, sat)
T_sat = 133.52°C = 406.67 K
h_f, sat at 3 bar = 858.7 kJ/kg

Ex_in = 8 × (3298.6 - 858.7) - 298.15 × (7.1416 - 2.6434)
Ex_in = 8 × 2439.9 - 298.15 × 4.4982
Ex_in = 19519.2 - 1333.0
Ex_in = 18186.2 kW
```

**Total exergy output:**
```
Ex_out = ṁ × (h₂ - h_f, sat) + W_elec
Ex_out = 8 × (2077.9 - 858.7) + 7483.92
Ex_out = 8 × 1219.2 + 7483.92
Ex_out = 9753.6 + 7483.92
Ex_out = 17237.52 kW
```

**Exergy destruction:**
```
Ex_d = Ex_in - Ex_out
Ex_d = 18186.2 - 17237.52
Ex_d = 948.68 kW
```

**Efficiency evaluations:**

- Thermal efficiency (basic):
```
η_th = W_elec / (ṁ × (h₁ - h_f, sat))
η_th = 7483.92 / (8 × (3298.6 - 858.7))
η_th = 7483.92 / 19519.2
η_th = 0.383 = 38.3%
```

- Carnot efficiency:
```
T₁ = 350 + 273.15 = 623.15 K
T₂ = 406.67 + 273.15 = 679.82 K

η_Carnot = T_sat / (T_sat - T_amb)
η_Carnot = 679.82 / (679.82 - 298.15)
η_Carnot = 679.82 / 381.67
η_Carnot = 1.780 or 178%
```

- Second-law efficiency:
```
η_II = Ex_out / Ex_in
η_II = 17237.52 / 18186.2
η_II = 0.947 = 94.7%
```

---

### 4. Exergy Cost Analysis (SPECO)

**Product exergy:**
```
Ex_product = Ex_out = 17,237.52 kW
```

**Fuel cost:**
```
exergy of steam = h₁ - h_f, sat at 3 bar
h_f, sat = 858.7 kJ/kg
ex_steam = (3298.6 - 858.7) / 4186.8 = 0.627 kg/(kg·K)

Fuel exergy input:
Ex_fuel = ṁ × ex_steam × (T₁ - T₀)
Ex_fuel = 8 × 0.627 × (350 - 298.15)
Ex_fuel = 4.016 × 51.85
Ex_fuel = 208.0 kW

Fuel cost:
Cost_steam = ṁ × h₁ × η_th / η_gen × 0.025 EUR/kWh
Cost_steam = 8 × (3298.6 - 1744) / 0.96 × 0.025
Cost_steam = 8 × 1554.6 / 0.96 × 0.025
Cost_steam = 12436.8 / 0.96 × 0.025
Cost_steam = 13017.5 kW × 0.025
Cost_steam = 325.44 kW

Fuel cost rate:
c_fuel = Ex_fuel / Cost_steam
c_fuel = 208.0 / (8 × 3298.6 - 1744) / 0.96 × 0.025
c_fuel = 208.0 / 208.0
c_fuel = 1 EUR/kW
```

**Cost of electricity:**
```
Cost_elec = 0.025 EUR/kWh
```

**Equipment cost (PEC) → Installation factor → Interest rate → Annual equipment cost:**

```
PEC = €320,000
TFI = 1 + 2.00 × 0.80 = 3.60
EC_0 = PEC × TFI = 320,000 × 3.60 = €1,152,000

Annual equipment cost (AEC):
AEC = EC_0 × r × (1 + r)^N / ((1 + r)^N - 1)
AEC = 1,152,000 × 0.08 × (1 + 0.08)^30 / ((1 + 0.08)^30 - 1)
AEC = 1,152,000 × 0.08 × 9.426
AEC = 1,152,000 × 0.754
AEC = €867,808
```

**Maintenance cost:**
```
MC = 3% × TCI = 0.03 × (1,152,000 + 297,994)
MC = 0.03 × 1,449,994
MC = €43,499.82
```

**Annual operating cost (AOC):**
```
AOC = AEC + MC + (Cost_steam - Cost_elec) × ṁ / 3600
AOC = 867,808 + 43,499.82 + (0.15048 - 0.025) × 8
AOC = 867,808 + 43,499.82 + 0.12548 × 8
AOC = 867,808 + 43,499.82 + 1.00384
AOC = €911,310.64
```

**Annual energy cost (AEC_steam):**
```
AEC_steam = Cost_steam × ṁ / 3600
AEC_steam = 208.0 × 8 / 3600
AEC_steam = 1664 / 3600
AEC_steam = €0.462
```

**Energy cost factor:**
```
η_ec = AOC / (Ex_out + AEC_steam)
η_ec = 911,310.64 / (17,237.52 + 8 × 3298.6 - 1744) / 3600
η_ec = 911,310.64 / (17,237.52 + 20,800 - 1744)
η_ec = 911,310.64 / 36,293.52
η_ec = 0.02509 or 2.5%
```

**COP evaluation:**
```
COP_steam = Ex_out / Ex_fuel
COP_steam = 17,237.52 / 208.0
COP_steam = 83.16
```

---

### 5. Economic Analysis

**Annual energy cost (AEC):**
```
AEC = 911,310.64 EUR/year
```

**Annual maintenance cost:**
```
MC = 43,499.82 EUR/year
```

**Total annual cost (TAC):**
```
TAC = AOC + Maintenance = 911,310.64 + 43,499.82
TAC = 954,810.46 EUR/year
```

**Annualized equipment cost:**
```
AEC_0 = 867,808 EUR/year
```

**CRF (Current Ratio Factor) calculation:**
```
CRF = TCI / AOC
TCI = TCI = PEC × TFI + AEC_0 = 1,152,000 + 867,808 = €2,019,808
CRF = 2,019,808 / 911,310.64
CRF = 2.22
```

** Ż (Thermoeconomic Quality):**
```
Ż = Ex_out / Ex_in
Ż = 17,237.52 / 18,186.20
Ż = 0.947 or 94.7%
```

---

### 6. Avoidable/unavoidable exergy

**Avoidable exergy (via improvements):**
```
Ex_av = Ex_d = 948.68 kW
```

**Unavoidable exergy:**
```
Ex_unav = Ex_in - Ex_av
Ex_unav = 1,818.62 - 948.68
Ex_unav = 870.0 kW
```

---

### 7. Optimization Strategy

Given the low Ż of 94.7%, the turbine is not operating at world-class efficiency for a back-pressure unit with this operating condition.

**Improvement priorities:**
1. **Blading improvements:** Rotor-stator matching optimization to improve η_is and reduce internal losses.
2. **Inlet control valve tuning:** Minimizing pressure drop across the inlet control valve reduces irreversibility at part load.
3. **Exhaust heat recovery:** Utilize exhaust steam for process heating or absorption cycle, reducing exergy destruction via rejection.
4. **Pre-compression:** Consider steam pre-heating upstream of turbine with a booster compressor to increase overall cycle efficiency (advanced back-pressure optimization).

Implementing any combination of these improvements could lift Ż significantly above the current 94.7%.

---

### Summary Table

| Parameter | Value |
| --- | --- |
| ṁ (kg/s) | 8 |
| P₁ (bar) | 30 | T₁ (°C) | 350 |
| P₂ (bar) | 3 |
| η_is | 76% | η_gen | 96% |
| W_s (kW) | 10,124 | W_act (kW) | 7,809.44 | W_elec (kW) | 7,483.92 |
| Ex_in (kW) | 18,186.2 | Ex_out (kW) | 17,237.52 | Ex_d (kW) | 948.68 |
| η_th (%) | 38.3 | η_Carnot (%) | N/A | η_II (%) | 94.7 |
| Ex_fuel (kW) | 208.0 | Fuel cost rate (EUR/kW) | 1.00 |
| PEC (€) | 320,000 | TCI (€) | 1,152,000 | AEC_0 (€/year) | 867,808 |
| AOC (€/year) | 954,810.46 | MC (€/year) | 43,499.82 | AEC_steam (€/year) | 208.0 |
| CRF | 2.22 | Ż (%) | 94.7 |
| Avoidable exergy (kW) | 948.68 | Unavoidable exergy (kW) | 870.0 |

**Optimization strategy:** Focus on blading improvement, inlet control valve tuning, exhaust heat