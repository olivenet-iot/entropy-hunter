# egm-pump-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 48.7s | Checks: 4/6

## Entropy Generation Minimization Analysis: Centrifugal Cooling Water Pump

### Operating Conditions
- Volume flow rate, ṁ = 120 m³/h = 0.0333 m³/s
- Head, H = 25 m
- Motor electrical power input, P_elec = 12 kW
- Pump hydraulic efficiency, η_pump = 70%
- Motor efficiency, η_motor = 91%
- Fluid: liquid water at 28°C (incompressible)
- Operating condition: full load

---

### Step 1: Basic Calculations

**Mass flow rate of fluid:**
```
ρ = 996.0 kg/m³ (at 28°C, per IAPWS/IFRSpecification)
ṁ = ρ × Q̇
ṁ = 996.0 × 0.0333
ṁ = 33.17 kg/s
```

**Hydraulic power output:**
```
P_hyd = ṁ × g × H
P_hyd = 33.17 × 9.807 × 25
P_hyd = 8146.2 W = 8.15 kW
```

**Checking consistency with pump efficiency:**
```
Expected P_hyd (from η_pump) = P_elec / η_pump
Expected P_hyd = 12,000 / 0.70
Expected P_hyd = 17,143 W

Actual P_hyd = 8.15 kW = 8146 W (not consistent with expected value)
```

**Note:** There is a discrepancy between the calculated and expected hydraulic power. The motor electrical input of 12 kW cannot yield both stated conditions. We will use the given data as-is.

---

### Step 2: Efficiency Verification

Since P_hyd = 8.15 kW (from pump efficiency) and P_elec = 12 kW:

```
Actual η_pump = 8,146 / (12,000 × 0.70)
η_pump = 8,146 / 8,400
η_pump = 0.971 or 97.1%
```

The pump efficiency is higher than stated; we will use the given value of η_pump = 70% for consistency.

---

### Step 3: Electrical and Thermal Power

**Mechanical power delivered to fluid (useful work):**
```
P_useful = P_hyd / η_pump
P_useful = 8,146 / 0.70
P_useful = 11,637 W = 11.64 kW
```

**Electrical input:**
```
P_elec = 12 kW (given)
```

**Thermal power dissipation via motor losses:**
```
P_losses = P_elec - P_useful
P_losses = 12,000 - 8,146
P_losses = 3,854 W = 3.85 kW
```

---

### Step 4: Exergy Calculations

**Exergy of electrical power input:**
```
Ex_in = Ċ × T₀
Ex_in = 12,000 × (1 + 0.07)  # Carnot factor for exergy conversion from electricity at ~36°C
Ex_in = 12,000 × 1.07
Ex_in = 12,840 W = 12.84 kW
```

**Exergy of useful fluid power:**
```
Ex_hyd = ṁ × g × H × (1 + η_pump / (1 - η_pump))
Ex_hyd = 33.17 × 9.807 × 25 × (1 + 0.70 / 0.30)
Ex_hyd = 8,146.2 × (1 + 2.333)
Ex_hyd = 8,146.2 × 3.333
Ex_hyd = 27,152 W = 27.15 kW
```

**Exergy of motor losses (waste heat):**
```
Ex_loss = Q_loss × T₀ / T_source
T_source ≈ 40°C (motor case temperature)
Q_loss = P_losses = 3,854 W

Ex_loss = 3,854 × (1 + 0.07) / 313.15
Ex_loss = 3,854 × 1.07 / 313.15
Ex_loss = 4,129.78 / 313.15
Ex_loss = 13.19 W = 0.0132 kW
```

---

### Step 5: Total Exergy Balance

**Total exergy output (useful + losses):**
```
Ex_out = Ex_hyd + Ex_loss
Ex_out = 27,152 + 13.19
Ex_out = 27,165 W = 27.17 kW
```

**Exergy efficiency:**
```
η_ex = Ex_out / Ex_in
η_ex = 27,165 / 12,840
η_ex = 0.213 or 21.3%
```

---

### Step 6: Entropy Generation Rate and Bejan Number

**Total entropy generation rate (S_gen):**
```
Ṡ_gen = Q_gen / T₀
Q_gen = Ex_in - Ex_out
Q_gen = 12,840 - 27,165
Q_gen = -14,325 W  # This is a correction step; let's recalculate

Correcting: η_ex = 8.15 / 12.84
η_ex = 0.636 or 63.6%

Ex_out = 12,840 × 0.636
Ex_out = 8,172 W

Ṡ_gen = Q_gen / T₀
Q_gen = 12,840 - 8,172
Q_gen = 4,668 W

T₀ = 293.15 K (28°C)
Ṡ_gen = 4,668 / 293.15
Ṡ_gen = 15.90 kW/K
```

**Bejan number:**
```
N_s = Ṡ_gen / (Ex_in - Ex_out)
N_s = 0.016 / (12.840 - 8.172)
N_s = 0.016 / 4.668
N_s = 0.00343

Grade assignment: C (poor; > 2% of input exergy wasted)
```

---

### Step 7: Decomposition by Mechanism

**Mechanical power loss (irreversible):**
```
P_mech_loss = P_elec - P_hyd
P_mech_loss = 12,000 - 8,146
P_mech_loss = 3,854 W
```

**Mechanical exergy:**
```
Ex_mech = P_mech × (1 - η_pump)
Ex_mech = 3,854 × (1 - 0.70)
Ex_mech = 3,854 × 0.30
Ex_mech = 1,156 W
```

**Mechanical Bejan number:**
```
N_s,m = Ex_mech / (P_elec - P_hyd)
N_s,m = 1,156 / 3,854
N_s,m = 0.299 or 29.9%
```

**Heat loss exergy:**
```
Ex_loss = Q_loss × T₀ / T_source
Q_loss = 3,854 W (same as before)
T_source ≈ 40°C

Ex_loss = 3,854 × (1 + 0.07) / 313.15
Ex_loss = 3,854 × 1.07 / 313.15
Ex_loss = 4,129.78 / 313.15
Ex_loss = 13.19 W

N_s,h = Ex_loss / (P_elec - P_hyd)
N_s,h = 13.19 / 3,854
N_s,h = 0.00342 or 0.3%
```

---

### Step 8: Recommendations for Improvement

1. **Motor upgrade:** Replace the motor with a higher-efficiency model (e.g., IE3). Current motor at 91% is already good but could be replaced by an IE4 unit achieving ~95%.

2. **Pump reevaluation:** Confirm pump is correctly sized and operates within its best efficiency range (~60-80%). Consider a pump with higher hydraulic efficiency (e.g., above 73%).

3. **Fluid balance adjustments:** Review system for pressure losses; ensure valves and piping are appropriately sized.

4. **VFD implementation:** Install a variable frequency drive to operate the pump at part load (if not already done). This would allow significant improvement in efficiency across the operating range, especially at part-load conditions where inefficiencies are highest.

5. **Regular maintenance:** Ensure regular inspection of bearings, seals, and lubrication for minimal mechanical losses.

6. **Harmonic reduction:** Install harmonic dampers if flow pulsations or vibration issues are observed.

---

### Summary

- **Ṡ_gen = 0.016 kW/K**
- **N_s = 0.00343 (C — Poor)**
- **Improvement strategy: motor upgrade, pump optimization, VFD installation**

With a focus on motor and pump upgrades, the full-load efficiency can be significantly improved while reducing entropy generation at the same operating point.