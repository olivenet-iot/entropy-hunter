# egm-compressor-01
Model: entropy-hunter
Time: 272.0s
Checks: 3/6

## EGM Analysis: Centrifugal Compressor (Full Load)

### Assumptions

1. Steady-state, steady-flow operation
2. Air modeled as ideal gas: Cp = 1.005 kJ/(kg·K), R = 0.287 kJ/(kg·K)
3. Inlet conditions: T₁ = 30°C (303.15 K), P₁ = 1 atm (101.325 kPa)
4. Discharge pressure: P₂ = 10 bar (1,000 kPa) — aftercooled system inferred since standard discharge is ~7–8 bar; cooled to near-ambient for practical purposes
5. Electrical power input: 150 kW (shaft + losses); η_is = 80% accounts for all losses in the compressor
6. FAD at inlet: Ṽ_in = 20 m³/min (measured at inlet conditions)
7. Kinetic and potential exergy changes neglected

### Step 1: Mass Flow Rate Determination

Using ideal gas law at inlet:

```
ρ₁ = P₁ / (R × T₁) = 101.325 / (0.287 × 303.15)
ρ₁ = 101.325 / 86.93
ρ₁ = 1.1642 kg/m³
```

```
ṁ = ρ₁ × Ṽ_in = 1.1642 × (20/60) m³/s
ṁ = 1.1642 × 0.03333 m³/s
ṁ = 0.03881 kg/s
```

### Step 2: Isentropic Discharge Temperature

First, find T₂s (isentropic discharge temperature):

```
P₁/P₂ = T₁/T₂s
T₂s = T₁ × P₂ / P₁ = 303.15 × 1000/101.325
T₂s = 303.15 × 9.8692
T₂s = 2,994.87 K

Since T₂s > T₀ (300 K), the cooled compressor model is correct:
Aftercooled discharge at T₂ ≈ T₁ = 303.15 K.
```

The useful exergy stream from compression is:

**Ex_inlet → outlet = ṁ × [(T₂ - T₁) - T₀ ln(T₂/T₁)]**

Since T₂ ≈ T₁ for aftercooled discharge (cooling removes all heat), we get:

```
ΔT = 0; T₂ = T₁ = 303.15 K
Ex_outlet = ṁ × [T₁(1 - 1) - R × T₁ ln(T₂/T₁)]
Ex_outlet = 0
```

The electrical power is entirely dissipated as heat rejection (heat to the environment, mostly in aftercooler + casing losses).

**Reformulation — Recognize Ex_inlet = W_shaft since no temperature rise:**

Since the air enters and leaves at essentially identical temperatures, the "product" is not pressure exergy but thermal management cost. We need:

```
Ex_product = ṁ × [(T₂ - T₁) - T₀ ln(T₂/T₁)]
= 0.03881 × [303.15(1-1) - 273.15 × (ln(1))]
= 0
```

However, the **real product** is the compression work itself — electricity input less mechanical/heat loss. The useful exergy recovered is the thermal waste (cooling duty).

The key entropy generation terms:

#### Electrical Power Input as Pure Exergy:
```
Ėx_in = ṁ × Cp × ln(T₂/T₁) + P_elec × (1 - η_is)
Since T₂ ≈ T₁, the first term is negligible.

Ėx_in = 150 kW (electrical input is pure work, treated as exergy)
```

#### Thermal Waste to Environment (Aftercooler Reject):
The compressor generates heat Q_gen at T₀ (environmental rejection):

```
Q_gen = W_shaft + ṁ × Cp × (T₂ - T₁)

Since T₂ ≈ T₁:
Q_gen = 150 kW + 0.03881 × 1.005 × [303.15-303.15]
Q_gen = 150 + 0

However, the compressor generates heat at ~isentropic T ≈ 472 K (for a cooled system):
Q_gen = ṁ × Cp × (T₂s - T₁) = 0.03881 × 1.005 × (472-303.15)
Q_gen = 0.03881 × 1.005 × 168.85
Q_gen = 6.59 kW (isentropic heating in cooled system)
```

Since Q_gen is at T₀, its exergy is zero. However, the compressor takes electricity and outputs heat to the environment.

The useful product of this cooled compressor is cooling duty:

**Ex_product (cooling duty) = ṁ × Cp × |T₂ - T₁| ≈ 0**

But since all the 150 kW goes into Q_gen, we measure entropy from electrical input:

#### Entropy Generation

For a cooled system with W_shaft = 150 kW, all heat rejected at T₀. The thermal component drives the entropy generation:

```
Ṡ_gen = ṁ × Cp × (T₂s/T₁ - 1) + W_shaft/(T₀)
```

The first term dominates (isentropic heating):

```
T₂s/T₁ - 1 = 472/303.15 - 1 ≈ 1.5569 - 1 = 0.5569
Ṡ_gen_thermal = 0.03881 × 1.005 × ln(1.5569)
= 0.0388855 × 0.47286
= 0.01833 kW/K

The electrical component:
W_shaft/T₀ = 150 / 273.15 = 0.5502 kW/K

Total:
Ṡ_gen = 0.01833 + 0.5502
= 0.5685 kW/K → 0.569 kW/K
```

**Final values:**

1. Total entropy generation rate (Ṡ_gen) = **0.569 kW/K**
2. Bejan number (N_s): Ratio of mechanism-specific entropy flows.
3. Decomposition:

   - **Heat rejection at T₀:** 6.59 kW → entropy 0, no exergy
   - **Shaft work input:** 150 kW at T₀ → entropy 150/273 = 0.5502 kW/K (pure exergy)
   - **Electrical input is pure exergy** — treated as 150 kW at T₀.

Since all 150 kW goes into Q_gen heat, the dominant mechanism:

```
N_s = |Heat rejection| / ṁCp(T₂s-T₁) ≈ 6.59 / 0 → ∞
N_s = |Shaft work| / ṁCpΔT ≈ 150 / (38.81×0.472) = 150/18.326 = 8.19

Thus, the **dominant mechanism** is heat rejection (waste at T₀).
```

4. **Recommendations:**

   - The cooling duty is a useful product; reduce it if cooling load decreases.
   - Reduce motor and drive losses to decrease waste heat output.
   - Improve aftercooler efficiency for reduced thermal losses.

In summary, while the electrical input is pure work, the system rejects 6.59 kW of heat at T₀, driving the entropy generation via thermal irreversibility. The actual product (cooling) has no exergy content since T₂ ≈ T₁; only the waste stream matters in entropy terms.

For a more physical analysis: the **thermal exergy destruction** is the key metric:

```
Ėx_d = Q_gen - ṁCpΔT
= 6.59 kW (heat to environment) + 0.03881 × 1.005 × (472-303.15)
= 6.59 kW + 6.49 kW = 13.08 kW

The **reduced Bejan number** with thermal destruction:

N_s,thermal = Q_gen / ṁCpΔT ≈ 6.59 / (0.03881 × 1.005) = 6.59 / 0.03902 = 167.7
```

The cooling is the product, the waste heat drives irreversibility.

**Final summary block:**

**Product:** Cooling duty (no exergy content in final compressed air)
**Waste:** Heat rejection at T₀

**Energy balance:**
- Shaft input: 150 kW
- Q_gen = 6.59 kW → useful for cooling but waste exergy
- ṁCpΔT = 0 (useless)

**Entropy generation summary:**
- Thermal irreversibility dominates as waste heat rejection.
- Total entropy generation rate: **Ṡ_gen = 0.5685 kW/K**

**Recommendations:** Focus on aftercooler efficiency to reduce Q_gen, and ensure the compressor is sized correctly for actual load (verify cooling duty matches demand).