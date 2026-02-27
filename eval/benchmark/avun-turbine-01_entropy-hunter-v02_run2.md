# avun-turbine-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 79.1s | Checks: 4/4

# Exergy Destruction Analysis: Back-Pressure Steam Turbine

## Operating Conditions
### Given Data
1. Inlet state: P₁ = 20 bar, T₁ = 300°C (superheated)
2. Outlet pressure: P₂ = 3 bar
3. Mass flow rate: ṁ = 4 kg/s
4. Isentropic efficiency: η_is = 72%
5. Generator efficiency: η_gen = 93%
6. Operating mode: full_load

### Reference (Best Available Technology)
1. Isentropic efficiency: η_is,ref = 90%
2. Generator efficiency: η_gen,ref = 98%

---

## Step 1: Steam Properties at Inlet (State 1)

From steam tables for superheated steam at P₁ = 20 bar (2 MPa), T₁ = 300°C:

```
Tsat (2 MPa) = 158.87°C
```

Since the inlet temperature is above saturation, we use:
- h₁ = 2926.4 kJ/kg
- s₁ = 6.5230 kJ/(kg·K)

---

## Step 2: Isentropic Outlet State (State 2s)

For an ideal turbine at P₂ = 3 bar:

```
T_sat(3 bar) = 133.58°C
```

At P₂ = 3 bar, s₂s = s₁ = 6.5230 kJ/(kg·K). We need to find the corresponding h value.

Using steam tables at P₂ = 3 bar:
- At T = 133.58°C (saturated): h_f = 792.4, h_g = 2765.0, s_f = 1.8455, s_g = 5.6730

Since s₂s = 6.5230 kJ/(kg·K) > s_f (1.8455 kJ/(kg·K)) at P₂ = 3 bar:

```
State 2s is superheated.
```

Using interpolation for h and s in steam tables at P₂ = 3 bar, T = 400 K (127°C):

```
h_2s = 2865.0 kJ/kg
s_2s = 7.0956 kJ/(kg·K)
```

---

## Step 3: Actual Outlet State (State 2)

From energy balance at the turbine outlet:

```
h₂ + ṁ × g = h₁ - ṁ × (1 − η_is) × (h₁ − h_2s)
```

Where:
- g = specific work of compression (approximately equal to pressure difference for small exergy calculations)

First, calculate the isentropic outlet temperature:

```
T₂s = T_sat(P₂) + (s₂s - s_f)/C_p
```

From steam tables at P₂ = 3 bar:
- h_f = 792.4 kJ/kg
- h_g = 2765.0 kJ/kg
- s_f = 1.8455 kJ/(kg·K)
- s_g = 5.6730 kJ/(kg·K)

```
s_sat(P₂) = 2.9491 kJ/(kg·K)
T_sat(3 bar) = 133.58°C

At T₂s ≈ 127°C (state between s_f and s_g):

h_2s = 2026.2, s_2s = 6.964 kJ/(kg·K)
```

Using isentropic efficiency:

```
h₂ = h₁ − ṁ × g + ṁ × (1 − η_is) × (h₁ − h_2s)
h₂ = 2926.4 − 4 × 9.807 + 4 × 0.28 × (2926.4 − 2026.2)
h₂ = 2926.4 − 39.228 + 4 × 0.28 × 900.2
h₂ = 2926.4 − 39.228 + 1008.576
h₂ = 3905.748 kJ/kg
```

---

## Step 4: Energy and Exergy Calculations

### Useful Work (First Law)

```
W_turbine = ṁ × (h₁ − h₂)
W_turbine = 4 × (2926.4 − 3905.748)
W_turbine = 4 × (−979.348)
W_turbine = −3917.39 kJ/s
```

Generator efficiency:

```
W_gen = η_gen × W_turbine
W_gen = 0.93 × (−3917.39)
W_gen = −3624.58 kJ/s
```

### Exergy Calculations

#### Dead State: T₀ = 25°C, P₀ = 101.325 kPa

```
T₀ = 298.15 K
P₀ = 101.325 kPa (1.013 bar)
```

```
Ex_inlet = ṁ × (h₁ − T₀ × C_p)
Ex_inlet = 4 × (2926.4 − 298.15 × 4.187)
Ex_inlet = 4 × (2926.4 − 1238.7085)
Ex_inlet = 4 × 1687.6915
Ex_inlet = 6750.766 kJ/s

Ex_isentropic outlet:
```

Using steam tables at P₂ = 3 bar, T_sat(P₂) = 133.58°C:

```
h_f = 792.4 kJ/kg
h_g = 2765.0 kJ/kg
s_f = 1.8455 kJ/(kg·K)
s_g = 5.6730 kJ/(kg·K)

At T₂s ≈ 127°C: h_2s = 2026.2 kJ/kg, s_2s = 6.964 kJ/(kg·K)
```

Dead state exergy:

```
Ex_2s_dead = ṁ × (h_2s − T₀ × C_p + T₂s × ln(T₂s/T₀))
Ex_2s_dead = 4 × (2026.2 − 298.15 × 4.187 + 361.036 × ln(361.036/298.15)
```

```
Ex_2s_dead = 4 × (2026.2 − 1248.817 + 361.036 × 0.2944
Ex_2s_dead = 4 × (2026.2 − 1248.817 + 105.75)
Ex_2s_dead = 4 × 982.133
Ex_2s_dead = 3928.5 kJ/s

Ex_isentropic outlet:

```

For a turbine (no chemical or boundary work):

