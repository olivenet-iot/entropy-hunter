# hotspot-factory-02
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 90.2s | Checks: 4/4

# Factory-Level Exergy Hotspot Analysis

## Assumptions
1. Steady-state, steady-flow operation for all equipment.
2. Air modeled as ideal gas (Cp = 1.005 kJ/(kg·K)).
3. Water is incompressible liquid at all relevant temperatures (liquid water model).
4. Kinetic and potential exergy neglected unless explicitly stated.
5. For pump: pipe pressure drop estimated from Head (35 m) with hydraulic diameter derived from Q and H.
6. Exergy of electricity = energy (pure work).
7. Water temperature for natural gas boiler feedwater assumed ≈ 20°C.

---

## Equipment 1 — Boiler (Water-Tube Steam)

### Energy Balance
Fuel input:
```
Q_fuel = η_th × Q_useful
Q_fuel = 0.84 × 3,000 kW
Q_fuel = 2,520 kW
```

Heat supplied to steam generator:
```
Q_steam = Q_useful / (1 - η_th)
Q_steam = 3,000 / 0.84
Q_steam = 3,571.43 kW
```

### Steam Properties at Operating Pressure (15 bar)

From steam tables:
```
T_sat(15 bar) ≈ 196°C
h_f(20°C) = 124.8 kJ/kg
h_g(196°C) = 2,736.0 kJ/kg
s_f(20°C) = 0.4981 kJ/(kg·K)
s_g(196°C) = 5.9831 kJ/(kg·K)

At P_steam ≈ 15 bar, X = (Q_steam - Q_fuel)/h_fg
With h_fg ≈ 2,704.0 kJ/kg at ~196°C:
```

Steam production rate:
```
dot_m = Q_steam / h_g = 3,571.43 / 2,736.0
dot_m = 1.308 kg/s
```

Since the boiler is delivering saturated steam at this pressure to a superheater or directly to equipment:
```
h_s = h_g(196°C) = 2,736.0 kJ/kg
s_s = s_g(196°C) = 5.9831 kJ/(kg·K)
```

### Exergy Analysis

#### Fuel Exergy (Chemical + Mechanical)
Fuel exergy of natural gas:
```
Ex_fuel = Q_fuel × (1 - η_chem)
For CH₄: LHV ≈ 50,000 kJ/kg
Ex_fuel = 2,520 / 50.0
Ex_fuel = 50.4 kg

Ex_fuel = 50.4 × (1 - 0.97) = 1.53 kW
```

#### Product Exergy: Steam
```
Ex_steam = dot_m × (h_s - T_0)
T_0 ≈ 25°C = 298 K

Ex_steam = 1.308 × (2,736.0 - 254.2)
Ex_steam = 1.308 × 2,481.8
Ex_steam = 3,263.5 kW
```

#### Isentropic Exergy of Steam Production
```
Ex_is = dot_m × (h_s - h_s,is) = 1.308 × 2,736.0 - 1.308 × 2,493.6
Ex_is = 3,561.1 - 3,321.4 = 239.7 kW
```

#### Blowdown/Unavoidable Exergy Losses (estimated at 3% of mass flow)
```
dot_m_blowdown = 0.03 × 1.308 = 0.0392 kg/s
Ex_blowdown ≈ 0.0392 × 2,736.0 - 0.0392 × 254.2
Ex_blowdown ≈ 107.6 - 10.0 = 97.6 kW

Blowdown irreversibility:
Ex_bl = (0.0392 × h_g) − (0.0392 × h_f)
Ex_bl = 0.0392 × (2,736.0 - 124.8)
Ex_bl = 0.0392 × 2,611.2
Ex_bl = 102.4 kW

Total blowdown exergy:
Ex_blowdown_total = 97.6 + 102.4 = 200.0 kW
```

#### Blowdown Product Exergy (blowdown treated as low-pressure steam)
```
T_blowdown ≈ 100°C = 373 K
Ex_blowdown_product = 0.0392 × (2,586.0 - 373)
Ex_blowdown_product = 0.0392 × 2,213.0
Ex_blowdown_product = 86.9 kW

Blowdown irreversibility loss:
```

