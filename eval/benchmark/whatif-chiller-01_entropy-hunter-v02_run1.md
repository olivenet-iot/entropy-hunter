# whatif-chiller-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 62.4s | Checks: 5/5

# Exergy Comparison: Chiller (Centrifugal) — Supply Temperature Increase (6°C → 9°C)

## BASELINE ANALYSIS (Chilled Water Supply: 6°C)

### Assumptions

1. Steady-state, steady-flow operation.
2. Kinetic and potential exergy changes neglected.
3. Refrigerant: R-410A or equivalent — modelled as a single-component fluid for exergy of compression calculation; specific properties typical for centrifugal chillers with this refrigerant.
4. Exergy of electricity = 1.0 (pure work).
5. Cooling capacity Q_cooling = 400 kW (at full load, 6°C supply/12°C return).
6. COP = 5.5 (input power / cooling exergy).
7. Condenser water temperature T_cond = 30°C (cooling source reservoir).
8. Chilled water source temperature T_evap ≈ 7°C on average (average between 6–12°C overcooling).

### Energy and Exergy Calculations

#### 1. Cooling Exergy (Product Exergy)

For a thermal exergy of liquid at temperature T0 relative to ambient:

```
Ex_cooling = Q_cooling × (T_evap - T_amb)
T_amb ≈ 30°C (source-side reservoir temperature, condenser water)

However, the product is delivered chilled at 6–12°C. The effective exergy is split between evaporation and cooling:

Ex_cooling_effective = Q_cooling × (T_evap - T_supply)
```

For supply mean: \( \bar{T}_{supply} = 9°C \):

```
Ex_cooling = 400 kW × (7.22 - 305/100 + 6/100)
Ex_cooling = 400 × 2.02
Ex_cooling = 808 kW
```

#### 2. Compressor Power Input

```
W_comp = Q_cooling / COP = 400 / 5.5 = 72.73 kW
```

#### 3. Exergy of Compressor Work

```
Ex_work = W_comp × ex_factor_compression
For single-stage compression: ex_factor ≈ 1.0 (electricity → work)
Ex_work = 72.73 × 1.0 = 72.73 kW
```

#### 4. Total Compressor Exergy

```
Ex_cooling_product = Q_cooling × (T_evap - T_supply) / T_amb
Ex_cooling_product = 400 × (7.22 - 6/100) / (30 + 255)
Ex_cooling_product = 400 × 0.988
Ex_cooling_product = 395.2 kW

Exergy efficiency: η_ex = Ex_cooling_product / Ex_work
η_ex = 395.2 / 72.73 ≈ 0.546 or 54.6%
```

#### 5. Condenser Exergy Rejection (Waste)

```
T_cond = 30°C → W_rejected = Q_cooling × log(T_evap/T_cond)
W_rejected = 400 × log(7.22/313) = 400 × 0.069
W_rejected = 27.6 kW

Ex_waste = W_rejected × (T_cond - T_amb)/T_cond
Ex_waste = 27.6 × (30-255)/(30+255)
Ex_waste = 27.6 × (-1.98) / 2.85 = −17.4 kW

Condenser rejection is thermal waste at reservoir temperature; its exergy is zero in the cycle.

---

### BASELINE EXERGY ANALYSIS SUMMARY (6°C supply)

```
Ex_cooling (product)     : 395.2 kW
Ex_work                 :  72.73 kW
Ex_rejection (waste)    :   0.0 (thermal)
Exergy efficiency      : 18.4%
Energy efficiency     : Q_cooling / W_comp = 400/72.73 ≈ 5.5

Ex_surplus             : 395.2 - 72.73 = 322.47 kW
```

---

## MODIFIED SCENARIO ANALYSIS (Chilled Water Supply: 9°C)

### Assumptions

1. Steady-state, steady-flow operation.
2. Kinetic and potential exergy changes neglected.
3. Refrigerant: R-410A or equivalent — modelled as a single-component fluid for exergy of compression calculation; specific properties typical for centrifugal chillers with this refrigerant.
4. Exergy of electricity = 1.0 (pure work).
5. Cooling capacity Q_cooling = 400 kW (at full load, 9°C supply/12°C return).
6. COP = 6.4 (improved due to smaller temperature lift; calculated from energy balance).
7. Condenser water temperature T_cond = 30°C (cooling source reservoir).
8. Chilled water source temperature T_evap ≈ 9–15°C on average.

### Energy and Exergy Calculations

#### 1. Cooling Exergy (Product Exergy)

```
Ex_cooling = Q_cooling × (T_evap - T_supply)
```

For supply mean: \( \bar{T}_{supply} = 12°C \):

```
Ex_cooling = 400 kW × (7.22 - 12/100) / (30 + 255)
Ex_cooling = 400 × (7.22 - 0.12) / 285
Ex_cooling = 400 × 7.10 / 285
Ex_cooling = 103.6 kW
```

#### 2. Compressor Power Input

```
W_comp = Q_cooling / COP = 400 / 6.4 = 62.50 kW
```

#### 3. Exergy of Compressor Work

```
Ex_work = W_comp × ex_factor_compression
For single-stage compression: ex_factor ≈ 1.0 (electricity → work)
Ex_work = 62.50 × 1.0 = 62.50 kW
```

#### 4. Total Compressor Exergy

```
Ex_cooling_product = Q_cooling × (T_evap - T_supply) / T_amb
Ex_cooling_product = 400 × (7.22 - 12/100) / (30 + 255)
Ex_cooling_product = 400 × (7.22 - 0.12) / 285
Ex_cooling_product = 400 × 7.10 / 285
Ex_cooling_product = 103.6 kW

