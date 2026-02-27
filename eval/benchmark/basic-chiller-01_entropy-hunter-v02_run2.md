# basic-chiller-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 45.1s | Checks: 3/3

## Exergy Analysis: Air-Cooled Screw Chiller (Full Load — 200 kW Cooling Capacity)

### Assumptions

1. Steady-state, steady-flow operation.
2. Kinetic and potential exergy changes are negligible.
3. The chiller is modelled as a black box; electricity input = work exergy (pure work).
4. Refrigerant: R-410A
5. COP (electrical) = 71.4 kW / 200 kW_cooling = 0.357; however, the problem provides COP = 2.8 as the overall energy efficiency ratio.
6. The "cooling capacity" of 200 kW refers to the cooling effect (ΔT-driven heat rejection from chilled water).
7. The condenser rejects waste heat at the ambient temperature (condenser rejects heat at T₀ = 35°C, but this is not a useful thermal reservoir for exergy analysis; it's rejected to surroundings).
8. The air-cooled condenser is modelled as rejecting heat to the environment at T₀ = 35°C.
9. Latent heat of vaporisation/condensation contributions are included in the Carnot refrigeration cycle calculations.

### Step 1: Basic Energy Balance

**COP definition:** COP = Q_cooling / W_comp
W_comp = Q_cooling / COP = 200 kW / 2.8 = **71.4 kW**

**Heat extracted from chilled water (Q_cold):**
Q_cold = ṁ_cw × Cp × ΔT_cooling
ΔT_cooling = T_chilled_supply - T_chilled_return = 7°C - 12°C = -5°C

However, the energy balance should reflect that Q_cold is actually the heat extracted from the chilled water:
Q_cold = ṁ_cw × Cp × (T_chilled_return - T_chilled_supply)
Where: ṁ_cw = Q_cold / (Cp × ΔT_cooling)

We need to determine ṁ_cw first:

### Step 2: Mass Flow Rate of Chilled Water

Q_cold = 200 kW
Cp_water = 4.18 kJ/(kg·K)
ΔT_cooling = 12°C - 7°C = 5 K

ṁ_cw = Q_cold / (Cp × ΔT_cooling) = 200 kW / (4.18 kJ/(kg·K) × 5 K) = **9.53 kg/s**

### Step 3: Cold Side Exergy Flow

Ex_cold = ṁ_cw × Cp × T₀ × ln(T_cold / T₀)
T_cold = 7°C = 280.15 K
T₀ = 35°C = 308.15 K

Ex_cold = 9.53 kg/s × 4.18 kJ/(kg·K) × (308.15 - 280.15) K × ln(280.15 / 308.15)
Ex_cold = 9.53 × 4.18 × 28 K × ln(0.91)
Ex_cold = 9.53 × 4.18 × 28 K × (-0.09) = **-116.6 kW**

The negative sign is expected (exergy out of the cold reservoir), so the magnitude is:
Ex_cold = 116.6 kW

### Step 4: Heat Rejected at Condenser

Q_cond = Q_cold + W_comp
Q_cond = 200 kW + 71.4 kW = **271.4 kW**

The condenser rejects this heat to the environment at T₀ = 35°C (modelled as 308.15 K).

### Step 5: Condenser Exergy Flow

Ex_cond = Q_cond × T₀ / T_source
Since the waste heat is rejected at ambient:
T_source = 35°C = 308.15 K
Ex_cond = 271.4 kW × (308.15 / 308.15) = **271.4 kW**

### Step 6: Carnot Refrigeration Cycle Efficiency

COP_Carnot = T_cold / (T_source - T_cold)
COP_Carnot = 280.15 K / (308.15 K - 280.15 K) = 280.15 / 28.0 = **9.97**

Actual COP = 2.8
Efficiency factor: η = actual / Carnot = 2.8 / 9.97 ≈ **0.2806 or 28.1%**

### Step 7: Exergy Balance

**Exergy input (work exergy):**
Ex_in = W_comp = 71.4 kW

**Exergy output (cooling exergy):**
Ex_out = Q_cold × T₀ / T_cold
Ex_out = 200 kW × 308.15 K / 280.15 K
Ex_out = 200 × 308.15 / 280.15 = **220.7 kW**

**Total useful exergy (heat rejected):**
Since the condenser rejects heat at ambient, we use the waste heat exergy:
Ex_cond = Q_cond × T₀ / T_source
Ex_cond = 271.4 kW × 308.15 K / 308.15 K = **271.4 kW**

**Total exergy output:**
Ex_out = Ex_cold + Ex_cond
Ex_out = 116.6 kW + 271.4 kW = **388.0 kW**

### Step 8: Exergy Balance Verification

Ex_in = Ex_out + Ex_waste
Ex_waste = Ex_in - Ex_out
Ex_waste = 71.4 kW - (116.6 + 271.4) kW = **-375.0 kW**

**Exergy destruction (second-law waste):**
Ex_d = 388.0 kW - 71.4 kW = **316.6 kW**

### Step 9: Thermodynamic Analysis Summary

| Item                | Value        | Unit |
|---------------------|-------------|------|
| Cooling capacity    | 200         | kW   |
| COP (electrical)    | 2.8         |      |
| Compressor power    | 71.4        | kW   |
| Condenser heat flow | 271.4       | kW   |
| Cold-side temperature| 7°C         | —    |
| Hot-side temperature | 35°C        | —    |
| Carnot COP          | 9.97        |      |
| Actual η (efficiency)| 0.2806 or 28.1% | —   |

### Step 10: Exergy Efficiency

η_ex = Q_cold / Ex_in = 200 kW / 71.4 kW = **2.80**

### Step 11: Avoidable and Unavoidable Exergy Losses

**Unavoidable exergy loss (minimum):**
Ex_unav = Q_cold × (T₀ - T_cold) / T_cold
Ex_unav = 200 kW × (308.15 K - 280.15 K) / 280.15 K
Ex_unav = 200 × 28 / 280.15 = **19.97 kW**

**Avoidable exergy loss:**
Ex_av = Ex_d - Ex_unav = 316.6 - 19.97 = **296.6 kW**

### Step 12: Improvement Priority

#### High Priority (Immediate):
- Optimise compressor efficiency.
- Upgrade to a higher COP screw or scroll mechanism.

#### Medium Priority:
- Improve condenser heat rejection effectiveness; reduce approach temperature.
- Reduce refrigerant charge and improve leakage detection/repair.

#### Low Priority:
- Ensure system insulation minimises heat loss from chilled water piping.

---

**Recommendation:** Focus on increasing the actual COP by optimising the compressor (reduce motor losses, increase isentropic efficiency), and reducing subcooling/superheating margins. The current COP of 2.8 is already relatively good for a screw chiller; further improvements are possible with careful design and operational tuning.

---

**Final Summary:**
- Exergy input = 71.4 kW
- Exergy output (cooling) = 116.6 kW
- Exergy waste (condenser rejection) = 271.4 kW
- Total exergy output = 388.0 kW
- COP_ex = 200 / 71.4 = **2.80**
- Avoidable loss: 296.6 kW
- Unavoidable loss: 19.97 kW
- Exergy efficiency (second-law efficiency): η_ex = 2.80

Achieving this level of exergy performance at full load indicates the unit is well-designed and operated; however, improvements can be sought to reduce avoidable losses further while maintaining the system balance.