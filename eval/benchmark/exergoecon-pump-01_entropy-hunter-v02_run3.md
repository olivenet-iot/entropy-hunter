# exergoecon-pump-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 68.5s | Checks: 5/6

## Exergoeconomic (SPECO) Analysis: Centrifugal Pump (Full Load)

### Operating Conditions
- Volume flow rate, Ṡ = 80 m³/h
- Total head, H = 40 m
- Motor power, P_elec = 15 kW
- Pump hydraulic efficiency, η_pump = 75%
- Motor efficiency, η_motor = 93%
- Fluid: water at 25°C
- Operating condition: full_load

### Step 1: Basic Energy Calculations

#### Hydraulic Power (Useful Work)
```
P_hyd = ρ × g × H × Ṡ
```

Given:
- ρ (water density at 25°C) = 997 kg/m³
- g = 9.807 m/s²
- Ṡ = 80 / 3600 = 0.02222 m³/s

```
P_hyd = 997 × 9.807 × 40 × 0.02222
P_hyd = 997 × 9.807 × 0.93684
P_hyd = 91,523 W = 91.5 kW
```

#### Motor Power (Electrical Input)
```
P_elec = P_hyd / η_pump
P_elec = 91,500 W / 0.75
P_elec = 121,999.98 W = 121.9 kW
```

The pump requires **122.0 kW** from the motor to achieve a useful hydraulic output of 91.5 kW at these operating conditions.

#### Motor Electrical Consumption (Including Motor Losses)
```
P_motor = P_elec / η_motor
P_motor = 121,999.98 W / 0.93
P_motor = 131,267.94 W = 131.3 kW
```

### Step 2: Exergy Calculations

#### Exergy of Electrical Power (First Law)
The exergy associated with pure electrical work is the same as its energy content:
```
Ex_in = P_elec × η_elc = 121,999.98 W
```

#### Exergy of Hydraulic Output
```
Ex_hyd = Q × (T_0 → T_s) + Q × g × H × (1 - η_pump)
```

For water at 25°C:
- Temperature rise across the pump is negligible for industrial water (ΔT < 3°C), so exergy due to temperature difference is zero.
- Therefore:

```
Ex_hyd = Ṡ × g × H × (1 - η_pump)
Ex_hyd = 0.02222 m³/s × 9.807 m/s² × 40 m × (1 - 0.75)
Ex_hyd = 0.02222 × 9.807 × 40 × 0.25
Ex_hyd = 0.02222 × 9.807 × 10
Ex_hyd = 0.02222 × 98.07
Ex_hyd = 2.183 kW
```

#### Exergy Wasted (Motor and Pump Losses)
```
Ex_waste = P_elec - Ex_hyd
Ex_waste = 121,999.98 W - 91,500 W
Ex_waste = 30,499.98 W = 30.5 kW
```

#### Total Exergy Output and Efficiency
```
Ex_out = Ex_hyd = 91.5 kW

Exergy efficiency:
η_ex = Ex_out / Ex_in
η_ex = 91,500 W / 121,999.98 W
η_ex = 0.751 or 75.1%
```

### Step 3: Entropy Generation and Second-Law Calculations

#### Total Power Dissipation (First Law)
```
P_diss = P_elec - P_hyd = 121,999.98 W - 91,500 W
P_diss = 30,499.98 W = 30.5 kW
```

#### Entropy Generation Rate (Second Law)
```
Ṡ_gen = P_diss / T₀
T₀ = 298.15 K

Ṡ_gen = 30,499.98 W / 298.15 K
Ṡ_gen = 102.36 × 10⁻³ kW/K
Ṡ_gen = 0.102 kW/K
```

#### Bejan Number (Efficiency Quality)
```
N_s = Ṡ_gen / (T₀ × ΔT_diss)

ΔT_diss is taken from Carnot: for a pure heat pump cycle

Carnot eff = 1 - T_cold/T_hot
For water at ~25°C and motor losses:

T_hot ≈ 400 K (motor heats up)
T_cold = 298.15 K
eff_Carnot = 1 - 298.15 / 400 = 0.267

Thus:
P_hyd / P_elec = η_pump = 0.75 (actual useful)

The effective Carnot cycle is between T_cold and T_hot
eff_Carnot_effective = 1 - 298.15/(298.15 + 36) = 1 - 262/334.15 ≈ 0.217

Therefore:
Ṡ_gen / (T₀ × ΔT_diss) = (P_diss / T₀) / (T_hot - T_cold)
N_s = 0.102 kW/K / ((400 - 298.15) K)
N_s = 0.102 / 101.85
N_s = 0.001003

```

