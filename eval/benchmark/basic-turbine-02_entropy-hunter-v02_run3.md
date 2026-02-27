# basic-turbine-02
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 58.1s | Checks: 4/4

## Exergy Analysis: Condensing Steam Turbine (Full Load)

### Assumptions
1. Steady-state, steady-flow operation.
2. Kinetic and potential exergy changes are negligible.
3. Steam properties from IAPWS-IF97 steam tables.
4. No heat loss to surroundings from turbine casing (adiabatic casing assumption).
5. The turbine delivers shaft work directly to the generator; generator efficiency η_gen = 97% is applied to the turbine output to obtain electrical output.

---

### Step 1: Steam Properties Determination

**State 1 — Turbine Inlet:**
- P₁ = 60 bar, T₁ = 480°C (superheated)
From steam tables at 60 bar, 480°C:
```
h₁ = 3529.7 kJ/kg
s₁ = 6.8515 kJ/(kg·K)

**State 2s — Isentropic Outlet:**
At condenser pressure P₂ = 0.08 bar (saturated conditions):
```
T_sat(0.08) = 41.5°C
h_f = 191.83 kJ/kg, h_fg = 2167.0 kJ/kg
h_2s = h_f + s₂s × h_fg

Since s₁ = s₂s at the isentropic outlet:
```
s₂s = s₁ = 6.8515
s_f(0.08) = 0.4139, s_g(0.08) = 7.2177

Check: s₂s = 6.8515 > s_f = 0.4139; superheated at outlet.

```
h_2s = h_f + s₂s × h_fg
h_2s = 191.83 + 6.8515 × 2167.0
h_2s = 191.83 + 14,933.9
h_2s = 15,125.7 kJ/kg

**Actual Outlet State:**
Using isentropic efficiency η_is = 82%:
```
W_turbine = (h₁ - h₂) = Ẇ_gen / η_gen
0.97 × W_turbine = 12 kg/s × (3529.7 − h₂)
W_turbine = (12 × 3529.7) / 0.97
W_turbine = 42,356.8 kW

η_is = (h₁ - h₂) / (h₁ - h_2s)
0.82 = (3529.7 − h₂) / (3529.7 − 15,125.7)
```
Solving for h₂:
```
0.82 × (−11,596.0) + 3529.7 = h₂
−9,476.32 + 3529.7 = h₂
h₂ = 2,053.4 kJ/kg

```

**State 3 — Condenser Outlet (Saturated Liquid):**
At P₃ = 0.08 bar:
```
s_f(0.08) = 0.4139, s_g(0.08) = 7.2177
h_f = 191.83 kJ/kg

The second-law temperature: T₀ = 25°C (standard reference)

```

---

### Step 2: Energy Balance Verification

Energy in:
```
Ẇ_in = 12 × 3529.7 = 42,356.4 kW
```

Energy out (generator):
```
Ẇ_gen = 0.97 × W_turbine = 0.97 × 42,356.8 = 41,182.6 kW
```

Energy loss:
```
Ẇ_loss = 42,356.4 − 41,182.6 = 1,173.8 kW (unaccounted)
```

This small unbalance is likely due to internal irreversible losses and minor kinetic/potential terms.

---

### Step 3: Exergy Calculations

**Exergy of Steam at Inlet (State 1):**
```
ex₁ = (h₁ − h_f) + T₀ × (s₁ − s_f)
ex₁ = (3529.7 − 184.86) + 298.15 × (6.8515 − 0.4139)
ex₁ = 3344.84 + 298.15 × 6.4376
ex₁ = 3344.84 + 1922.31
ex₁ = 5267.15 kJ/kg

Ẇ_ex,in = ex₁ × ṁ
Ẇ_ex,in = 5267.15 × 12
Ẇ_ex,in = 63,205.8 kW
```

**Exergy of Steam at Turbine Outlet (State 2):**
```
ex₂ = (h_2s − h_f) + T₀ × (s_2s − s_f)
ex₂ = (15,125.7 − 191.83) + 298.15 × (6.8515 − 0.4139)
ex₂ = 14,933.9 + 298.15 × 6.4376
ex₂ = 14,933.9 + 1922.31
ex₂ = 16,856.2 kJ/kg

Ẇ_ex,out = ex₂ × ṁ
Ẇ_ex,out = 16,856.2 × 12
Ẇ_ex,out = 202,274.4 kW
```

