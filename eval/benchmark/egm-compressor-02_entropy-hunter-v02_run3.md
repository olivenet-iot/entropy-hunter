# egm-compressor-02
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 67.1s | Checks: 4/6

# Entropy Generation Minimization (EGM) Analysis: Screw Air Compressor (Part Load)

## Operating Conditions
- **Nominal power:** 90 kW (full load)
- **Operating condition:** Part load ~72% → Actual electrical input P_in = 65 kW
- **Inlet air temperature T_0:** 35°C (308.15 K)
- **Discharge pressure P_1:** 8 bar ≈ 800 kPa
- **FAD at nominal:** V̇_FAD, Nom = 9.0 m³/min → FAD at part load: V̇_FAD = 6.25 m³/min (assuming proportional reduction)
- **Isentropic efficiency η_is:** 68% at part load
- **Working fluid:** Air

### Assumptions
1. Steady-state, steady-flow operation.
2. Air modelled as ideal gas with Cp = 1.005 kJ/(kg·K), R = 0.287 kJ/(kg·K).
3. Relative humidity neglected (compressor operates above dew point at full load; part-load correction is implicit in the given FAD reduction and η_is values).
4. No heat recovery from motor/aftercooler losses.
5. Kinetic and potential exergy changes are negligible.

---

## 1. Mass Flow Rate

Air density at T_0 = 308.15 K, P_0 = 101.325 kPa (atmospheric):
```
ρ_0 = P_0 / (R × T_0) = 101.325 / (0.287 × 308.15)
ρ_0 ≈ 1.164 kg/m³
```

Actual mass flow rate at part load:
```
ṁ = ρ_0 × V̇_FAD = 1.164 × 0.104167 m³/s (converting FAD to m³/s)
ṁ ≈ 0.1205 kg/s
```

---

## 2. Energy Balance

### Compressor power input at part load

```
P_in = 65 kW
```

### Air inlet state: T_0 = 308.15 K, P_0 = 101.325 kPa (atmospheric)

Air outlet at 8 bar:
```
T_1 = T_0 + ΔT_s (sensible temperature rise in adiabatic compressor model)
```

Using isentropic efficiency: η_is = 68% for a single-stage screw at part load.

We first calculate the theoretical discharge temperature using the Carnot/Isentropic expansion ratio:

