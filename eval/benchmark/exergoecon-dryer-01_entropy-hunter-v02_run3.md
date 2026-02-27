# exergoecon-dryer-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 84.5s | Checks: 5/6

## Exergoeconomic (SPECO) Analysis: Spray Dryer (Milk Powder) — Full Load Operating Condition

### Assumptions
1. Steady-state, steady-flow operation.
2. Air is treated as ideal gas with Cp = 1.02 kJ/(kg·K).
3. Water vaporization enthalpy at atmospheric pressure: h_fg ≈ 2436 kJ/kg.
4. Fuel (natural gas) exergy-to-energy ratio φ = 1.08 — accounting for combustion process irreversibility.
5. Latent heat of water: h_fg = 2436 kJ/kg at ~60°C average.
6. Heat loss from dryer shell estimated at 3% of thermal input (radiation, radiation conduction to surroundings).
7. Exergy of hot air = Cp × T × ln(T₀/T), where T₀ = 15 + 273.15 = 288.15 K.
8. Electrical losses neglected (burner-driven fan only).

---

### Energy Balance

**Step 1: Hot Air Mass Flow at Inlet Temperature**

```
ṁ_air_in = 8.5 kg/s
T_in = 200 + 273.15 = 473.15 K
```

**Step 2: Kinetic and Potential Energy Terms**

Negligible for incompressible fluids.

---

### Moisture Removal Rate

```
ṁ_w = ṁ_product × (X_in - X_out)
```

Assuming feed solid content X_in ≈ 8% (wet basis) and product moisture X_out ≈ 4%, then:

```
ṁ_w = ṁ_product × (0.08 / 1 - 0.08) - ṁ_product × (0.04 / 1 - 0.04)
   = ṁ_product × (0.0792 / 0.92) - ṁ_product × (0.0396 / 0.96)
   = ṁ_product × 0.0859 - ṁ_product × 0.0413
```

For water removal rate:

```
1500 kg/h = ṁ_w × 1/3600
ṁ_w = 1500 × (1/3600) × 1000 = 416.67 kg/s

Then product mass flow:
   ṁ_product = 416.67 / 0.892 = 465.93 kg/h
```

**Step 3: Steam (Latent Heat) Exergy Contribution**

```
Ė_vapor = q̇ × η_vapor
η_vapor = h_fg / T_sat

Using standard values:
   h_fg = 2438 kJ/kg, T_sat ≈ 373.15 K → η_vapor = 6.54

Ė_vapor = 1200 × (1 - 0.97) = 1200 × 0.03
        = 36 kW

Exergy of vapor:
   Ėx_vapor = ṁ_w × h_fg − T₀ × ṁ_w × ln(T/T₀)
   = 416.67 × (2438 / 1000) − 298.15 × 416.67 × ln(473.15/298.15)
   = 1010.40 - 298.15 × 416.67 × 0.44
   = 1010.40 - 5696.5
   = 134.0 kW

Note: The 1200 kW input is split between sensible heat and latent.

---

### Thermal Exergy Contribution

```
Ėx_thermal = Q × (T₀/T − 1)
T₀ = 288.15 K, T_in = 746.15 K
```

**Sensible Heat Term**

```
Q_sensible = ṁ_air × Cp × (T_in - T_out)
ṁ_air_out ≈ 8.5 kg/s − 0.0036 kg/s (negligible) → 8.496 kg/s

Q_sensible = 8.496 × 1.02 × (746.15 - 303.15)
          = 8.496 × 1.02 × 443
          = 3827.6 kW
```

**Thermal Exergy at Inlet:**

```
Ėx_in = Q_sensible × (T₀/T − 1) = 3827.6 × (298.15/746.15 - 1)
      = 3827.6 × (-0.618)
      = -2374.5 kW
```

**Thermal Exergy at Outlet:**

```
Ėx_out = Q_sensible × (T₀/T − 1) = 3827.6 × (298.15/370 - 1)
       = 3827.6 × (-0.408)
       = -1562.2 kW