#### Exergy-Based Efficiency Improvement Potential (SPECO)
```
ξ_ex = η_ex / η_ex,ideal = 0.751 / 1 = 0.751 → 24.9%

For a centrifugal pump: the minimum possible exergy efficiency with water at 25°C and good maintenance is about 86%. Therefore:

η_ex,optim = 0.86
ΔEx_save = (η_ex,optim - η_ex) × Ex_in
ΔEx_save = (0.86 - 0.751) × 121.999 W
ΔEx_save = 0.109 × 121.999
ΔEx_save = 13.25 kW

Annual energy savings:
E_s = ΔEx_save × Ė_fuel = 13,250 × 0.751 = 9,946.25 kW/h/year

Cost saving: Ċ_s = E_s × c_elec = 9,946.25 × 0.11
Č_s = 1,094.087 EUR/year
```

### Step 4: Economic Analysis — SPECO Method (Ż - Ż₀)

#### Reference Cost Calculation (PEC → TCI)
```
TCI = PEC × CF_install × (1 + i)^n
PEC = €4,500
CF_install = 1.50
i = 6%
n = 15

TCI = 4,500 × 1.50 × (1 + 0.06)^15
TCI = 6,750 × 2.396558
TCI = €16,135.60
```

#### Annual Maintenance Cost
```
C_maintenance = 6% of TCI/year
C_maintenance = 0.06 × 16,135.60
C_maintenance = €968.14
```

#### Annual Operating Costs (Electricity)
```
Ż = Ė_elec × c_elec
Ė_elec = P_hyd + P_diss

Ė_elec = 91,500 W + 30,499.98 W
Ė_elec = 121,999.98 W

Ż = 121,999.98 × 0.000367 (0.11 EUR/kWh)
Ż = 45.24 EUR/h

Annual operating cost:
Z_op = Ż × h_op
Z_op = 45.24 × 8,000
Z_op = €361,920/year
```

#### Total Annual Cost (TAC)
```
TAC = TCI × r + Z_op + C_maintenance
r = interest rate = 6%
TCI = 16,135.60 EUR

TAC = 16,135.60 × 0.06 × (1 + 0.06)^15 + 361,920 + 968.14
TAC = 16,135.60 × 0.06 × 2.396558 + 361,920 + 968.14
TAC = 2,427.90 + 361,920 + 968.14
TAC = €365,316.04/year
```

#### Year 0 (Present Value)
```
PV = TCI / (1 + i)^n
PV = 16,135.60 / (1 + 0.06)^15
PV = 16,135.60 / 2.396558
PV = €6,747.67
```

#### Ż₀ — Minimum Annual Operating Cost with Perfect Maintenance
```
Ż₀ = Ė_elec × c_elec

For perfect maintenance: Ṡ_diss → 0 → P_diss → 0 (no losses)

Ż₀ = 91,500 W × 0.000367
Ż₀ = 33.6 EUR/h

Annual Ż₀:
Z₀_op = Ż₀ × h_op
Z₀_op = 33.6 × 8,000
Z₀_op = €268,800/year
```

#### SPECO Ratio ( Ż / Ż₀)
```
f-factor: Ż / Ż₀
f-factor = 361,920 / 268,800
f-factor = 1.347

CRF: Ż₀ / TCI
CRF = 268,800 / 16,135.60
CRF = 16.665

The pump is operating at 93% efficiency with 15 kW motor — relatively good but not outstanding.
```

### Step 5: Optimization Strategy

**Current situation:** f-factor of 1.347 (high), CRF of 16.665 (excellent) — the pump is operating above average for this class, so improvements should focus on reducing losses and increasing efficiency.

**Action Plan:**
1. **Motor Upgrade:** Replace existing motor with a higher-efficiency IE3 or IE2-rated unit.
   - Expected savings = 7%–9%
2. **Bearings/Seals Maintenance:** Regular lubrication and seal checks to reduce mechanical friction.
   - Expected savings = 0.5%–1%
3. **Flow Optimization:** Remove throttling valves or reconfigure the system for higher efficiency at full load.
   - Expected savings = 2%–5%
4. **Motor-Associated Part Load Optimizer (MPC):** Implement an auto-tuning VFD to reduce no-load losses and improve part-load performance.
   - Expected savings = 3%–6%

**Projected Ż reduction with optimization:**
```
Ż_opt = Ż × (1 - 0.07) = 361,920 × 0.93
Ż_opt = 335,485 EUR/year

Annual savings:
ΔŻ = Ż - Ż_opt
ΔŻ = 361,920 - 335,485
ΔŻ = 26,435 EUR/year

Life cycle cost reduction (LCCR):
LCCR = ΔŻ × n / TCI
LCCR = 26,435 × 15 / 16,135.60
LCCR = 398,25 / 16,135.60
LCCR = 24.7%
```

---

**Summary:**
- Ż = €361,920/year (current)
- Ż₀ (perfect maintenance) = €268,800/year
- f-factor = 1.347 → pump is operating above average; optimization focus on reducing losses.
- CRF = 16.665 — excellent overall value for the investment.
- Optimization strategy: motor upgrade (IE3), bearing/seal maintenance, flow optimization, and VFD control.

**Annual savings:** €26,435/year → LCCR = 24.7%.

Recommend prioritizing motor replacement with an IE3 unit to achieve at least a 93%–95% hydraulic efficiency level across the operating range.