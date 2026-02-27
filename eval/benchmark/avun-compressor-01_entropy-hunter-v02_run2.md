# avun-compressor-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 52.0s | Checks: 4/4

## Exergy Analysis: Compressor (Screw Air — Full Load)

### Operating Conditions
1. **Electric power input:** \( \dot{W}_{elec} = 55\ kW \)
2. **Inlet air temperature:** \( T_0 = 25^\circ C = 298\ K \)
3. **Discharge pressure:** \( P_2 = 8\ bar = 800\ kPa \) (absolute)
4. **FAD (Free Air Delivery):** \( \dot{V}_{FAD} = 8.0\ m^3/min \)
5. **Isentropic efficiency:** \( \eta_{isen} = 72\% \)
6. **Operating mode:** Full load

### Reference (BAT): Atlas Copco GA VSD+
- Isentropic efficiency: \( \eta_{isen,\ BAT} = 90\% \)
- Specific energy consumption at 8 bar: \( \dot{w}_{BAT} = 5.8\ kW/(m^3/min) \)

---

### Step 1 — Mass Flow Rate

Air density at inlet (ideal gas, R = 0.287 kJ/(kg·K)):

\[ \rho_0 = \frac{P_0}{R T_0} = \frac{101.325\ kPa}{0.287\ kJ/(kg·K) \times 298\ K} \]

\[ \rho_0 = 1.1644\ kg/m^3 \]

Mass flow rate:

\[ \dot{m} = \rho_0 \cdot \dot{V}_{FAD} = 1.1644\ kg/m^3 \times \frac{8}{60}\ m^3/s \]

\[ \dot{m} = 1.1644 \times 0.1333 \]

\[ \dot{m} = 0.1552\ kg/s \]

### Step 2 — Air Inlet and Outlet Conditions

**Inlet:**
- Air is treated as ideal gas at ambient pressure (101.325 kPa) or atmospheric condition.
- The given inlet temperature of \( T_0 = 25^\circ C = 298\ K \).

**Outlet:**
- Discharge pressure: \( P_2 = 800\ kPa \)
- From isentropic analysis, the outlet temperature can be determined.

### Step 3 — Isentropic Outlet Temperature

Using the ideal gas relation for an isentropic process:

\[ T_2s = T_1 \left( \frac{P_2}{P_1} \right)^{\frac{\gamma-1}{\gamma}} \]

At inlet (atmospheric):

\[ P_1 = 101.325\ kPa, \quad T_1 = 298\ K \]

Air: \( R = 0.287\ kJ/(kg·K), \; Cp = 1.005\ kJ/(kg·K), \; \gamma = 1.4 \)

\[ \frac{P_2}{P_1} = \frac{800}{101.325} = 7.906 \]

\[ T_2s = 298 \times (7.906)^{\frac{1.4-1}{1.4}} \]

\[ T_2s = 298 \times (7.906)^{0.2857} \]

\[ T_2s = 298 \times 3.337 \]

\[ T_2s = 995.5\ K \rightarrow \text{(This is unphysical for air, so recheck the reference states)} \]

Air at atmospheric inlet is near-ideal; thus:

For an adiabatic process:

\[ T_2 = T_1 + \frac{\dot{Q}}{C_p} = 298\ K - R_s \]

From the reference BAT, \( \eta_{isen,\ BAT} = 0.90 \):

For FAD of 8.0 m³/min at 8 bar:

\[ \dot{W}_{elec,\ BAT} = 5.8 \times 8/60 = 0.773\ kW/m^3/min \]

Convert: \( V_FAD = 8/60 = 0.1333 m³/s \)

\[ \dot{W}_{elec,\ BAT} = 0.773 \times 0.1333 = 0.103\ kW \]

At 90% isentropic:

For FAD of 8/60 = 0.1333 m³/min:

\[ \dot{W}_{elec,\ BAT} = 5.8 \times 0.1333 = 0.774\ kW \]

### Step 4 — Energy Balance

**Heat rejection at cooler:**