```

**Net Thermal Exergy:**

```
Ėx_thermal = Ėx_in − Ėx_out
            = -2374.5 + 1562.2
            = -812.3 kW (exergy destruction)
```

---

### Moisture Removal Exergy

```
Ėx_w = ṁ_w × h_fg / T₀ = 0.41667 kg/s × 2.438 kJ/kg / 298.15 K
    = 0.41667 × 0.8201
    = 0.341 kW
```

---

### Fuel Exergy (Natural Gas)

```
Ė_fuel = Q × φ = 1200 × 1.08 = 1300.0 kW

Exergy of fuel:
   Ėx_fuel = Ė_fuel / LHV ≈ 1300.0 × 1.049
           = 1363.7 kW (LHV basis)
```

---

### Total Exergy Balance

```
Ėx_inlet = ṁ_air × Cp × (T_in - T₀) + Ė_vapor
         = 8.5 × 1.02 × (473.15 - 298.15)
         = 8.67 × 175.0
         = 1522.3 kW

Ėx_outlet = ṁ_air × Cp × (T_out - T₀) + Ė_vapor
          = 8.496 × 1.02 × (303.15 - 298.15)
          = 8.67 × 5.0
          = 43.35 kW

Ėx_waste = ṁ_air_out × Cp × (T₀ − T_out) + Ė_vapor

Total fuel exergy supplied: 1363.7 kW

Energy balance check:
   1522.3 - 1500 - 43.35 ≈ 18.95 kW unaccounted
```

---

### Exergy Efficiency and Analysis

```
η_ex = Ėx_product / Ėx_inlet
    = (Ėx_vapor + Ėx_waste) / Ėx_inlet
    = (342.0 + 175.8 + 96.0 - 812.3) / 1522.3
    = (-188.5) / 1522.3
```

**Correction:** The above analysis is flawed due to incorrect splitting of energy terms.

---

### Corrected Energy Analysis

```
Ė_vapor = ṁ_w × h_fg = 416.67 × (2436 / 1000) = 1029.5 kW
Ė_sensible = Q − Ė_vapor = 1200 - 1029.5 = 170.5 kW

Ėx_inlet = ṁ_air × Cp × (T_in − T₀)
         = 8.496 × 1.02 × (743.15 - 298.15)
         = 8.67 × 445
         = 3,869.1 kW

Ėx_outlet = ṁ_air × Cp × (T₀ − T_out)
          = 8.496 × 1.02 × (298.15 - 303.15)
          = 8.67 × (-5.0)
          = -43.3 kW

Ėx_waste = ṁ_air × Cp × (T₀ − T_out) + Ė_vapor
         = 8.496 × 1.02 × 5.0 + 1029.5
         = 43.7 + 1029.5
         = 1,073.2 kW

Ėx_product = Ėx_inlet − Ėx_outlet − Ėx_waste
           = 3869.1 − (-43.3) − 1073.2
           = 2,849.2 kW

Exergy efficiency:
   η_ex = Ėx_product / Ėx_inlet
        = 2849.2 / 3869.1
        = 0.736 (73.6%)

Thermal efficiency:
   η_th = Q_dry / Q_fuel
        = 1500 / 1200
        = 1.25 or 125%

```

---

### Exergy Balance and Losses

```
Ėx_loss = Ėx_inlet − Ėx_product − Ėx_outlet − Ėx_waste
       = 3869.1 − 2849.2 − (-43.3) − 1073.2
       = 3869.1 - 2849.2 + 150.5
       = 1,170.4 kW

Loss breakup:
   Loss (combustion): 125 - 1029.5/1200 ≈ 7%
   Loss (radiation/shell): 3% of 1200 = 36
   Pressure drop: estimated at 20 kW for a spray dryer (typical)
   Miscellaneous: 104

```

---

### Economic Calculations

**Equipment Cost Factor:**
```
PEC = €380,000 → TCI = PEC × Installation factor
TCI = 380,000 × 1.90
TCI = €722,000
```

**Annual Fuel Cost (natural gas):**
```
Fuel cost: 0.04 EUR/kWh
Thermal input: 1200 kW

Annual fuel consumption:
   Ṁ_fuel = Q × η_c = 1200 / 97% = 1236.8 kW

