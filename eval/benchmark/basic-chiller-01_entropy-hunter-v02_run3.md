# basic-chiller-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 51.9s | Checks: 4/4

## Exergy Analysis: Air-Cooled Screw Chiller (Full Load)

### Assumptions

1. Steady-state, steady-flow conditions.
2. Kinetic and potential exergy changes are negligible.
3. Compressor work is pure work (exergy = energy).
4. The chiller operates as a Carnot cycle for the cold side heat rejection: COP_ideal = T_cold/T_absorp.
5. Heat input to condenser from ambient air (cooling effect) is treated as waste exergy destruction at the environment temperature.
6. Refrigerant R-410A properties used internally, but all energy inputs/outputs are stated in terms of kW.
7. The chilled water system is modeled as a black box with 200 kW cooling delivered via a heat exchanger; the Carnot COP (cold-side) is calculated from the given actual COP.
8. Air-cooled condenser rejects heat to ambient at T₀ = 35°C.

---

### Step 1: Basic Energy Balance

#### Cooling Capacity
Q_cold = 200 kW

#### Condenser Heat Rejection
From energy balance on the chiller:
```
Q_condenser = Q_cold + W_comp
Q_condenser = 200 kW + 71.4 kW
Q_condenser = 271.4 kW
```

#### Compressor Power Input (Given)
W_comp = 71.4 kW

---

### Step 2: Carnot COP and Verification

The actual COP is given as:
```
COP_actual = Q_cold / W_comp
COP_actual = 200 kW / 71.4 kW
COP_actual ≈ 2.80 (already provided, confirms our inputs)
```

Using the Carnot formula for the chiller's cold-side COP:
```
COP_Carnot = T_cold / (T_cond - T_cold)
T_cold = 7°C → K = 254.15
T_cond = 35°C → K = 308.15

COP_Carnot = 254.15 / (308.15 − 254.15)
COP_Carnot ≈ 254.15 / 54
COP_Carnot ≈ 4.71
```

The **actual** COP of 2.8 is sub-Carnot, expected for a compression-based chiller with losses. Our analysis continues using these values.

---

### Step 3: Cold and Hot Reservoir Temperatures

Chilled water supply (T_cold):
```
T_cold = 7°C → T_cold = 254.15 K
```

Condenser air inlet temperature (T_cond) treated as the environment:
```
T_cond = 35°C → T_cond = 308.15 K
```

---

### Step 4: Carnot COP and Exergy Efficiency

Calculate the Carnot COP:
```
COP_Carnot = Q_cold / T_cold × (1/T_cond − 1/T_cold)
COP_Carnot = 254.15 / 308.15 × (1/308.15 - 1/254.15)
COP_Carnot = 254.15 / 308.15 × (-0.000976 + 0.00394)
COP_Carnot ≈ 254.15 / 308.15 × 0.00296
COP_Carnot ≈ 0.0794 or 7.94 kW/kW
```

Calculate the exergy efficiency (second-law efficiency):
```
η_ex = COP_actual / COP_Carnot
η_ex = 2.80 / 7.94
η_ex ≈ 0.3536 or 35.36%
```

---

### Step 5: Energy and Exergy Calculations

#### Total Heat Input (Fuel)
```
Q_fuel = Q_condenser = 271.4 kW
```

#### Thermal (Energy) Efficiency
```
η_th = Q_cold / Q_fuel
η_th = 200 kW / 271.4 kW
η_th ≈ 0.738 or 73.8%
```

#### Exergy of Fuel (Heat Input)
```
Ex_fuel = Q_fuel × (T_cond/T₀ − 1)
Ex_fuel = 271.4 kW × (308.15/35 + 1 - 1)
Ex_fuel = 271.4 kW × (8.804 + 1 - 1)
Ex_fuel = 271.4 kW × 8.804
Ex_fuel ≈ 2396.4 kW·K
```

#### Exergy of Cold Delivery
```
Ex_cold = Q_cold × (T_cold − T₀)/T₀
Ex_cold = 200 kW × (254.15/35 - 1)
Ex_cold = 200 kW × (7.261 - 1)
Ex_cold = 200 kW × 6.261
Ex_cold ≈ 1252.2 kW·K
```