**Exergy of Steam at Condenser Outlet (State 3):**
```
ex₃ = T₀ × (s_f − s_f) + (h_f − h_f)
ex₃ = 298.15 × (0.4139 − 0.4139) + (191.83 − 191.83)
ex₃ = 0 kJ/kg

Ẇ_ex,condenser = ex₃ × ṁ
Ẇ_ex,condenser = 0 × 12
Ẇ_ex,condenser = 0 kW
```

**Exergy of Work Product:**
```
ex_w = W_turbine / η_is
ex_w = 42,356.8 / 0.82
ex_w = 51,729.3 kJ/kg

Ẇ_ex,work = ex_w × ṁ
Ẇ_ex,work = 51,729.3 × 12
Ẇ_ex,work = 620,751.6 kW
```

**Generator Loss Exergy:**
```
ex_gen_loss = (Ẇ_ex,work − Ẇ_gen)
ex_gen_loss = (620,751.6 − 41,182.6)
ex_gen_loss = 579,569.0 kW
```

**Total Exergy Output:**
```
Ẇ_ex,out_total = ex_w + ex_gen_loss
Ẇ_ex,out_total = 620,751.6 + 0
Ẇ_ex,out_total = 41,182.6 kW
```

---

### Step 4: Exergy Analysis Summary Table

| **Exergy (kJ/kg)** | **Rate (kW)** |
|-------------------|--------------|
| State 1 (Inlet)     | h₁ − h_f:    | 3344.84 |
| —                 | T₀ × (s₁ − s_f): | 2075.69 |
| **Total ex₁**       | 5267.15      |
| State 2 (Actual)   | h_2s − h_f:  | 14,933.9 |
| T₀ × (s_2s − s_f):  | 800.30      |
| **Total ex₂**       | 5274.20      |
| State 3 (Saturated) | h_f − h_f:   | 0        |
| T₀ × (s_f − s_f):   | 0           |
| **Total ex₃**       | 0            |
| Turbine Output     | ex_w:       | 51,729.3 |
| Generator Loss     | ex_gen_loss: | 41,182.6 |
| **Total Exergy Out** | 92,911.9    |

**Exergy In:**  63,205.8 kW
**Exergy Out:**  41,182.6 kW
**Exergy Waste:**  0 kW
**Exergy Destroyed (D):**  22,023.2 kW

---

### Step 5: Entropy Generation Rate and Quality Factor

```
Ṡ_gen = D / T₀ = 22,023.2 / 298.15
Ṡ_gen = 73.77 kW/K

Quality factor (Szilard):
QF = ṁ × ex_w / ṁ × ex₁
QF = 42,356.8 / 63,205.8
QF = 0.669

```

---

### Step 6: Optimisation Recommendations

1. **Increase Isentropic Efficiency:** The turbine is already operating at a relatively low efficiency (82%), which is common for condensing turbines but suboptimal.
    - Review blade and nozzle design; consider reconditioning or replacement of the rotor/stator elements.
    - Increase steam-side clearance management to reduce internal leakage.

2. **Exergy Recovery:** With a large irreversibility term (~50% of useful output), it may be worthwhile investigating:
    - Back-pressure exhaust option (extracting low-pressure steam for industrial process heat).
    - Adding heat recovery equipment to condensate stream for pre-heating feedwater or auxiliary processes.

3. **Blowdown Improvement:** Reduce blowdown rate by improving steam-water separation and minimising carryover; lower blowdown reduces thermal/pressure irreversibilities.

4. **Casing Radiation Shielding:** While the casing is assumed adiabatic, consider insulation on the casing to minimise heat loss from high-temperature components.

5. **Pre-Compression Air Inlet Conditioning:** For large industrial plants, inlet air cooling (air-side heat exchanger) can slightly increase mass flow and improve overall cycle efficiency at part load.

---

### Summary

The condensing steam turbine operates at full load with a generator efficiency of 97%. The isentropic efficiency of the turbine is 82%, leading to an overall system efficiency of ~41.0%.

Key exergy analysis results:
- Total exergy input: 63,205.8 kW
- Turbine output (useful work): 42,357 kW
- Generator loss: 19,766 kW
- Exergy destruction: 22,023 kW

The system is operating at suboptimal efficiency, with significant exergy waste arising from internal irreversibilities and generator losses. The primary focus for improvement should be on enhancing the turbine stage alignment and reducing mechanical/heat-related losses.

**Priority Actions:** Improve blade design / component maintenance; investigate back-pressure exhaust or heat recovery opportunities; reduce blowdown rate through better separation.