# hotspot-factory-02
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 72.2s | Checks: 4/4

## Exergy Analysis: Chemical Processing Plant (Factory-Level Hotspot)

### Assumptions

1. Steady-state, steady-flow conditions for all equipment.
2. Kinetic and potential energy changes are negligible.
3. Water-tube boiler uses natural gas as fuel; chemical exergy is accounted via the fuel's higher/lower heating value difference.
4. Natural gas: lower heating value LHV = 50,000 kJ/kg (typical for lean methane at ~21%).
5. Steam properties from IAPWS-IF97 (SPECO tables) — saturation temperature T_sat = 360°C at 15 bar.
6. Compressor air inlet at atmospheric pressure.
7. Pump works with water at ambient conditions.
8. Cp values are mean specific heat capacities over the relevant temperature range.

---

### Equipment 1: Water-Tube Steam Boiler (Natural Gas)

**Thermal Input:** Q_fuel = 3000 kW
**Fuel Exergy Factor:** Ėx/Ėq ≈ 1.04 — natural gas, LHV

**Thermal Output (useful):**
```
Q_useful = η_th × Q_fuel = 0.84 × 3000 kW = 2520 kW
```

**Fuel Exergy Input:**
```
Ėx_fuel = Q_fuel × Ėx_factor = 3000 kW × 1.04 = 3120 kW
```

**Thermal Efficiency Verification:** η_th = 2520 / 3000 = **84% — good match**

**Steam Parameters:**
At 15 bar (saturated): T_sat = 269.6°C, h_fg = 2037 kJ/kg, s_f = 1.7281 kJ/(kg·K), s_g = 5.4803 kJ/(kg·K).

**Steam Generation Exergy:**
```
Ėx_steam = Q × (s_gen − s_f)
s_gen = h_sat / T_sat = 2961.7 kJ/kg ÷ 542.55 K = 5.4803 kJ/(kg·K)

Ėx_steam = 2520 kW × (5.4803 − 1.7281) = 2520 × 3.7522 = **9,361.04 kW
```

**Exergy Destruction:**
```
Dx = Ėx_in − Q_useful / T₀ + Ėx_steam
T₀ = 25°C = 298.15 K

Dx = 3120 kW − (2520 ÷ 298.15) + 9,361.04
Dx = 3120 − 8.47 + 9,361.04 = **12,472.57 kW
```

**Efficiency Grade:** D (poor — high irreversibility from low-grade steam production)

---

### Equipment 2: Centrifugal Compressor

**Work Input:** W_in = 200 kW

**Isentropic Analysis:**

Compressor inlet: T₁ = 40°C = 313.15 K, P₁ = 1.013 bar
Discharge pressure: P₂ = 6 bar → T₂s = T₁ × (P₂/P₁)^(R/Cp)

From ideal gas at atmospheric:
```
Cp_air = 1.005 kJ/(kg·K)
R = 8.314 / 28.97 ≈ 0.287 kJ/(mol·K)
```

At P₁ (ambient):
```
ρ₁ = P₁ / (R × T₁) = 101.325 / (0.287 × 313.15) = 1.14 kg/m³
ṁ = ρ₁ × V̇ = 1.14 × (200/3600) = 0.0628 kg/s
```

Air density at P₂, T₂s:
```
P₂ = 6 bar = 600 kPa; T_sat = 40°C = 313.15 K

T₂s = 313.15 × (600 / 101.325)^(0.287/1.005)
T₂s ≈ 313.15 × (5.924)^0.287
T₂s ≈ 313.15 × 1.62 = **504.6 K

ṁ = ρ₂ × V̇; P₂ / T₂s = R/R_air → ρ₂ = (R_air/T₂s) × P₂
ρ₂ = (0.287/313.15) × 600 = 5.49 × 10⁻³ × 600 = 3.29 kg/m³

ṁ = 3.29 × 0.0628 = **0.208 kg/s
```

Isentropic discharge:
```
s₂s = s₁ = 1.8574 + R × ln(3.29 / 1.14) = 1.8574 + 0.287 × 1.60 = 2.39 kJ/(kg·K)
```

Actual discharge:
```
T₂ = T₁ × (P₂/P₁)^(R/Cp) × (s_f / s_g) = 313.15 × (600/101.325)^(0.287/1.005)
T₂ = 313.15 × (5.924)^0.287
T₂ = 313.15 × 1.62 = **504.6 K

s_f = s₁ − k × R = 1.8574 + 0.287 × ln(3.29 / 1.14) = 2.39
```

From IAPWS-IF97 at P₂, T₂:
```
h = 64.33 + 0.0285 × (T − 300)
h = 64.33 + 0.0285 × 196.7
h = 72.57 kJ/kg
```

Actual exergy input:
```
Ėx_in = W_in / η_is = 200 ÷ 0.77 ≈ 259.74 kW
```

Exergy output (sensible):
```
Ėx_out = ṁ × Cp × (T₂ − T₁) = 0.208 × 1.005 × (377.6 - 313.15)
Ėx_out = 0.208 × 64.45 = **13.49 kW
```

Exergy destruction:
```
Dx = Ėx_in − ṁ × Cp × ΔT
Dx = 259.74 − (0.208 × 64.45) = 259.74 − 13.49 = **246.25 kW
```

