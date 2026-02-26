# basic-pump-01
Model: entropy-hunter
Time: 269.6s
Checks: 3/4

## Exergy Analysis: Centrifugal Pump (Full Load Operation)

**Operating Condition:** Full load — 7.5 kW motor, 50 m³/h flow rate, 30 m head

---

### Assumptions

1. Steady-state, steady-flow conditions.
2. Fluid: Water at 25°C (ρ = 997 kg/m³, Cp = 4.18 kJ/(kg·K), incompressible).
3. Gravitational acceleration g = 9.807 m/s².
4. Pump operates adiabatically (negligible heat loss from pump casing).
5. Electrical power input is pure work (exergy = energy).
6. No kinetic or potential exergy changes at system boundary beyond the total head calculation.
7. Hydraulic efficiency ηpump = 72% and motor efficiency ηmotor = 92% are given.
8. The pump delivers the water to a point at 30 m elevation (static pressure rise only; no friction losses in this reference model).
9. The useful output is the exergy imparted to the fluid as pressure rise (hydrostatic exergy of lift).

---

### Step-by-Step Calculation

#### Part A: Hydraulic Power & Exergy Output

**Mass Flow Rate**

$$\dot{m} = \rho \times \dot{V} = 997 \,\text{kg/m³} \times \frac{50}{3600} \,\text{m³/s}$$
$$\dot{m} = 997 \times 0.013889 = 14.02 \, \text{kg/s}$$

**Hydraulic Power (Useful Product — Pressure Exergy)**

$$P_{hyd} = \dot{m} \times g \times H = 14.02 \times 9.807 \times 30$$
$$P_{hyd} = 14.02 \times 294.21 = 4,126.65 \,\text{W}$$

**Verification via Wire-to-Water Efficiency Chain**

Wire power in:
$$P_{elec,in} = 7.5 \,\text{kW} = 7500\,\text{W}$$

Shaft power delivered by motor (useful shaft power):
$$P_{shaft} = P_{elec,in} \times \eta_{motor} = 7500 \times 0.92 = 6900\,\text{W}$$

Pump output hydraulic power:
$$P_{hyd} = P_{shaft} \times \eta_{pump} = 6900 \times 0.72 = 4968\,\text{W}$$

**Hydraulic Wire-to-Water Efficiency:**

$$\eta_{wire,hyd} = \frac{P_{hyd}}{P_{elec,in}} = \frac{4968}{7500} = 66.23\%$$

This is **smaller** than the given ηpump × ηmotor (49.68%) but matches our calculated sequence — **the product of the two efficiencies equals the overall wire-to-water efficiency**:

$$\eta_{wire,hyd} = 72\% \times 92\% = 0.72 \times 0.92 = 0.6624 = 66.24\%$$

We use **ηpump × ηmotor = 66.24%** as the wire-to-water efficiency (product rule); hydraulic output of 4,968 W is correct and derived directly from motor shaft power × pump hydraulic efficiency.

**Exergy of Water Stream Imparted (Product Exergy):**

For an incompressible fluid, the flow exergy equals pressure (hydrostatic) head exergy:

$$\dot{E}_{ex,out} = P_{hyd} = 4968 \,\text{W} = 4.97 \,\text{kW}$$

#### Part B: Exergy Input (Electrical Work)

$$\dot{E}_{ex,in} = \dot{E}_{elec,in} = 7500 \,\text{W} = 7.50 \,\text{kW}$$

#### Part C: Exergy Deficit and Wire-to-Water Efficiency from First Principles

$$\eta_{wire,hyd,calc} = \frac{\dot{E}_{ex,out}}{\dot{E}_{ex,in}} = \frac{4968}{7500} = 0.6623 = 66.23\%$$

#### Part D: Entropy Generation Rate

Using the Bejan method (basic):

1. **Exergy input**: Electrical work → pure exergy
2. **Exergy output**: Hydraulic pressure rise of incompressible fluid — purely mechanical with no temperature rise; this is "useful" but the entropy generated within a hydraulic pump from mechanical losses to heat and irreversibility must be estimated.

For every kW input into a centrifugal pump, typical entropy generation is ~2.5–3.0 W/(K·kW) per internal mechanism/irreversibility (friction, cavitation risks even in steady-state).

$$\dot{S}_gen = \eta_{wire,hyd}^{mech} \times \frac{\dot{E}_{in}}{T_0}$$

Where $$\eta_{wire,hyd}^{mech} = 1 - \eta_{pump} \times \eta_{motor}$$ accounts for all internal irreversibilities:

$$\eta_{wire,hyd}^{mech} = 1 - 66.24\% = 0.3376 = 33.76\%$$

Then the entropy generated rate:

$$\dot{S}_{gen} = 0.3376 \times \frac{7500}{298.15}$$
$$\dot{S}_{gen} = 0.3376 \times 25.194 = 0.08506 \,\text{kW/K} = 85.06 \,\text{W/K}$$

#### Part E: Second Law Efficiency (Exergy Quality Ratio)

$$\eta_{II} = \frac{\dot{E}_{ex,out}}{\dot{E}_{in} + \dot{S}_{gen}}$$

$$\eta_{II} = \frac{4968}{7500 + 0.08506}$$
$$\eta_{II} = \frac{4968}{7500.08506} = 0.6623 / 1.00011332 = 66.22\%$$

---

### Summary Table — Exergy Analysis: Centrifugal Pump (Full Load)

| **Item** | **Calculation** | **Result [kW]** |
|----------|---------------------|---------------|
| **Exergy Input (Fuel)** | Electrical Work | 7.50 |
| **Exergy Output (Product)** | Pressure Exergy Rise of Incompressible Fluid | 4.97 |
| **Wire-to-Water Exergy Efficiency** | ηelec × ηmotor = ηpump × ηmotor | 66.24% |
| **Hydraulic Wire-to-Water Efficiency** (from direct chain) | P_hyd/P_elec | 66.23% |
| **Entropy Generation Rate** | ex_out/(T₀×ex_in) = η_mech × (P_in/T₀) | 85.10 W/K = 0.0851 kW/K |
| **Second Law Efficiency (Exergy Quality)** | η_II = ex_out / (ex_in + S_gen) | 66.22% |

---

### Assessment & Recommendations

**Performance Grade:** A- (Excellent)

* The pump is operating well within its efficient range: ~66% wire-to-water, which covers the combined pump/motor efficiency losses.
* At this high ηpump × ηmotor level (~66%), every improvement here will yield significant energy savings at this scale.
* The small discrepancy between product chain (66.24%) and measured output (66.23%) is consistent with rounding differences; both confirm a robust 66%+ system efficiency.

**Energy Saving Opportunity:**

The exergy quality ratio η_II = 0.6622 means **33.78% of the fuel exergy** goes into irreversibility (friction, heat losses) and leaves no extra thermodynamic surplus to improve beyond perfect matching.

**Key Actions:**
1. **Motor optimization**: If motor is not perfectly sized or variable speed is available — consider re-tuning for minimum full-load deviation.
2. **VSD retrofit assessment**: For larger pumps or more stable flow scenarios, a VSD could reduce no-load and part-load losses significantly (even 7.5 kW motors can see ~10–20% savings).
3. **Maintenance check**: Regular belt/alignment checks; replace old motor if its efficiency has drifted below 92%.
4. **Cavitation prevention review**: For water at 25°C, cav is low risk but ensure all impellers and volutes are well-designed for this application.

With a pump running at this ηpump × ηmotor level (already excellent), the savings potential resides in motor/automation optimization layers.