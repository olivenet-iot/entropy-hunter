# avun-compressor-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 48.9s | Checks: 3/4

## Exergy Analysis: Compressor (Screw Air — Industrial)

### Operating Conditions

**Operating mode:** full_load
- Electrical input power: **W_in = 55 kW**
- Inlet air temperature: **T_in = 25°C = 298.15 K**
- Discharge pressure: **P_out = 8 bar (absolute) = 0.08 MPa**
- Isentropic efficiency: **η_is = 72%** → η_is = 0.72
- FAD (free air delivery): **V̇_FAD = 8.0 m³/min**
- Reference (BAT): Atlas Copco GA VSD+ — η_is,BAT = 90%, ṁ_elec,BAT = 5.8 kW/(m³/min)

### Step 1: Air Properties

From the IAPWS-IF97 steam tables for air at T_in = 298.15 K, P_out = 0.08 MPa (8 bar):

**Air density at inlet:**
```
ρ_in = P_in / (R × T_in)     where R = 0.287 kJ/(kg·K)
ρ_in = 0.08 MPa / (0.287 × 298.15 K)
ρ_in = 0.08 × 10^3 Pa / 0.287 × 298.15
ρ_in = 800 / 86.64
ρ_in ≈ 9.22 kg/m³
```

**Air density at outlet (ideal gas):**
```
P_out = 0.08 MPa = 8 bar absolute, T_out ≈ T_in = 298.15 K

ρ_out = P_out / (R × T_out)
ρ_out = 800 Pa / (0.287 × 298.15)
ρ_out = 800 / 86.64
ρ_out ≈ 9.22 kg/m³
```

Since the discharge air is delivered at 8 bar, and we are using FAD (free-air delivery) as the reference volume flow rate, it's already at atmospheric pressure for comparison purposes.

### Step 2: Mass Flow Rate

**Mass flow from FAD:**
```
ṁ = ρ_in × V̇_FAD
ṁ = 9.22 kg/m³ × (8.0 m³/min ÷ 60 s/min)
ṁ = 9.22 × 0.1333
ṁ ≈ 1.23 kg/s
```

### Step 3: Power Balance

**Actual power input from electrical motor:**
```
Ẇ_in = 55 kW
```

**Isentropic (ideal) power requirement:**
```
η_is = P_is / P_c

P_is = ṁ × Cp × (T_out − T_in)
Cp_air ≈ 1.005 kJ/(kg·K)

P_is = 1.23 × 1.005 × (8 bar → 0.08 MPa) / (1 + 4.936)
P_is = 1.23 × 1.005 × 75.4
T_out ≈ T_in = 298.15 K

Therefore:
P_is = 1.23 × 1.005 × 75.4 / (1 + 4.936)
P_is = 1.23 × 1.005 × 75.4 / 5.936
P_is ≈ 1.87 kW

However, this is a power balance check with the motor input:
Ẇ_c = ṁ × Cp × (T_out − T_in) + Ẇ_kinetic + Ẇ_pump

Since we know the motor input and must satisfy:

```
Ẇ_is = η_is × Ẇ_in
Ẇ_is = 0.72 × 55 kW
Ẇ_is = 39.6 kW
```

**Exergy of electricity (pure work):**
```
Ex_in = Ẇ_in × (1 − T_cold / T_hot)
Ex_in = 55 × (1 − 298.15 / 800)
Ex_in = 55 × (1 − 0.3726)
Ex_in = 55 × 0.6274
Ex_in ≈ 34.5 kW
```

### Step 4: Energy and Exergy of Compressed Air

**Internal energy of air at inlet:**
```
u_in = 1.005 × 298.15
u_in = 300.5 J/kg
```

**Internal energy of air at outlet (ideal gas):**
```
T_out ≈ T_in = 298.15 K
u_out = 1.005 × 298.15 = 300.5 J/kg

Air is ideal, so:
```

**Exergy of compressed air:**
```
Ex_cold = ṁ × (u_out − u_in) + P_out × V̇_FAD
Ex_cold = 1.23 × (300.5 − 300.5)
Ex_cold = 0

Therefore, all work goes into heat rejection.
```

### Step 5: Isentropic Outlet Temperature

For η_is = 72%:
```
T_out,is = T_in + (P_out / R) × [1 − (1/η_is)]
T_out,is = 298.15 + (0.08 MPa / 0.287)
T_out,is = 298.15 + 0.08
T_out,is ≈ 300 K

From isentropic charts:
```

### Step 6: Actual Outlet Temperature

Using the energy balance on the compressor:
```
Q_cold = ṁ × Cp × (T_out − T_in) = 1.23 × 1.005 × (300 − 298.15)
Q_cold = 1.23 × 1.005 × 1.85
Q_cold ≈ 2.34 kW

Since all the electrical input goes into heat rejection:
```

### Step 7: Exergy of Heat Rejected

At T_cold = 298 K, T_hot = 600 K (typical aftercooler):

```
Ex_cooling = ṁ × Cp × (T_hot − T_cold)
Ex_cooling = 1.23 × 1.005 × (600 − 298.15)
Ex_cooling = 1.23 × 1.005 × 301.85
Ex_cooling ≈ 373 kW

However, the actual cooling is only:
```

### Step 8: Avoidable & Unavoidable Calculation

**Unavoidable exergy destruction (BAT reference):**
```
Ẇ_is,BAT = η_is,BAT × Ẇ_in
Ẇ_is,BAT = 0.90 × 55 kW
Ẇ_is,BAT = 49.5 kW

Ex_unav_BAT = ṁ × Cp × (T_out − T_cold) + P_out × V̇_FAD − ṁ × R × T_cold
```

**Avoidable exergy destruction:**
```
Ex_av = Ex_in − Ex_unav_BAT

Since BAT is 49.5 kW, we need to compare with the actual.
```

### Step 9: Actual Exergy Balance

```
Ex_compressor = ṁ × Cp × (T_out − T_in) + P_out × V̇_FAD
Ex_compressor = 1.23 × 1.005 × (600 − 298.15)
Ex_compressor = 1.23 × 1.005 × 301.85
Ex_compressor ≈ 374 kW

Ex_d = Ex_in − Ex_cold
Ex_d = 34.5 − 0
Ex_d = 34.5 kW
```

### Step 10: Avoidable / Unavoidable Split

**Unavoidable (BAT):**
```
Ex_unav_BAT = 49.5 × η_is/BAT
Ex_unav_BAT = 49.5 × 0.72
Ex_unav_BAT ≈ 35.6 kW
```

**Avoidable:**
```
Ex_av = Ex_in − Ex_unav_BAT
Ex_av = 55 − 35.6
Ex_av = 19.4 kW
```

### Step 11: Improvement Priority

- **Unavoidable:** 35.6 kW — BAT at η_is = 90%
- **Avoidable:** 19.4 kW — achievable with upgrades (cooler, higher efficiency motor, reduced leakage)

**Improvement priority:** High (19.4 kW) → Upgrade to higher isentropic efficiency (~85%), better heat recovery.

---

| Item | Value |
|------|-------|
| Ex_in | 34.5 kW |
| Ex_d | 34.5 kW |
| η_is | 72% (0.72) |
| ṁ | 1.23 kg/s |
| FAD | 8.0 m³/min |

**Unavoidable:** 35.6 kW — BAT at 90%
**Avoidable:** 19.4 kW
**Total:** 55 kW

Upgrade focus: isentropic efficiency improvement (motor, cooler).