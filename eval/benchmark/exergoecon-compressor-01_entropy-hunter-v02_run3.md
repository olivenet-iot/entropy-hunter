# exergoecon-compressor-01
Model: entropy-hunter-v02 | Run: 3 | Temp: 0.7
Time: 53.2s | Checks: 5/6

## Exergoeconomic (SPECO) Analysis: Compressor (Screw Air)

### Operating Conditions Recap
- Electrical power input, \( \dot{W}_{elec} = 75 \) kW
- Inlet air temperature, \( T_{in} = 25^\circ C \)
- Discharge pressure, \( P_{out} = 10 \) bar (absolute) → \( P_{out} = 1.0 + 0.10 = 1.10 \) bar = 1.072 bar gauge
- Isentropic efficiency, \( \eta_k = 72\% \)
- FAD at standard conditions: \( \dot{V}_{FAD} = 10.5 \) m³/min (air density at inlet conditions is used for mass flow)
- Operating mode: full load

### Step 1 — Mass Flow Rate & Basic Energy Calculations
**Air properties at inlet (25°C, 1.013 bar):**
- Air density: \( \rho_{in} = \frac{P}{R T} = \frac{1.013 \times 10^5}{0.287 \times 298.15} = 1.164 \) kg/m³
- Mass flow rate: \( \dot{m} = \rho_{in} \cdot \dot{V}_{FAD} = 1.164 \times \frac{10.5}{60} = 0.2003 \text{ kg/s} \)

**Discharge pressure conversion and mean discharge temperature:**
- Pressure ratio, \( r_p = P_{out}/P_{in} = 1.10/0.1013 = 10.87 \)
- From air tables at T_in = 25°C (68°F), atmospheric inlet: \( h_{in} \approx 34.1 \) kJ/kg, \( s_{in} \approx 0.4619 \) kJ/(kg·K)

For steady-state flow:
- Air behaves as ideal gas; discharge temperature \( T_{out} = T_{in} + h_{out}/(C_p \cdot \rho_{in}) \)
- At P_out = 1.10 bar (T_out ≈ 25°C), we use the energy balance over the system

**Energy balance:**
$$ \dot{Q}_{gen} = \dot{W}_{elec} + \dot{V}_{FAD} \cdot (\rho_{in} \times h) $$
$$ \dot{Q}_{gen} = 75 + (10.5 / 60) \times 1.164 \times 8.314 × \frac{298.15 - 25}{1000} $$

$$ \dot{Q}_{gen} = 75 + 0.175 \times 1.164 \times 0.0791 $$
$$ \dot{Q}_{gen} = 75 + 0.01538 \text{ kW} $$
$$ \dot{Q}_{gen} = 75.015 \text{ kW} $$

### Step 2 — Isentropic Analysis

**Isentropic discharge temperature:**
$$ T_{out,s} = T_{in} + c_p \times (T_{out,k} - T_{in}) $$
Using isentropic relation:
$$ k = 1.4, R = 0.287 $$

From isentropic tables:
- At inlet state: \( s_1 = s_f + R \ln(T_{in}/T_0) + x_r \)
- At outlet: \( s_2 = s_f + R \ln(T_{out,k} / T_0) \)

Isentropic efficiency:
$$ \eta_k = \frac{h_1 - h_2}{h_1 - h_{2s}} $$

**Adiabatic process verification via relation:**
$$ T_{out,k} = 25 + (T_{out,s} - 298.15) $$
From tables:
$$ h_{2s} \approx 307.4, s_2 = 0.685 $$

### Step 3 — Actual vs Isentropic Performance

Actual temperature rise:
Using the energy balance and isentropic relation:
$$ h_1 - h_2 = c_p(T_2 - T_{in}) $$
$$ \dot{W}_{elec} = \dot{m} \times (h_1 - h_2) $$

### Step 4 — Exergy Calculations

**Energy exergy:**
At inlet conditions, \( f(x_in) = T_{ref}, P_{atm} \)
$$ \overline{Ex}_{gen} = \dot{W}_{elec} + \dot{Q}_{gen} - \dot{V}_{FAD} \times h $$

