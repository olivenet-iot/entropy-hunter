# egm-compressor-01
Model: entropy-hunter-v02 | Run: 2 | Temp: 0.7
Time: 42.3s | Checks: 3/6

## EGM Analysis: Centrifugal Compressor (Full Load)

### Operating Conditions
- Electrical power input, $\dot W_{elec}$: 150 kW
- Inlet air temperature, $T_{in}$: 30°C (303.15 K)
- Discharge pressure, $P_{out}$: 10 bar = 1000 kPa
- Isentropic efficiency, η_is: 80% (= 0.80)
- FAD at inlet conditions, $\dot V_{FAD,in}$: 20.0 m³/min (0.333 m³/s)
- Operating condition: full_load

### Step 1: Air Properties and Inlet Conditions

**Air density at inlet ($T_{in} = 30^\circ\text{C}$, $P_0 = 101.325$ kPa):**
$$
\rho_{in} = \frac{P_0}{R \cdot T_{in}} = \frac{101.325\,\text{kPa}}{(0.287\,\text{kJ/(kg·K)})(303.15\,\text{K})}
$$
$$
\rho_{in} = 1.1645\,\text{kg/m}^3
$$

**Mass flow rate:**
$$
\dot{m}_{air} = \rho_{in} \cdot \dot V_{FAD,in} = 1.1645\,\text{kg/m}^3 \times 0.333\,\text{m}^3/\text{s}
$$
$$
\dot{m}_{air} = 0.3882\,\text{kg/s}
$$

### Step 2: Isentropic Outlet Temperature Calculation

From energy balance on the isentropic compressor:
$$
\dot W_{elec} = \dot m_{air} \cdot (C_p(T_2 - T_1)) + \frac{\eta_{is}}{1-\eta_{is}} \cdot \dot Q_{gen}
$$

At steady-state, energy added by heat $\dot Q_{gen}$ is negligible for a compressor with a small temperature rise. Thus:
$$
\dot W_{elec} = \dot m_{air} \cdot C_p(T_2 - T_1)
$$
where $C_p$ (air Cp at 30°C) ≈ 1.020 kJ/(kg·K).

From isentropic efficiency:
$$
\eta_{is} = \frac{\text{Isentropic power}}{\text{Actual power}} = \frac{\dot W_{elec}}{\dot m_{air} \cdot C_p(T_2 - T_1)}
$$

### Step 3: Air Properties at Discharge (Reconstructed)

At $P_2 = 10$ bar:
$$
T_2 = T_1 + \frac{R \times T_1}{C_p} \left( \frac{P_2}{P_{in}} - 1 \right)
$$

**Inlet pressure (atmospheric):**
$$
P_{in} = P_0 = 101.325\,\text{kPa}
$$

**Isentropic discharge temperature:**
For air, $k=1.4$; using the isentropic relation:
$$
T_2^{(is)} = T_1 \left( \frac{P_2}{P_{in}} \right)^{\frac{k-1}{k}}
$$

$$
T_2^{(is)} = 303.15\,\text{K} \times (10)^\left(\frac{1.4 - 1}{1.4}\right)
$$
$$
T_2^{(is)} = 303.15 \times (10)^{0.2857}
$$
$$
T_2^{(is)} = 303.15\,\text{K} \times 1.9864
$$
$$
T_2^{(is)} = 602.9\,\text{K}
$$

**Actual (measured) outlet temperature:**
From energy balance:
$$
C_p(T_2 - T_1) = \frac{\dot W_{elec}}{\dot m_{air}}
$$
$$
T_2 = T_1 + \frac{\dot W_{elec}}{\dot m_{air} \cdot C_p}
$$

Using the isentropic efficiency:
$$
\eta_{is} = 0.80 \Rightarrow T_2 = T_1 + \frac{\dot W_{elec}}{0.3882 \times 1.020}
$$
$$
T_2 = 303.15 + \frac{150}{0.40}
$$
$$
T_2 = 303.15 + 375.0
$$
$$
T_2 = 678.15\,\text{K} \quad (\text{thermal})
$$

**Revised T2:**
This temperature is physically impossible for a compressor with an inlet of 30°C. The error arises from neglecting the small temperature rise in the actual process. A more accurate approach would use the given η_is and FAD to calculate T2 directly.

**Corrected T2 (from energy balance):**
$$
\dot W_{elec} = \dot m_{air} \cdot C_p(T_2 - T_1)
$$

$$
T_2 = T_1 + \frac{\dot W_{elec}}{\dot m_{air} \cdot C_p}
$$

### Step 4: Actual Power and Isentropic Analysis

**Actual power (including losses):**
From η_is:
$$
\eta_{is} = \frac{\text{Isentropic power}}{\dot W_{elec}}
$$
$$
\text{Isentropic power} = \frac{\eta_{is} \cdot \dot W_{elec}}{\eta_{is}} = 150\,\text{kW}
$$

**Actual isentropic outlet temperature (from η_is):**
$$
T_2^{(s)} = T_1 + \frac{T_2 - T_1}{\eta_{is}}
$$

### Step 5: Entropy Generation Calculation

**Isentropic flow exergy:**
$$
\text{Ex}_f^{(is)} = \int \frac{\dot V}{T_0} (T - T_0) + P\left(\frac{P}{P_0} - 1\right)\,dV
$$

**Actual flow exergy:**
$$
\text{Ex}_f = \int \frac{\dot V}{T_0} (T - T_0) + P\left(\frac{P}{P_0} - 1\right)\,dV
$$

### Step 6: Exergy Balance and Entropy Generation

**Exergy of electricity input:**
$$
\text{Ex}_{in} = \dot W_{elec}
$$

**Exergy of air product at inlet conditions:**
$$
\text{Ex}_a^{in} = C_p(T_1 - T_0) + P_0\left(\frac{\dot V}{T_0}\right)
$$

**Isentropic exergy change:**
$$
\Delta \text{Ex}^{(is)}_{comp} = \text{Ex}_a^{out(is)} - \text{Ex}_f^{in}
$$

**Actual exergy product (using FAD):**

### Step 7: Gouy-Stodola Theorem and Bejan Number

**Gouy-Stodola theorem:**
$$
\dot S_{gen} = \dot Q_{gen} - \frac{\dot W_{elec}}{T_0}
$$

**Bejan number (N_s):**
$$
N_s = \frac{\dot S_{gen}}{\dot Q_{gen}}
$$

### Step 8: Decomposition by Mechanism

- Friction (isentropic)
- Heat transfer (cooling losses)
- Mixing/pressure drop (fidelity)

### Step 9: Recommendations

1. **Increase isentropic efficiency:** Replace worn bearings, ensure correct blade design.
2. **Reduce pressure drop:** Clean compressor inlet and outlet piping; check for fouling.
3. **Cooling optimization:** Improve air cooler efficiency to reduce overheating losses.

---

**Detailed numerical results and mechanism decomposition will follow based on step-by-step calculations.**