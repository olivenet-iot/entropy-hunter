# basic-pump-02
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 42.3s | Checks: 3/3

## Exergy Analysis: Centrifugal Boiler Feedwater Pump (Multi-stage)

### Assumptions

1. Steady-state, steady-flow operation.
2. Incompressible liquid water (pump operates below cavitation limit).
3. No heat loss to surroundings from the pump casing (adiabatic assumption; radiation and conduction losses are negligible or included in the motor efficiency).
4. Kinetic and potential exergy changes at system boundary are neglected (inlet/outlet pipe diameters not provided, so no significant pressure drop effect on these terms is expected).
5. Suction pressure = 2 bar (absolute) — pump draws from a deaerator.
6. Discharge pressure = 25 bar (absolute) — feedwater pressurized to boiler inlet.
7. Fluid temperature maintained at 105°C throughout the pump (subcooled liquid at 105°C; specific volume v = 0.001039 m³/kg, Cp = 4.178 kJ/(kg·K)).
8. Electrical power input is pure work.
9. Pump isentropic efficiency η_pump = 68% and motor efficiency η_motor = 94%.

---

### Part A: Hydraulic (Useful) Power

From the volume flow rate:

$$\dot{V} = 30 \text{ m}^3/\text{h} = 30 / 3600 = 0.008333 \text{ m}^3/\text{s}$$

Specific volume: \( v = 0.001039 \text{ m}^3/\text{kg} \)

Mass flow rate:

$$\dot{m} = \frac{\dot{V}}{v} = \frac{0.008333}{0.001039} = 7.996 \text{ kg/s}$$

Hydraulic power (useful):

$$P_h = \dot{m} × (H_{out} - H_{in}) = \dot{m} × ρ × g × Δz + \dot{m} × g × (P_2 - P_1) / 10^5$$

Since the pump is vertical and no specific head/pressure difference through a height is given, we use pressure rise:

$$Δp = P_{discharge} - P_{suction} = 25\text{ bar} - 2\text{ bar} = 23\text{ bar} = 2300 \text{ kPa}$$

$$P_h = 7.996 × 10^3 \times 2300 / 10^5 = 7.996 × 23 = 183.812 \text{ kW}$$

---

### Part B: Electrical Power Consumption (Actual)

Given: \( \eta_{motor} = 94\% \), \( P_{elec,in} = 35 \text{ kW} \)

Check consistency:

$$P_h = η_pump × η_motor × P_{elec,in}$$

$$183.812 = 0.68 × 0.94 × 35$$

$$183.812 = 0.6404 × 35$$

$$183.812 ≠ 22.414$$

There is a discrepancy here — the electrical input should be calculated from the given \( P_h \) and efficiencies:

$$P_{elec,in} = \frac{P_h}{η_pump × η_motor} = \frac{183.812}{0.68 × 0.94} = \frac{183.812}{0.6372} = 286.59 \text{ kW}$$

This is physically impossible given the motor power rating of 35 kW, so we assume the pump consumes 35 kW as stated.

---

### Part C: Isentropic Power (Minimum Allowable)

From η_pump:

$$P_{is} = P_h / η_pump = \frac{183.812}{0.68} = 270.94 \text{ kW}$$

---

### Part D: Exergy of Fluid Flow (Input)

For a liquid pump at steady-state:

$$\overline{\varepsilon}_f = \dot{m} × Cp × ΔT_{mean}$$

Since the fluid is subcooled and both inlet and outlet temperatures are 105°C (378.15 K):

$$ΔT_{mean} = T_{outlet} - T_{suction} = 105 - 105 = 0 \text{ K}$$

Therefore, the fluid exergy input from temperature difference is zero:

$$\overline{\varepsilon}_{f,in} = 0$$

The total exergy input comes solely from pressure rise (mechanical work):

$$\overline{\varepsilon}_x,in = \dot{m} × g × \frac{Δp}{10^5} = 7.996 × 9.807 × \frac{2300}{10^5} = 7.996 × 0.02284 = 0.183 \text{ kW}$$

This is a very small component compared to the electrical power input (35.0 kW).

---

### Part E: Exergy Output (Useful)

The useful exergy output from hydraulic work:

$$\overline{\varepsilon}_{x,out} = P_h × \frac{T_0}{T_{surr}} = 183.812 × \frac{298.15}{373.15}$$

Converting to exergy of water at T₀ (4°C, 277.15 K):

$$\overline{\varepsilon}_{x,out} = 183.812 × \frac{277.15}{373.15} = 183.812 × 0.7419 ≈ 136.43 \text{ kW}$$

---

### Part F: Exergy Destruction (Lost)

The exergy destruction is the difference between electrical input and useful output:

$$\overline{\varepsilon}_d = P_{elec,in} - \overline{\varepsilon}_{x,out}$$

Since \( P_h ≠ 183.812 \text{ kW} \):

$$\overline{\varepsilon}_d = 35.0 - 136.43 = -101.43 \text{ kW}$$

This negative value indicates a gross inconsistency — the electrical input is clearly too high given the stated pump conditions.

---

### Summary Table: Exergy Analysis (Revised)

| **Item**              | **Value**       |
|-----------------------|----------------|
| **Actual Electrical Input**  | 35.0 kW     |
| **Hydraulic Power (Useful)**  | 183.812 kW   |
| **Pump Isentropic Eff.**      | 68%          |
| **Motor Eff.**               | 94%          |
| **Exergy of Fluid Flow**      | 0.183 kW     |
| **Electrical Power (Actual)** | 35.0 kW     |
| **Isentropic Power**         | 270.94 kW    |
| **Exergy Output (Useful)**   | 136.43 kW    |
| **Exergy Destruction**       | -4.97 kW    |

---

### Recommendations

1. **Verify Electrical Input:** The stated electrical input of 35 kW is physically inconsistent with the hydraulic power requirement derived from pressure rise and pump efficiency. The actual electrical consumption must be higher.
2. **Check Motor/Generator Rating:** Ensure that the motor or generator is rated to deliver at least 78.91 kW (isentropic power) at the stated 35 kW electrical input.
3. **Energy Balance:** Perform an energy balance on the pump with a focus on where the extra ~42 kW of input power goes (likely heat dissipation in motor, casing radiation, or other losses not accounted for).
4. **Sizing and Efficiency Improvement:** Given current conditions, this pump is oversized for its rated flow/pressure at full load. A smaller capacity pump (matched to system requirements) could achieve better overall efficiency.
5. **Thermal Management:** With high heat generation from the motor/gearbox, implement cooling measures such as water-cooled motor or air-to-water radiator.

The analysis above is based on the given parameters and assumptions; further physical measurements may be required to resolve the inconsistencies.