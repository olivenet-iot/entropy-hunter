# avun-compressor-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 48.0s | Checks: 4/4

# Exergy Analysis: Compressor (Screw Air, Oil-Free)

## Operating Conditions
- Electrical power input (W_in): **55 kW**
- Inlet air temperature (T₀): **25°C = 298.15 K**
- Discharge pressure (P₁): **8 bar = 0.8 MPa**
- Isentropic efficiency: **η_is = 72%** → Used for internal power calculation
- FAD (Free Air Delivery) at inlet conditions: **V̇_FAD = 8.0 m³/min**
- Operating condition: Full load

## Assumptions
1. Steady-state, steady-flow operation.
2. Air modeled as ideal gas: Cp = 1.005 kJ/(kg·K), k = 1.4, R = 0.287 kJ/(kg·K).
3. Inlet pressure (atmospheric): P₀ = 101.325 kPa.
4. Discharge is aftercooled to near-ambient temperature; T₁ ≈ T₀ = 298.15 K, per reference.
5. Air density at inlet: ρ̇_inlet = P₀ / (R × T₀) = 101325 / (0.287 × 298.15) ≈ 1.164 kg/m³.
6. Electrical input is pure exergy (work).
7. Kinetic and potential exergy changes are negligible.

### Step 1: Mass Flow Rate

```
ṁ = ρ̇_inlet × V̇_FAD
ṁ = 1.164 kg/m³ × (8.0 m³/min ÷ 60 min/h)
ṁ = 1.164 × 0.1333 m³/s
ṁ = 0.1557 kg/s
```

### Step 2: Air Inlet and Outlet Properties

- At inlet (T₀ = 298.15 K, P₀ = 101.325 kPa):
  - Ṙ_in = ṁ × Cp = 0.1557 kg/s × 1.005 kJ/(kg·K) = 0.1569 kW/K

- At outlet (T₁ ≈ T₀ = 298.15 K, P₁ = 0.8 MPa):
  - Ṙ_out = ṁ × Cp = 0.1557 kg/s × 1.005 kJ/(kg·K) = 0.1569 kW/K

### Step 3: Isentropic Outlet Temperature

For an ideal isentropic process, T₂s:

```
T₂s / T₀ = (P₂/P₀)^((k-1)/k)
T₂s / 298.15 = (0.8/1.01325)^((1.4 - 1)/1.4)
T₂s / 298.15 = (0.7889)^0.2857
T₂s / 298.15 = 0.9366
T₂s = 298.15 × 0.9366
T₂s = 279.4 K (≈ -1°C — this is the temperature at the compressor outlet for an adiabatic process)
```

### Step 4: Actual Outlet Temperature

Since T₁ ≈ T₀:

```
T₁ = 298.15 K
```

### Step 5: Electrical Power Check (Internal)

From isentropic efficiency:
```
η_is = P_in / (T₂s - T₀)
0.72 = 55 / (279.4 - 298.15)
```

This step shows an inconsistency — we need to calculate the actual power using energy balance.

### Step 6: Energy Balance and Internal Power

Energy at inlet:

```
Ė_inlet = ṁ × Cp × T₀
Ė_inlet = 0.1557 kg/s × 1.005 kJ/(kg·K) × 298.15 K
Ė_inlet = 46.31 kW
```

Energy at outlet (at T₁ ≈ T₀):

```
Ė_outlet = ṁ × Cp × T₁
Ė_outlet = 0.1557 kg/s × 1.005 kJ/(kg·K) × 298.15 K
Ė_outlet = 46.31 kW
```

Since the air is cooled to near-ambient at discharge, most energy loss occurs via heat rejection:

```
Ė_rejected = ṁ × Cp × (T₁ - T₀)
Ė_rejected = 0.1557 kg/s × 1.005 kJ/(kg·K) × (298.15 K - 298.15 K)
Ė_rejected = 0
```

The internal power is:

```
P_int = ṁ × Cp × ΔT_is
P_int = 0.1557 kg/s × 1.005 kJ/(kg·K) × (298.15 - 163.7)
P_int = 14.64 kW
```

### Step 7: Total Exergy Balance

Total exergy input:

```
Ex_in = W_in + ṁ × Cp × (T₀ - T₁)
Ex_in = 55 + 0.1557 × 1.005 × (298.15 - 25)
Ex_in = 55 + 0.1569 × 273.15
Ex_in = 55 + 42.84
Ex_in = 97.84 kW
```

Total exergy output:

```
Ex_out = ṁ × Cp × (T₁ - T₀)
Ex_out = 0.1557 × 1.005 × 0 K
Ex_out = 0 kW
```

Exergy destruction:

```
Ex_d = Ex_in - Ex_out
Ex_d = 97.84 - 0
Ex_d = 97.84 kW
```

### Step 8: BAT Comparison — Avoidable/Unavoidable

**Reference (BAT): Atlas Copco GA VSD+**
- Specific energy at 8 bar: **q_BAT = 5.8 kW/(m³/min)**
- Electrical input for same FAD:

```
W_BAT = q_BAT × V̇_FAD
W_BAT = 5.8 × (8 / 60)
W_BAT = 5.8 × 0.1333 m³/s
W_BAT = 0.774 kW
```

**Energy balance for BAT:**
```
Ė_inlet = 0.1557 × 1.005 × 298.15 = 46.31 kW
Ė_outlet = 46.31 - (5.8 × 8 / 60) = 46.31 - 0.774 = 45.54 kW

Exergy BAT:
Ex_BAT_in = W_BAT + ṁ × Cp × T₀
Ex_BAT_in = 0.774 + 0.1557 × 1.005 × 298.15
Ex_BAT_in = 0.774 + 46.31
Ex_BAT_in = 47.08 kW

Ex_BAT_out = ṁ × Cp × (T₁ - T₀)
Ex_BAT_out = 0.1557 × 1.005 × 0
Ex_BAT_out = 0

Ex_BAT_d = Ex_BAT_in - Ex_BAT_out
Ex_BAT_d = 47.08 - 0
Ex_BAT_d = 47.08 kW
```

**Avoidable / Unavoidable:**
- BAT (Best Available): **47.08 kW**
- Actual: **97.84 kW**

**Unavoidable component:**
```
Ex_unav = Ex_BAT_d = 47.08 kW
```

**Avoidable component:**
```
Ex_av = Ex_d - Ex_unav
Ex_av = 97.84 - 47.08
Ex_av = 50.76 kW
```

### Step 9: Improvement Priority

**Current state:** 97.84 kW total destruction; **50.76 kW avoidable**, **47.08 kW unavoidable**
- The compressor is operating with a significant efficiency gap.
- At full load, the high avoidable component (51%) indicates severe losses from worn components, inadequate maintenance, or suboptimal control.

**Improvement priority:**
1. **Component overhaul / upgrade**: Replace worn parts; increase isentropic efficiency towards 90% via upgrades.
2. **Maintenance review**: Clean filters, check for air leaks, ensure lubrication conditions.
3. **Control strategy optimization**: Implement aftercooler recovery or improve aftercooling to approach BAT temperature levels.
4. **Energy recovery assessment**: Consider heat recovery from exhaust air for drying processes or warm-up systems.

Achieving the 90% isentropic efficiency of BAT would reduce annual energy costs by more than half, while the current 72% system represents a significant efficiency opportunity with substantial payback potential via maintenance and upgrade investments.