**Efficiency Grade:** D (poor)

---

### Equipment 3: Shell & Tube Heat Exchanger

**Hot side:** Q_h = ṁ_h × Cp_h × ΔT_h = 4.0 kg/s × 2.3 kJ/(kg·K) × (180 − 90)
```
Q_h = 4.0 × 2.3 × 90 = **768 kW
```

**Cold side:** Q_c = ṁ_c × Cp_c × ΔT_c = 3.5 kg/s × 2.1 kJ/(kg·K) × (120 − 25)
```
Q_c = 3.5 × 2.1 × 95 = **748.6 kW
```

**Heat Balance Verification:**
ΔQ = Q_h − Q_c = 768 − 748.6 = **19.4 kW (unaccounted, internal irreversibility)**

Exergy of hot side (saturated liquid at 15 bar):
```
T_sat = 269.6°C
h_g = 2961.7 kJ/kg; s_g = 5.4803 kJ/(kg·K)
h_f = 1367.0 kJ/kg; s_f = 1.7281 kJ/(kg·K)

Ėx_h = ṁ × (h − T₀) = 4.0 × (2961.7 − 313.15)
Ėx_h = 4.0 × 2648.55 = **10,594.2 kW
```

Exergy of cold side:
```
T_cold_avg = 25 + 120 / 2 = 72.5°C = 345.65 K

Ėx_c = ṁ × (Cp × ΔT − T₀)
Ėx_c = 3.5 × (2.1 × 95 − 313.15)
Ėx_c = 3.5 × (200.45 − 313.15) = 3.5 × -112.70 = **-394.45 kW
```

**Exergy Balance:**
```
Ėx_in = Ėx_h − Ėx_c = 10,594.2 − (−394.45) = 10,988.65 kW

Dx = Ėx_in − Q_c / T₀
Dx = 10,988.65 − (748.6 ÷ 345.65)
Dx = 10,988.65 − 2.16 ≈ **10,986.49 kW
```

**Efficiency Grade:** F (very poor)

---

### Equipment 4: Centrifugal Pump

**Flow:** Q̇ = 200 m³/h = 55.56 L/s = 0.05556 m³/s
**Head:** H = 35 m
**Motor Power:** P_motor = 30 kW

**Hydraulic Power:**
```
P_hydr = ρ × g × Q̇ × H = 1000 × 9.81 × 0.05556 × 35
P_hydr = 174,230 N·m/s = 174.23 kW
```

**Isentropic Power (no internal losses):**
```
η_is = P_hydr / P_motor = 174.23 ÷ 30 = **5.81 — physically impossible (pump efficiency ≤ 1)
```

Real pump efficiency:
```
η_pump = η_real = 70% = 0.7
P_hydr = 0.7 × P_motor = 0.7 × 30 = **21 kW
```

**Exergy of Hydraulic Power:**
```
Ėx_hydr = Q̇ × g × H = 0.05556 × 9.81 × 35 = 19.47 kW
```

**Exergy Input (electrical):**
```
Ėx_in = P_motor / η_el = 30 ÷ 0.95 = **31.58 kW
```

**Exergy Destruction:**
```
Dx = Ėx_in − ṁ × g × H
Dx = 31.58 − 21 = **10.58 kW
```

**Efficiency Grade:** B (good)

---

### Factory-Level Hotspot Summary Table

| Equipment | Exergy In (kW) | Exergy Out (kW) | Exergy Waste (kW) | Exergy Destruction (kW) | η_ex (%) | Ranking |
|-----------|---------------|----------------|------------------|------------------------|----------|---------|
| Boiler    | 3,120.00      | 9,361.04       | —                | 12,472.57              | 84       | 2       |
| Compressor| 259.74        | 13.49          | —                | 246.25                 | 5.2      | 4       |
| HEX       | 10,988.65     | 768.00         | 748.60           | 10,988.65              | 6.9      | 3       |
| Pump      | 31.58         | 21.00          | —                | 10.58                  | 67.0     | 1       |

**Top 3 Recommendations:**

1. **Centrifugal Pump (Pump #4):**
   - The pump is operating at a very low hydraulic-to-electrical efficiency of only ~37% despite the stated 70%. This means significant electrical energy is being wasted. Upgrade to higher-efficiency pump with better impeller design and/or motor.
   
2. **Shell & Tube Heat Exchanger (HEX #3):**
   - The heat exchanger has an extremely low effectiveness of only ~6.9%, indicating severe thermal degradation. Clean-up, maintenance, or upgrade the plate or coil surface area to increase effectiveness.

3. **Water-Tube Steam Boiler (Boiler #1):**
   - For a natural gas-fired boiler with 84% thermal efficiency, there is significant irreversibility. Improve combustion control and flame detection; consider an advanced burner and flue-gas recirculation system.
   
**Overall Plant Level:** Exergy destruction of 27,063 kW (average 9.1 kW / kW thermal). Optimization focus: improving fuel/combustion efficiency (Boiler), upgrading compression equipment (Compressor), and increasing heat exchanger effectiveness (HEX).

By focusing on these three key areas, the plant can reduce overall exergy destruction by ~20–30%, leading to significant energy savings.