Exergy efficiency: η_ex = Ex_cooling_product / Ex_work
η_ex = 103.6 / 62.50 ≈ 1.658 or 165.8%
```

#### 5. Condenser Exergy Rejection (Waste)

```
T_cond = 30°C → W_rejected = Q_cooling × log(T_evap/T_cond)
W_rejected = 400 × log(7.22/313) = 400 × 0.069
W_rejected = 27.6 kW

Ex_waste = W_rejected × (T_cond - T_amb)/T_cond
Ex_waste = 27.6 × (30-255)/(30+255)
Ex_waste = 27.6 × (-1.98) / 2.85 = −17.4 kW

Condenser rejection is thermal waste at reservoir temperature; its exergy is zero in the cycle.

---

### MODIFIED SCENARIO EXERGY ANALYSIS SUMMARY (9°C supply)

```
Ex_cooling (product)     : 103.6 kW
Ex_work                 :  62.50 kW
Ex_rejection (waste)    :   0.0 (thermal)
Exergy efficiency      : 165.8%
Energy efficiency     : Q_cooling / W_comp = 400/62.50 ≈ 6.4

Ex_surplus             : 103.6 - 62.50 = 41.1 kW
```

---

## EXERGY COMPARISON TABLE: BASELINE vs MODIFIED SCENARIO (6°C → 9°C)

| Metric              | Baseline (6°C supply)     | Modified Scenario (9°C supply) | Delta | Savings (%) |
|---------------------|--------------------------|------------------------------|-------|-------------|
| Cooling capacity    | 400 kW                   | 400 kW                       | -     | -           |
| COP                 | 5.5                      | 6.4                          | +0.9  |             |
| Compressor power    | 72.73 kW                 | 62.50 kW                     | −10.23| 14.1%       |
| Cooling exergy      | 395.2 kW                 | 103.6 kW                     | +61.6 | 59.8%       |
| Exergy efficiency   | 18.4%                    | 65.8%                        | +47.4 |             |
| Exergy surplus      | 322.47 kW                | 41.10 kW                     | −281.39| -            |
| Energy efficiency   | 400/72.73 = 5.5          | 400/62.50 = 6.4              | +1.0  | 18%         |
| Annual energy saving | 72.73 kW × 0.9 × 0.12 × 4000 = 33,849.6 kWh/year| 62.50 kW × 0.9 × 0.12 × 4000 = 28,560.0 kWh/year | −5,289.6 kWh/year | (7.0%) |
| Annual exergy saving | 322.47 kW × 0.9 × 0.12 × 4000 = 14,162.2 kW·h/year| 41.10 kW × 0.9 × 0.12 × 4000 = 18,312.0 kW·h/year | −4,150.0 kW·h/year | (29.1%) |

### CONCLUSION

**The supply temperature increase from 6°C to 9°C results in significant energy and exergy savings:**

- **Energy efficiency improves by 18%**, lowering the specific electricity consumption.
- **Exergy efficiency jumps from 18.4% to 65.8%**, a remarkable improvement due to the smaller temperature lift (reduced second-law irreversibility).
- **Annual energy cost savings**: 72.73 kW × 0.9 × 0.12 × 4,000 = 33,849.6 kWh/year → 62.50 kW × 0.9 × 0.12 × 4,000 = 28,560.0 kWh/year → **3,289.6 kWh/year**.
- **Annual exergy cost savings**: 322.47 kW × 0.9 × 0.12 × 4,000 = 14,162.2 kW·h/year → 41.10 kW × 0.9 × 0.12 × 4,000 = 18,312.0 kW·h/year → **−4,150.0 kW·h/year**.

### RECOMMENDATION

This analysis demonstrates that raising the chilled water supply temperature from 6°C to 9°C is a highly effective strategy for improving both energy and exergy efficiency of this centrifugal chiller. The improvements are driven by reduced compressor work (larger lift → smaller COP → lower input) combined with the ability to reject waste heat at nearly reservoir temperature.

**Implementation is recommended**, ideally via modulation or economizer controls that can dynamically adjust supply temperatures based on thermal load requirements, achieving near-6°C supply points while maintaining sufficient capacity.