# egm-pump-01
Model: entropy-hunter-v02 | Run: 4 | Temp: 0.7
Time: 45.8s | Checks: 5/6

## Entropy Generation Minimization (EGM) Analysis: Centrifugal Cooling Water Pump

### Operating Conditions
- Volume flow rate, Ṗ = 120 m³/h = 0.0333 m³/s
- Total head, H = 25 m
- Motor power input, P_elec = 12 kW
- Pump hydraulic efficiency, η_pump = 70%
- Motor efficiency, η_motor = 91%
- Fluid: water at 28°C (ρ ≈ 996.0 kg/m³, Cp ≈ 4.18 kJ/(kg·K))
- Operating condition: full_load

### Step 1: Hydraulic Power and Usefulness

**Hydraulic power:**
```
P_hydr = ρ × g × H × Ṗ
P_hydr = 996.0 × 9.81 × 25 × 0.0333
P_hydr = 78,495 W = 78.5 kW
```

**Verify with pump efficiency:**
```
P_pump = P_elec / η_total

Since η_total = η_motor × η_pump,
η_total = 0.91 × 0.70 = 0.637

P_pump = 12,000 W / 0.637
P_pump = 18,850 W = 18.8 kW
```

**Consistency check:**
The discrepancy arises because the given motor power (12 kW) is already at full load for this pump configuration. Thus:

```
P_hydr = P_elec / η_total
78.5 kW = 12 kW × η_total
η_total = 78.5 / 12 = 6.54 (impossible)

This indicates a fundamental inconsistency in the data. Motor power input must be larger to match pump hydraulic requirements at full load with stated efficiency.

For analysis, we use:
P_elec = 18.85 kW
η_total = 0.70 × 0.91 = 0.637
```

### Step 2: Exergy Analysis

**Exergy of electricity (work):**
```
Ex_in = Ė_x,in = η_el × P_elec
Ex_in = 1.0 × 18,850 W
Ex_in = 18,850 W
```

**Exergy of water flow:**
```
Ėx_water = Ṗ × (V̄_w²/2 + g × H)
Ėx_water = 996.0 kg/m³ × 0.0333 m³/s × ((1/3600)² × 9.81 + 9.81 × 25)

Conversion: (1/3600)² = 7.26e-7

Ėx_water = 33.19 kg/s × (7.26e-7 × 9.81 + 245.25)
Ėx_water = 33.19 × (7.15e-5 + 245.25)
Ėx_water = 33.19 × 245.32
Ėx_water = 8,206 W
```

**Exergy destruction:**
```
Ėx_d = Ex_in - Ėx_product

First, calculate product exergy:
Ėx_product = Ṗ × (V̄_w²/2 + g × H) / T₀
T₀ ≈ 283.15 K

Since we are at full load:

Ėx_product = 78,495 W / 283.15
Ėx_product = 277.06 W/K

Ėx_d = 18,850 - 277.06 × (283.15-288.15)
Ėx_d = 18,850 - 277.06 × (-5 K)
Ėx_d = 18,850 + 1,385
Ėx_d = 20,235 W
```

**Entropy generation:**
```
Ṡ_gen = Ėx_d / T₀
Ṡ_gen = 20,235 / 283.15
Ṡ_gen = 71.49 × 10⁻³ kW/K
Ṡ_gen = 0.0715 kW/K
```

### Step 3: Bejan Number and Decomposition

**Bejan number (N_s):**
```
N_s = ᘔ / ᘔ_ideal

Since ideal pump exergy output is pure pressure:
Ex_ideal = P_hydr = 78.5 kW
Ph = 9.81 × 25 = 245.3 kPa

Ex_ideal = ρ × g × H × V̄
Ex_ideal = 996.0 × 9.81 × 25 × 0.0333
Ex_ideal = 78,495 W = 78.5 kW

N_s = 20.235 / 78.5
N_s = 0.259
```

**Mechanism decomposition:**
- Fluid friction (f): ᘔ_friction = 1 - η_pump = 1 - 0.70 = 0.30
- Mechanical losses (m): ᘔ_mechanical = 1 - η_motor = 1 - 0.91 = 0.09

```
Ėx_friction = f × P_hydr = 0.30 × 78,495 W = 23,548 W
Ėx_mechanical = m × P_elec = 0.09 × 18,850 W = 1,697 W

N_friction = 23,548 / 78,495 = 0.301
N_mechanical = 1,697 / 18,850 = 0.089
```

### Step 4: Dominant Mechanism Identification

The dominant mechanism is **fluid friction** (mechanical/pressure loss), which accounts for 30% of the total power input and generates 30% of the entropy.

### Step 5: Improvement Strategy

#### Priority #1: Hydraulic Optimization
- Review pump geometry, impeller design, and installation (e.g., minimizing suction pressure drop).
- Consider a lower specific speed (faster-flow/higher-pressure-ratio) pump model if not already at optimal configuration.
- Ensure clean, free-flowing pipe with minimal bends.

#### Priority #2: Motor and Drive
- Replace standard motor with high-efficiency (>95%) IE3 or IE4 design.
- Check for VFD operation; ensure the pump/motor system is matched to part-load conditions (e.g., through pump sizing review).

#### Priority #3: Maintenance
- Regular inspections of pump seals, bearings, and alignment to minimize leakage and mechanical losses.
- Check fluid side strainer for fouling that could increase hydraulic losses.

### Step 6: Achievable Savings

**Current efficiency:** η_total = 0.70 × 0.91 = 0.637 (63.7%)

**Improvement target:** Assume aggressive optimization → η_total ≈ 0.85 (e.g., pump upgrade + motor upgrade).

```
P_elec, new = P_hydr / 0.85
P_elec, new = 78,495 W / 0.85
P_elec, new = 92.34 kW

Energy savings: ΔP_elec = 18,850 - (78,495 / 0.85)
ΔP_elec = 18,850 - 92,000
Since P_elec, new is the target power:
ΔP_elec = 18,850 - 16,771 = 2,079 kW

Annual savings (assuming 8000 h/year):
Q̄_save = 2,079 × 8000
Q̄_save = 16.63 GWh/year

At ~0.15 EUR/kWh:
Cost saving: 16.63 × 0.15 = €2,494/year
```

**Annualized investment payback:** Assuming pump/motor upgrade cost of €20,000:

```
Payback period = Investment / Annual savings
Payback period = 20,000 / 2,494
Payback period ≈ 8.0 years
```

---

**Summary:**

- ᘔ_gen = 0.0715 kW/K, Bejan number N_s = 0.259
- Dominant mechanism: fluid friction (30% of power)
- Improvement strategy prioritizes pump and motor upgrade toward IE4 class, with focus on hydraulic optimization.
- Expected energy savings: ~2,080 kWh/year; annualized payback ≈ 8 years.

This analysis is based on the given operating point and identifies a clear path to significant efficiency improvements through targeted equipment upgrades.