```
P_ratio = P_1 / P_0 = 800 / 101.325 ≈ 7.90
T_is = T_0 × (P_1/P_0)^(Cp/R)
T_is = 308.15 × (7.90)^((1.005/0.287)) 
T_is = 308.15 × (7.90)^3.49
T_is ≈ 308.15 × 336.06
T_is ≈ 103,323 K   (This is a gross error — the compressor cannot achieve this temperature; we need to use energy balance)

Let's calculate T_1 using energy balance at T_0 = 308.15:

```
Cp × ṁ × ΔT = η_is × P_in
1.005 × 0.1205 × (T_1 - 308.15) = 0.68 × 65
0.1210475 × (T_1 - 308.15) = 44.2
T_1 - 308.15 = 44.2 / 0.1210475
T_1 ≈ 44.2 / 0.1210475 + 308.15
T_1 ≈ 365.09 K
```

### Exergy of compressed air

At P_1 = 8 bar (absolute), T_1 = 365.09 K:

```
Ex_air = ṁ × (Cp × T_0 - R × ln(P_1/P_0) + (P_1 - P_0)/R)
Ex_air = 0.1205 × ((1.005 × 308.15) − (0.287 × ln(801.325/101.325)) + (800−101.325)/0.287)
Ex_air = 0.1205 × ((1.005 × 308.15) − (0.287 × ln(7.91))) + 2466.27/0.287
Ex_air = 0.1205 × (309.69 + (−0.287 × 2.067) + 8583.8)
Ex_air = 0.1205 × (309.69 − 0.594 + 8583.8)
Ex_air = 0.1205 × 8893.99
Ex_air ≈ 1073.2 kW
```

### Electrical input

```
Ė_el = P_in = 65 kW
```

---

## 3. Exergy Balance

### Compressor isentropic exergy output (Cp × T_1)

```
Ex_is = ṁ × Cp × (T_1 − T_0)
Ex_is = 0.1205 × 1.005 × (365.09 − 308.15)
Ex_is = 0.1205 × 1.005 × 56.94
Ex_is ≈ 7.27 kW
```

### Total exergy output

```
Ex_out = ṁ × (P_1 − P_0)/R + ṁ × Cp × T_0 − ṁ × R × ln(P_1/P_0)
Ex_out = 0.1205 × (800/0.287) + 0.1205 × 1.005 × 308.15 − 0.1205 × 0.287 × ln(801.325/101.325)
Ex_out = 0.1205 × 2796.4 + 0.1205 × 309.69 − 0.1205 × 0.287 × ln(7.91)
Ex_out = 337.52 + 37.11 − 0.1205 × 0.287 × 2.067
Ex_out = 337.52 + 37.11 − 0.0694
Ex_out ≈ 374.56 kW
```

### Exergy efficiency

```
η_ex = ṁ × (P_1 − P_0)/R / (Ė_el − Ex_is)
η_ex = 0.1205 × (800/0.287) / (65 − 7.27)
η_ex = 344.98 / 57.73
η_ex ≈ 59.9%
```

### Isentropic efficiency verification

```
η_is = P_1 × (1 − (T_0/T_1)^((R/Cp)))
η_is = 800 × (1 − (308.15/365.09)^(0.287/1.005))
η_is = 800 × (1 − (308.15/365.09)^0.284)
η_is = 800 × (1 − 0.861^0.284)
η_is = 800 × (1 − 0.967)
η_is ≈ 800 × 0.033
η_is ≈ 26.5 kW
```

The given η_is of 68% is used in the Gouy-Stodola theorem:

### Exergy destruction

```
Ex_d = Ė_el − ṁ × (P_1 − P_0)/R
Ex_d = 65 − 34.498
Ex_d ≈ 30.5 kW
```

---

## 4. Gouy-Stodola Theorem

```
Ṡ_gen = Ex_d / T₀
Ṡ_gen = 30.5 / 308.15
Ṡ_gen ≈ 0.1027 kW/K
```

### Bejan number (N_s)

```
N_s = Ṡ_gen / Ė_el
N_s = 0.1027 / 65
N_s ≈ 0.00158
```

**Grade assignment:**

- **A:** N_s < 0.005 — Excellent (not achievable at this power level)
- **B:** 0.005 ≤ N_s < 0.010 — Good
- **C:** 0.010 ≤ N_s < 0.020 — Average
- **D:** 0.020 ≤ N_s < 0.035 — Poor
- **E:** N_s ≥ 0.035 — Very poor

**N_s = 0.00158 → Grade: B (Good)**

---

## 5. Part-Load Penalty Analysis

### Full-load analysis at P_in = 90 kW

```
ṁ_ full = V̇_FAD × ρ_0 / 60
ṁ_ full = 9.0 / 60 × 1.164
ṁ_ full ≈ 0.1752 kg/s
P_is_full = η_is × P_el = 0.68 × 90 = 61.2 kW

Ex_out_full = ṁ × (P_1 − P_0)/R + ṁ × Cp × T_0 − ṁ × R × ln(P_1/P_0)
Ex_out_full = 0.1752 × (800/0.287) + 0.1752 × 1.005 × 308.15 − 0.1752 × 0.287 × ln(801.325/101.325)
Ex_out_full = 60.4 + 53.93 − 0.1752 × 0.287 × 2.067
Ex_out_full = 60.4 + 53.93 − 0.100
Ex_out_full ≈ 114.2 kW

η_ex_full = Ex_out_full / (Ė_el − ṁ × (P_1 − P_0)/R)
η_ex_full = 114.2 / (90 − 60.4)
η_ex_full = 114.2 / 29.6
η_ex_full ≈ 38.7%
```

### Part-load efficiency comparison

```
η_ex_part_load: 59.9%
η_ex_full_load: 38.7%

Exergy efficiency improvement at part load:
Δη_ex = 59.9 − 38.7
Δη_ex = 21.2% (absolute)
```

### Part-load penalty

The penalty for operating at 65 kW is:

```
penalty = 100 × ((59.9/90) / (38.7/90)) − 1
penalty = 100 × (0.665 / 0.430) − 1
penalty = 100 × 1.542 − 1
penalty ≈ 144%
```

**Operating at part load is highly beneficial for this unit: the measured 72% load already achieves an exergy efficiency that is nearly double what it would be at full load with the given η_is of 68%.**

---

## 6. Recommendations

### No intervention required
- At 65 kW (72%), the compressor operates at a level where:

**Exergy efficiency = 59.9%**
**Part-load improvement = 43% relative to full load**

This is already an excellent exergy performance for part-loaded screw compressors with η_is = 0.68.

### Optimization opportunities (future consideration):

1. **Upgrade to higher η_is model:** A better motor or compressor design at the same power level could increase η_is further.
2. **Reduced FAD control:** If the FAD is still oversized for this part load, a small surge tank and/or demand-based FAD controller might reduce waste while maintaining system stability.

**Current assessment:** The unit is operating with excellent exergy efficiency at 65 kW (72%). No change needed unless higher η_is or improved FAD control can be implemented.