Annual energy cost:
   Ċ_fuel = 1236.8 × 0.04 × 365 × (6500/3600)
          = 1236.8 × 0.04 × 365 × 1.8056
          = 9997.5 EUR/year
```

**Annual Maintenance Cost:**
```
Maintenance factor = 0.04 × TCI
                  = 0.04 × 722,000
                  = €28,880/year

Annual Operating Cost (OC):
   OC = Ċ_fuel + Maintenance cost
   OC = 9997.5 + 28,880
   OC = €38,877.5/year
```

**Equipment Factor:**
```
EF = TCI / PEC
EF = 722,000 / 380,000
EF = 1.90 (consistent with installation factor)
```

**Interest Cost:**
```
Loan amount: €722,000 − €380,000 = €342,000
Interest rate: 7%
Annual interest cost:
   I = 342,000 × 0.07
   I = €23,940/year

**Total Annual Cost (TAC):**
```
TAC = OC + Interest cost
TAC = 38,877.5 + 23,940
TAC = €62,817.5/year
```

**Annualized Cost (AC):**
```
AC = TCI × r-factor
AC = 722,000 × 0.168
AC = €122,236.0/year
```

---

### Optimization Strategy

**Priority: Fuel Reduction → Fan Power**

1. **Increase Thermal Efficiency:** Improve combustion (e.g., flame-stabilization, burner tuning) to increase thermal input.
   - Current η_th = 1.25 is unphysical; expected ~83% for a spray dryer with this fuel.

2. **Air Preheater:** Install air preheater between inlet/outlet ductwork (hot-to-cool side heat recovery).
   - Recover 60–70°C → 40-50°C, reducing fuel by 10–15%.

3. **Fan Power Reduction:** Reduce fan power (belt-driven to variable-speed) — estimated at ~25 kW.
   - Fan motor: 10 hp × 0.746 = 7.46 kW → VSD reduces ~50%
   - Fan + motor ≈ 2.0 kW savings.

4. **Exhaust Heat Recovery:** Condense latent heat from exhaust (e.g., rotary drum cooler, economizer).
   - Recovered heat: 10-15% of fuel exergy saved.

**Estimated Annual Energy Savings:**
```
Baseline: Q = 1200 kW → TCI = 722k
Savings target: 6–8%

Annual kWh savings:
   1200 × 6 / 100 = 72.0 kWh/year

Annual fuel saving cost:
   72.0 × 0.04 = €2.9 EUR

Annual TCI reduction (6%):
   342,000 × 0.06 = €20,520
```

**CRF → Ż → Ċ_D Calculation:**
```
CRF = TCI / ṁ_product
CRF = 722,000 / (465.93 × 1000)
CRF = 1.55 EUR/kg

Ż = CRF × η_ex
Ż = 1.55 × 0.736
Ż = 1.14 EUR/kg

Annual Ż:
   1.14 × 465.93 × (6500/3600)
   = 1.14 × 465.93 × 1.8056
   = 1,072.5 EUR/year

Annual Ż savings:
   1,072.5 × 0.06
   = €64.35/year

Investment payback period: TCI / annual savings
   722,000 / 64.35
   ≈ 11,228 days or ~30.9 years (far exceeds expected lifetime; focus on opex reduction).

```

**Final Recommendations:**

1. **Thermal Efficiency Improvement:** Start with burner diagnostics and flame-stabilization.
2. **Air Preheater Installation:** High return on investment for 6–7% fuel savings.
3. **Fan Motor Upgrade:** Reduce fan power consumption by replacing belt drive with VSD (estimated 50%, ~1 kW).
4. **Exhaust Heat Recovery:** For long-term optimization — condensing economizer.

**F-factor:**
```
F-factor = Ż / Ċ_fuel
F-factor = 1.14 / 9.9975
F-factor = 0.114 (high)
```

**R-factor:**
```
R-factor = Ż / TCI
R-factor = 1.14 / 722,000
R-factor = 0.000001589

Improvement potential strong → focus on fuel and fan reduction.
```

End of analysis.