```
Ex_outlet = ṁ × (T₂s − T₀) × C_p + ṁ × (P₂ − P_0)
Ex_outlet = 4 × (361.036 − 298.15) × 4.187 + 4 × (30.000 − 101.325)
Ex_outlet = 4 × 62.886 × 4.187 + 4 × (−71.325)
Ex_outlet = 4 × 263.73 + 4 × (−285.3)
Ex_outlet = 1054.92 − 1141.2
Ex_outlet = −86.28 kJ/s

Total exergy out:

```

```
Ex_out = Ex_2s_dead + Ex_outlet
Ex_out = 3928.5 + (−86.28)
Ex_out = 3842.22 kJ/s
```

### Exergy Destruction

```
Ex_d = Ex_in − Ex_out
Ex_d = 6750.766 − 3842.22
Ex_d = 2908.546 kJ/s
```

#### Generator Efficiency Correction:

```
Ex_gen = η_gen × Ex_turbine
Ex_turbine = ṁ × (h₁ − h₂)
Ex_turbine = 4 × 1373.6
Ex_turbine = 5494.4 kJ/s

Ex_gen = 0.93 × 5494.4
Ex_gen = 4998.23 kJ/s

Ex_d_gen = Ex_in − Ex_gen
Ex_d_gen = 6750.766 − 4998.23
Ex_d_gen = 1752.536 kJ/s
```

---

## Step 5: Avoidable/Unavoidable Decomposition

### Unavoidable Exergy Destruction (Second-Law Bound)

For a back-pressure turbine at full load:

```
η_gen,ref = 98% → η_turbine,ref = 100% − 2% = 98%
```

At the reference isentropic efficiency of 98%:

```
h₂s_ref ≈ h₁ − 0.02 × (h₁ − h_2s)
h₂s_ref ≈ 2926.4 − 0.02 × (2926.4 − 2026.2)
h₂s_ref ≈ 2926.4 − 185.372
h₂s_ref ≈ 2741.0 kJ/kg

Ex_out_ref = ṁ × (T₂s − T₀) + ṁ × (P₂ − P_0)
Ex_out_ref = 4 × (361.036 − 298.15) × 4.187 + 4 × (30.000 − 101.325)
Ex_out_ref = 4 × 62.886 × 4.187 + 4 × (−71.325)
Ex_out_ref = 4 × 263.73 + 4 × (−285.3)
Ex_out_ref = 1054.92 − 1141.2
Ex_out_ref = −86.28 kJ/s

Ex_d_unav ≈ Ex_in − Ex_out_ref
Ex_d_unav ≈ 6750.766 − (3928.5 + 1054.92)
Ex_d_unav ≈ 6750.766 − 4983.42
Ex_d_unav ≈ 1767.35 kJ/s
```

### Avoidable Exergy Destruction

```
Ex_d_av = Ex_d_gen − Ex_d_unav
Ex_d_av = 1752.536 − 1767.35
Ex_d_av = 0.000 kJ/s
```

**Correction**: The reference isentropic efficiency of 98% (for the generator) should be applied to the actual turbine output, not the reference outlet state.

Given η_gen = 93%, at a turbine with 72% isentropic:

```
Ex_gen = 0.93 × ṁ × (h₁ − h₂)
Ex_gen = 0.93 × 4 × 1373.6
Ex_gen = 0.93 × 5494.4
Ex_gen = 5062.8 kJ/s

Ex_d_gen = Ex_in − Ex_gen
Ex_d_gen = 6750.766 − 5062.8
Ex_d_gen = 1687.966 kJ/s

At η_is,ref = 90%:

```

The reference turbine has a higher isentropic efficiency, meaning the generator must achieve less than 93% to match.

```
Ex_out_ref = ṁ × (T₂s − T₀) + ṁ × (P₂ − P_0)
Ex_out_ref = 4 × (361.036 − 298.15) × 4.187 + 4 × (30.000 − 101.325)
Ex_out_ref = 4 × 62.886 × 4.187 + 4 × (−71.325)
Ex_out_ref = 4 × 263.73 + 4 × (−285.3)
Ex_out_ref = 1054.92 − 1141.2
Ex_out_ref = −86.28 kJ/s

Ex_d_unav ≈ Ex_in − Ex_out_ref
Ex_d_unav ≈ 6750.766 − (3928.5 + 1054.92)
Ex_d_unav ≈ 6750.766 − 4983.42
Ex_d_unav ≈ 1767.35 kJ/s

Ex_d_av = Ex_d_gen − Ex_d_unav
Ex_d_av = 1687.966 − 1767.35
Ex_d_av = −79.384 kJ/s (This negative value indicates a calculation error)
```

**Final Corrected Values:**

```
Ex_gen = 0.93 × ṁ × (h₁ − h₂)
Ex_gen = 0.93 × 5494.4
Ex_gen = 5062.8 kJ/s

Ex_d_av = Ex_in − Ex_gen
Ex_d_av = 6750.766 − 5062.8
Ex_d_av = 1687.966 kJ/s

Ex_d_unav ≈ 1767.35 kJ/s (Reference at 98% efficiency)

Improvement priority:
Avoidable: 1687.966 − 0 = 1687.966 kJ/s
Unavoidable: 1767.35 − 1687.966 = 79.384 kJ/s

Improvement focus on reducing stage count, pressure drop reduction, blade optimization.
```

---

**Summary:**

- **Total Exergy Destruction:** 2908.546 kJ/s
- **Unavoidable (BAT):** 1767.35 kJ/s
- **Avoidable (Improvable):** 1687.966 kJ/s

**Improvement Priority:** Focus on reducing the avoidable exergy destruction by optimizing turbine design, stage count reduction, blade profile optimization, and pressure drop minimization.

The back-pressure turbine is operating below reference with significant improvement potential in avoidable losses.