#### Exergy of Waste Heat Rejected
```
Ex_waste = Q_condenser × (T_cond − T₀)/T₀
Ex_waste = 271.4 kW × (308.15/35 - 1)
Ex_waste = 271.4 kW × (8.804 - 1)
Ex_waste = 271.4 kW × 7.804
Ex_waste ≈ 2116.7 kW·K
```

#### Exergy Destruction (Second Law)
```
Ex_d = Q_cold × (T_cond/T₀ − T_cold/T₀) + W_comp
Ex_d = 200 kW × ((308.15/35 - 254.15/35))
Ex_d = 200 kW × (8.804 - 7.261)
Ex_d = 200 kW × 1.543
Ex_d ≈ 308.6 kW·K

Ex_d = Q_cold − Q_cold/η_th + W_comp
Ex_d = 200 − 200 / 0.738 + 71.4
Ex_d = 200 − 271.4 + 71.4
Ex_d = 99.6 kW·K

Ex_d = Q_cold × (T_cond/T₀ − T_cold/T₀) + W_comp
Ex_d = 200 × ((308.15/35 - 254.15/35)
Ex_d = 200 × (8.804 - 7.261)
Ex_d = 200 × 1.543
Ex_d ≈ 308.6 kW·K
```

---

### Step 6: Summary Table

| **Parameter**           | **Value**         |
|------------------------|------------------|
| Cooling capacity (Q_cold)| 200 kW           |
| Chilled water supply    | 7°C (254.15 K)   |
| Condenser air inlet     | 35°C (308.15 K)  |
| Compressor power        | 71.4 kW          |
| COP (actual)            | 2.8             |
| COP (Carnot)            | 4.71            |
| Energy efficiency       | 73.8%           |
| Exergy efficiency       | 35.4%           |
| Heat input (fuel)       | 271.4 kW         |
| Exergy of fuel          | 2,396.4 kW·K     |
| Exergy of cold delivery | 1,252.2 kW·K     |
| Exergy of waste heat    | 2,116.7 kW·K     |
| Exergy destruction      | 99.6 kW·K        |

---

### Step 7: Exergy Analysis Conclusions

**Overall assessment:** The chiller operates at a sub-Carnot COP (2.8) and achieves an exergy efficiency of **35.4%**.

**Energy waste:** The exergy destruction is relatively low compared to the thermal input (~99.6 kW·K / 271.4 kW = 0.367 or 36.7%), indicating that the compressor and internal irreversibilities are well managed for a screw chiller.

**Improvement potential:** The key area for improvement is increasing the COP through:
- Optimizing heat exchanger surface areas.
- Reducing pressure drops in the system (pump power, fouling).
- Improving motor efficiency or using variable-speed drives on compressor.
- Minimizing refrigerant charge to reduce internal subcooling/overheating.

Achieving a 10% improvement in COP would yield:
```
ΔCOP = 2.8 × 0.1 = 0.28 kW
Q_cold_new = Q_fuel / (COP + ΔCOP)
Q_cold_new = 271.4 / (2.8 + 0.28) 
Q_cold_new ≈ 95.3 kW

ΔQ_cold = 200 - 95.3 = 104.7 kW
```

A **COP improvement of 0.28** would increase the cooling capacity by ~52% (104.7 kW), while maintaining a COP above 3.0 for full-load efficiency.

---

### Step 8: Recommendations

1. **Compressor Optimization:** Ensure compressor is operating at near-best-efficiency-point (BEP) — check motor and gearbox alignment, oil pressure, and valve timing.
2. **Heat Exchanger Maintenance:** Regular inspection and cleaning of condenser and evaporator heat exchangers to minimize ΔT and reduce pressure drops.
3. **Refrigerant Management:** Check for refrigerant leaks; maintain appropriate charge level without excessive subcooling/overheating.
4. **Water Treatment:** Ensure chilled water system is free from fouling or corrosion — regular chemical treatment can improve heat transfer.
5. **Variable Speed Drive (VSD):** If not already installed, consider a VSD on the compressor for part-load efficiency improvements and reduced cycle frequency.

By addressing these areas, the chiller's exergy efficiency could approach 40-45%, significantly reducing operating costs while maintaining high cooling capacity.