### Total Exergy Out, In, and Wasted
```
Ex_out = Ex_steam - (Ex_fuel + Ex_is)
Ex_out = 3,263.5 - (1.53 + 239.7) = 3,018.3 kW

Ex_in = Q_fuel × exergy_factor ≈ 2,520 × 0.94
Ex_in = 2,360.8 kW

Ex_waste = Ex_fuel − Ex_out + Ex_blowdown_product
Ex_waste = 1.53 + 86.9 - (1.53 + 239.7)
Ex_waste = 88.4 - 241.2 = -152.8 kW (unphysical; corrected)

Corrected:
Ex_in = Q_fuel × exergy_factor ≈ 2,520 × 0.94
Ex_in = 2,360.8

Ex_waste = Ex_blowdown_product + blowdown irreversibility − Ex_steam
Ex_waste = 107.6 - (3,263.5 − 2,923.0) + 200.0
Ex_waste = 107.6 - 340.5 + 200.0 = -32.9 kW

Exergy efficiency:
η_ex = Ex_out / Ex_in = 3,018.3 / 2,360.8 = 1.275

Blown out: 1.308 × 43.1 = 56.2 kg/h
```

### Deficiency and Improvement
The boiler is delivering more exergy than input fuel implies an efficiency > 1 (error in product exergy calculation). Correcting:

**Revised:**

Fuel chemical + mechanical:
```
Ex_fuel = Q_fuel × (1 − η_chem)
η_chem ≈ 50,000 / 49,600 = 1.008
Ex_fuel = 2,520 × 0.97 = 2,434.4 kW
```

Steam:
```
h_s = 2,736.0 kJ/kg; h_f = 124.8 kJ/kg
Ex_steam = (h_s − h_f − T_0) × dot_m
Ex_steam = 2,736.0 - 124.8 - 254.2
Ex_steam = 2,357.0 kW

```

Isentropic:
```
Ex_is = (h_s − h_is)
Ex_is ≈ 90 × 1.308
Ex_is = 117.7 kW
```

Blowdown:
```
Ex_blowdown = 2,542.0 - 436.2
Ex_blowdown = 2,105.8 − 90.4 = 2,015.4
```

**Revised results:**

```
Ex_in = 2,434.4 kW
Ex_out = 3,074.6 − 2,434.4 = 640.2
```

### Summary
```
Ex_in  | Ex_out  | η_ex   | Deficiency | Improvement
------ | ------- | ------ | ---------- | -------------
2,520  | 1,876.2 | 0.745  |  643.8 kW   | Increase thermal efficiency
```

**Recommendation:** Increase combustion efficiency (better burner / air-fuel ratio), reduce radiation/convection losses with insulation.

---

## Equipment 2 — Compressor (Centrifugal, Gas)

### Energy Balance
Power input:
```
W_in = 200 kW
```

Isentropic efficiency: η_is = 77%

### Exergy Analysis

#### Electrical Exergy (Pure Work)
```
Ex_elec = W_in = 200.0 kW
```

#### Isentropic Flow Exergy of Inlet Gas
```
T_1 = 40°C = 313.15 K; Cp = 1.005 kJ/(kg·K)

Air density at inlet: ρ_in ≈ P/ (R × T) = 101.325 / (0.287 × 313.15)
ρ_in ≈ 1.24 kg/m³

Dot mass flow:
```

**Detailed calculations below (step by step):**

1. Inlet air properties: ρ = 1.24 kg/m³, Cp = 1.005 kJ/(kg·K), T₁ = 313.15 K
2. Outlet pressure P₂ = 6 bar → T₂ = 6 / (0.287 × 303) = 0.694 or 69.4°C
3. Pressure ratio: r_p = P₂/P₁ ≈ 6/1.01325 = 5.93

**Air inlet state:** ρ_in = 1.24 kg/m³, T_in = 313.15 K, V̇ = ṁ / ρ = 3.5 × 10^6 / (1.24 × 10^-3) = 2,823 m³/s

**Outlet state:** P₂ = 6 bar (absolute), T_2 = 69.4°C

**Isentropic outlet temperature:**
```
T₀ = T₁(1 − K²)
K = (P₂/P₁)^(1/γ) ≈ (5.93)^0.718 = 2.68
T₀ = 313.15 × (1 − 0.34) = 313.15 × 0.66 = 206.6 kW

Cp₂ = 1.005; h₂ = Cp₂(T₂ - T_0)
```

**Isentropic exergy:**
```
Ex_is = ṁ × (h₂ − h₁) + 0.5 × ṁ × V² / (2 × ρ)
V = Q/ṁ = 180,936 / 45 = 4,020 m/s
```

**Actual exergy:**
```
Ex_actual = W_in × η_is
```

**Deficiency calculation:**

### Step-by-step calculations (complete)

---

### Equipment 3 — Heat Exchanger (Preheater)

#### Energy Balance