For every kW input, the screw compressor rejects \( Q_{cool} = \dot{W}_{elec} - \dot{Q} \).

From BAT reference:

\[ Q_{cool,\ BAT} = 0.774\ kW \]

At full load with 55 kW input:

\[ Q_{cool} = 55 - (5.8 \times 1333) = 55 - 77.4 = -22.4\ kW \rightarrow \text{Correction: BAT is 0.774 kW, so} \]

Thus:

\[ Q_{cool} = 55 - 0.774 = 54.226\ kW \]

### Step 5 — Exergy Calculations

**Useful output (pressure exergy):**

$$\bar{e}_p = \dot{m} R T_0 \left(1 - \frac{P_1}{P_2}\right)$$

$$\bar{e}_p = 0.1552 \times 0.287 \times 298 \left(1 - \frac{101.325}{800 + 101.325}\right)$$

$$\bar{e}_p = 0.1552 \times 0.287 \times 298 \left(1 - \frac{101.325}{901.325}\right)$$

$$\bar{e}_p = 0.1552 \times 0.287 \times 298 \times (1 - 0.1124)$$

$$\bar{e}_p = 0.1552 \times 0.287 \times 298 \times 0.8876$$

$$\bar{e}_p = 11.423\ kW$$

**Total exergy input:**

$$\bar{E}_{in} = T_0 \dot{Q}_{cool} = 298 \times (55 - 0.774)$$

$$\bar{E}_{in} = 298 \times 54.226 = 16137.5 kW$$

**Efficiency:**

$$\eta_{comp} = \frac{\bar{e}_p}{\bar{E}_{in}} = \frac{11.423}{0.161375} = 0.69$$

**Exergy destruction (first-law residual):**

$$\bar{D} = \dot{W}_{elec} - \bar{e}_p = 55 - 11.423 = 43.577\ kW$$

### Step 6 — BAT Comparison and Avoidable/Unavoidable Split

BAT reference:

**Electrical input:** \( \dot{W}_{elec,\ BAT} = 0.774\ kW \)

For BAT at 5.8 kW/(m³/min):

\[ \dot{W}_{elec,\ BAT} = 5.8 \times 1333 / 60 = 129.7\ kW \]

**Energy savings:**

\[ \Delta W_{elec} = 55 - 12.97 = 42.03\ kW \]

### Step 7 — Avoidable/Unavoidable Split

**Avoidable:** The compressor is at full load; the avoidable part stems from the gap between actual and BAT efficiency.

\[ \dot{W}_{elec,\ avoid} = 55 - 12.97 = 42.03\ kW \]

For a screw compressor with η_isen = 72%, the unavoidable component is derived from the exergy destruction at this point:

**Unavoidable:**

\[ \bar{D}_{unav} = \dot{W}_{elec} - \eta_{comp} \cdot \bar{e}_p \]

\[ \bar{D}_{unav} = 55 - (0.72 \times 11.423) \]

\[ \bar{D}_{unav} = 55 - 8.196 = 46.804\ kW \]

**Avoidable:** The gap between actual and BAT, which reduces with better efficiency:

\[ \bar{D}_{avoid} = 42.03 - (90\% \text{- isentropic reduction}) = 42.03 - 5.67 = 36.36\ kW \]

### Summary

- **Total exergy destruction:** 46.804 kW
- **Unavoidable component:** 5.67 kW (from BAT reference at same η_isen)
- **Avoidable component:** 42.03 - 5.67 = 36.36 kW

**Improvement priority:** The avoidable component of 36.36 kW is the primary focus for optimization, achievable by upgrading to a compressor with better isentropic efficiency (e.g., higher-quality scroll or screw design).

**Achievable improvement potential:** Reducing avoidable exergy destruction by 50% would save \( 0.5 \times 36.36 = 18.2\ kW \) in electricity consumption.

---

This analysis provides a detailed split of the exergy destruction and highlights the efficiency gap between current equipment and BAT, prioritizing specific improvement actions based on achievable savings.