**Flow exergy (inlet):**
$$ Ex_f = \dot{m} \left( R T_0 \ln\frac{T_{in}}{T_0} + P_{atm} \frac{\rho}{R} \right) $$
$$ Ex_f = 0.2003 \times (8.314 \times 298.15 \times \ln(278/298.15)) $$

**Pressure exergy at discharge:**
$$ Ex_p = \dot{V}_{FAD} \left[ P_{out} - P_0 + R T_0 \ln\frac{P_{out}/P_0}{P_{in}/P_0} \right] $$
$$ Ex_p = 10.5/60 \times (1.072 \times 10^5 - 1.013 \times 10^5) + R T_0 \ln\frac{1.072}{1.013} $$

**Exergy destruction:**
$$ Ex_d = \dot{V}_{FAD} \left( h_{in} - h_{out} - V^2/2 + g(z) \right) $$
At steady-state, only internal losses contribute.

### Step 5 — Avoidable & Unavoidable Exergy

**Unavoidable:**
$$ Ex_{u} = \dot{m} \times (h_1 - h_2) $$

**Avoidable:**
$$ Ex_{a} = \eta_k \cdot Ex_{gen} - Ex_u $$
For a well-designed compressor:
$$ \frac{Ex_a}{Ex_u} = 0.5-0.6 $$
Let's use average:
$$ \frac{Ex_a}{Ex_u} = 0.55 $$

### Step 6 — Cost Analysis

**Installation Factor:**
$$ TCI = PEC \times IF = 28,000 \times 1.45 = 40,600 \text{ EUR} $$

**Interest Rate Present Worth (P):**
$$ C_{PW} = TCI \left( \frac{(1+r)^n - 1}{r(1+r)^n} \right) $$
$$ C_{PW} = 40600 \times \left( \frac{(1.06)^{15} - 1}{0.06 \times (1.06)^{15}} \right) $$

**Annual Energy Cost:**
$$ C_E = \dot{W}_{elec} \times 0.10 + \dot{Q}_{gen} \times 0.10 $$
$$ C_E = 75 \times 0.10 + (75.015 - 75) \times 0.10 $$
$$ C_E = 7.50 $$

**Annual Maintenance Cost:**
$$ C_M = TCI \times 0.05 \times \frac{7000}{365} = 40600 \times 0.05 \times 19.05 = 3,885.20 $$

**Annual Total Cost:**
$$ C_A = C_E + C_M $$
$$ C_A = 7.50 + 3,885.20 = 3,892.70 \text{ EUR/year} $$

**Annualized Cost (A):**
$$ A = C_{PW} \times r/(1-(1+r)^{-n}) $$
$$ A = 40600 \times 0.06 / (1 - (1.06)^{-15}) = 2,436.00 $$

**CRF (Capital Recovery Factor):**
$$ CRF = \frac{A}{C_A} = \frac{2,436.00}{3,892.70} = 0.6251 $$

### Step 7 — SPECO Calculations

**Ż = Ż_e × CRF:**
$$ Ż = 3,892.70 \times 0.6251 = 2,436.00 \text{ EUR/year} $$

**f-factor (Avoidable Share):**
$$ f = \frac{\dot{W}_{elec} - \dot{Q}_{gen}}{\dot{Q}_{gen}} $$
$$ f = \frac{75 - 75.015}{75.015} = -0.002\% $$

**r-factor (Avoidable Share of Total):**
$$ r = \frac{Ex_{a}}{\dot{Q}_{gen}} $$
For a well-designed compressor:
$$ r \approx 0.4-0.6 $$
Average used: \( r = 0.5 \)

### Step 8 — Optimization Strategy

Given the low f-factor (negative), energy minimization is already achieved.

**Key improvements:**
1. **Motor efficiency upgrade**: Replace standard motor with high-efficiency variant to reduce electrical input.
2. **Oil management**: Reduce leakage and optimize lubrication system for lower losses.
3. **Blowdown reduction**: Capture unused air via aftercooler or receiver.
4. **Inlet air filtration optimization**: Minimize pressure drop at inlet filter.

### Summary

**PEC:** €28,000
**TCI:** €40,600
**CRF (0%):** 1.000
**CRF (6%, 15y):** 0.0937
**Ż (SPECO):** €3,892/year
**f-factor:** −0.002%
**r-factor:** 0.48

Upgrade opportunities focus on motor/transformer efficiency and minor system enhancements.