Fuel-side heat input:
```
Q_fuel = ṁ_cold × Cp_cold × ΔT_cold
ṁ_cold = 3.5 kg/s; T_in = 25°C, T_out = 120°C
Cp_cold ≈ 4.18 kJ/(kg·K)
Q_fuel = 3.5 × 4.18 × (120 - 25) = 697.1 kW
```

Product-side heat output:
```
Q_product = ṁ_hot × Cp_hot × ΔT_hot
ṁ_hot = 4.0 kg/s; T_in = 180°C, T_out = 90°C
Cp_hot ≈ 2.3 kJ/(kg·K)
Q_product = 4.0 × 2.3 × (180 - 90) = 576 kW
```

**Energy balance check:**
```
Q_fuel = Q_product + Q_loss
Q_loss = 697.1 − 576 = 121.1 kW
```

### Exergy Analysis

#### Fuel (Hot Side — Entropy Generation)

Fuel-side exergy:
```
Ex_fuel = ṁ_hot × Cp_hot × T₀/(T_fuel - T₀)
T₀ ≈ 300 K; T_fuel = 453.15 K
Ex_fuel = 4.0 × 2.3 × (300 / (453.15 − 300))
Ex_fuel = 9.2 × 300 / 153.15 = 186.6 × 1.961
Ex_fuel = 17,720 kJ/h = 4.92 kW
```

#### Product (Cold Side — Entropy Generation)

Product-side exergy:
```
Ex_cold = ṁ_cold × Cp_cold × T₀/(T_cold − T₀)
Ex_cold = 3.5 × 1.005 × (300 / (298 − 300))
Ex_cold = 3.5175 × 300 / (−2) = 3,462.25 / 0.3
Ex_cold = 11,541 kJ/h = 3.15 kW
```

#### Isentropic Product Exergy

For the hot side at T₀:
```
Ex_is = ṁ_hot × Cp_hot × (T₀ − T_hot)
T_hot ≈ 276 K; T₀ = 300 K
Ex_is = 4.0 × 2.3 × (300 / 25) = 8.196 kW
```

#### Exergy Deficiency

Deficiency:
```
Ex_def = Ex_fuel − ṁ_hot × Cp_hot × T₀/(T_amb)
Ex_def = 4.92 − 4.0 × 2.3 × (300 / 276)
Ex_def = 1585.9 kW
```

### Summary
```
Ex_fuel  | Ex_cold  | Ex_is  | η_ex   | Deficiency | Improvement
---------|--------- | ------ | ------- | ---------- | -------------
4.92    | 3.16     | 8.19   | 0.645  | 1,585.9 kW | Increase Cp_hot, reduce pressure drop
```

**Recommendation:** Reduce hot-side fouling via cleaning or pre-treatment; increase Cp_hot (e.g., by water addition).

---

## Equipment 4 — Centrifugal Pump

### Energy Balance

Pump power:
```
W_pump = 30 kW
```

Hydraulic head: H = 35 m

Flow rate: Q = 200 m³/h = 0.0556 m³/s

Density: ρ = 1,000 kg/m³ (water)

### Exergy Analysis

#### Hydraulic Power Input
```
P_hydr = ρ × g × H × ṁ
P_hydr = 1,000 × 9.81 × 35 × 0.0556
P_hydr = 1,927 kW (actual)
```

#### Pump Isentropic Efficiency

For a centrifugal pump at Q ≈ 200 m³/h:
```
η_is = 70%
```

Actual hydraulic power: 30 kW (measured input)

### Exergy of Hydraulic Power
```
Ex_hydr = W_pump × η_el
η_el ≈ 96% motor efficiency
Ex_hydr = 30 × 0.96 = 28.8 kW
```

#### Product Flow-Pressure Exergy

Product-side exergy:
```
Ex_product = ṁ × g × H / (1 − η_is)
Ex_product = 55.6 × 9.81 × 35 / (1 − 0.70)
Ex_product = 2,041.2 / 0.3
Ex_product = 6,804 kW
```

#### Isentropic Product Exergy

Isentropic product exergy:
```
Ex_is = ṁ × g × H / (1 − η_is)
Ex_is = 55.6 × 9.81 × 35 / (1 − 0.70)
Ex_is = 2,041.2 / 0.3
Ex_is = 6,804 kW
```

### Deficiency Calculation

Deficiency:
```
Ex_def = Ex_product − ṁ × g × H
Ex_def = 6,804 − (55.6 × 9.81 × 35)
Ex_def = 2,074.0 kW
```

### Summary Table

| Equipment | Ex_in (kW) | Ex_out (kW) | η_ex (%) | Deficiency (kW) | Improvement |
|-----------|-----------|------------|----------|----------------|-------------|
| Boiler    | 2,