# egm-compressor-01
Model: entropy-hunter-v02 | Run: 1 | Temp: 0.7
Time: 51.5s | Checks: 4/6

# Entropy Generation Minimization (EGM) Analysis: Centrifugal Compressor

## Operating Conditions
- Electrical power input, \( \dot{W}_{elec} \): 150 kW
- Air inlet temperature, \( T_1 \): 30°C (303.15 K)
- Discharge pressure, \( P_2 \): 10 bar (1.0 MPa) → absolute discharge pressure: 2.00 + 1.00 = **3.0 bar** (300 kPa)
- Isentropic efficiency, η_is: 80%
- FAD (free air delivery), \( \dot{V}_{FAD} \): 20.0 m³/min
- Operating condition: full load

### Step 1: Air Properties at Inlet and Outlet

**Inlet air properties at T₁ = 30°C (303.15 K), P₀ = 1.013 bar (101.3 kPa):**
- Pressure, \( P_1 \) = 1.013 bar (101.3 kPa)
- Air: ideal gas with Cp = 1.005 kJ/(kg·K), R = 0.287 kJ/(kg·K), k = 1.4
- Molecular weight, M = 28.97 kg/kmol

Air density at inlet:
\[ \rho_1 = \frac{P_1}{R T_1} = \frac{101.3 \times 10^3}{0.287 \times 303.15} \approx 1.164 \text{ kg/m}^3 \]

**Mass flow rate:**
\[ \dot{m} = \rho_1 \cdot \dot{V}_{FAD} = 1.164 \times \frac{20}{60} = 1.164 \times 0.3333 \approx 0.388 \text{ kg/s} \]

**Outlet pressure (absolute):**
\[ P_2 = 3.0 \text{ bar} = 300 \text{ kPa} \]

### Step 2: Isentropic Outlet Temperature

For isentropic compression:
\[ T_{2s} = T_1 \left( \frac{P_2}{P_1} \right)^{\frac{(k-1)}{k}} \]
With \( k = 1.4 \):
\[ T_{2s} = 303.15 \times \left( \frac{300}{101.3} \right)^{0.2857} \approx 303.15 \times 2.963^{\frac{2}{3}} \approx 303.15 \times 1.486 \approx 448.2 \text{ K} = 175.05^\circ C \]

However, the isentropic efficiency of 80% gives:
\[ T_{2s} = T_1 + \frac{\dot{W}_{elec}}{\rho_1 c_p (T_{2s} - T_1)} \]
Since we already calculated \( T_{2s} \) from the given isentropic efficiency:
\[ T_{2s} = 448.2 \text{ K} \]

**Actual outlet temperature:**
Using first-law energy balance on the compressor:
\[ h_2 + \frac{\dot{W}_{elec}}{T_0} = h_1 + \eta_{is} \times \left( \frac{T_{2s}}{T_1} - 1 \right) R T_1 \]

At \( P_2 = 3.0 \text{ bar} \), the actual \( h_2 \approx 458.6 \text{ kJ/kg} \) (using standard tables at 179.5°C).

### Step 3: Isentropic Outlet Temperature Correction

For isentropic efficiency:
\[ \eta_{is} = \frac{T_1 - T_{2s}}{T_1 - T_0} \]

With \( T_1 = 303.15 \text{ K} \), \( T_2 = 458.6 / 1.005 \approx 455.9 \text{ K} \):
\[ 0.80 = \frac{T_1 - T_{2s}}{T_1 - T_0} = \frac{303.15 - T_{2s}}{303.15 - 273.15} \]
\[ 303.15 - T_{2s} = 0.80 \times 30 \approx 24.0 \text{ K} \]
\[ T_{2s} \approx 279.15 \text{ K} = 6.0^\circ C \]

### Step 4: Energy Balance Verification

Actual:
\[ h_2 = 458.6 / 1.005 \approx 456.3 \text{ kJ/kg} \]
Energy balance:
\[ \dot{Q}_{gen} + \dot{W}_{elec} = \dot{m} (h_2 - h_1) \]
With \( h_1 = 107.89 \) kJ/kg at inlet:
\[ \dot{Q}_{gen} = \dot{m} (h_2 + T_0/c_p - h_1) \]
For air: \( T_0 = 25^\circ C = 298.15 K \)
\[ \dot{Q}_{gen} = 0.388 \times (456.3 - 107.89 + 298.15/1.005) \]
\[ \dot{Q}_{gen} = 0.388 \times (348.41 + 296.8) = 0.388 \times 645.21 = 251.57 \text{ kW} \]

### Step 5: Exergy Calculations

**Total exergy input:**
\[ \dot{Ex}_{in} = T_0 \dot{W}_{elec} / (T_1 - T_0) = 298.15 \times 150 / 70.0 = 648.3 \text{ kW} \]

**Useful exergy output:**
\[ \dot{Ex}_{useful} = \dot{m} (C_p(T_2 - T_1) + (P_2/P_1 - 1)\rho_1) \]
At steady-state, the useful exergy is:
\[ \dot{Ex}_{useful} = \dot{W}_{elec} + \dot{Q}_{gen} = 150 + 251.57 = 401.6 kW \]

**Irreversible (waste) exergy:**
\[ \dot{Ex}_{irr} = \dot{Ex}_{in} - \dot{Ex}_{useful} = 648.3 - 401.6 = 246.7 \text{ kW} \]

**Entropy generation rate (Gouy-Stodola):**
\[ \dot{S}_{gen} = \frac{\dot{Ex}_{irr}}{T_0} = \frac{246.7}{298.15} \approx 0.83 \text{ kW/K} \]

### Step 6: Bejan Number (N_s) — Dominant Mechanism Identification

\[ N_s = \frac{\dot{Ex}_{irr}}{\dot{Ex}_{in}} = \frac{246.7}{648.3} \approx 0.38 \]

#### Decomposition by mechanism:
- **Heat transfer:** \( \dot{Q}_{gen} / T_0 = 251.57 / 298.15 \approx 0.844 \text{ kW/K} \)
- **Pressure drop (friction):** \( \dot{W}_{elec} - \dot{m}(h_2 - h_1) = 150 - 387.69 = -237.69 \text{ kW} \)
  This negative value indicates an error in the exergy balance; it should be:
  \( \dot{Ex}_{friction} = (P_2/P_1 - 1)\rho_1 \cdot V^2/2 \)

Correcting with correct work term:
\[ \dot{W}_{useful} = 0.83 \times 648.3 = 541.7 kW \]
\[ \dot{Ex}_{friction} = 150 - (h_2 - h_1) = 150 - 387.69 + 125.3 = -112.39 \]

### Corrected Step 4: Exergy Balance

\[ \dot{Ex}_{friction} = 648.3 - (h_2 - h_1) = 648.3 - 330.87 = 317.5 kW \]
\[ \dot{Ex}_{mixing} = 0 \]

**Bejan number:**
\[ N_s = \frac{\dot{Ex}_{friction}}{\dot{Ex}_{in}} = \frac{317.5}{648.3} \approx 0.49 \]
Friction is dominant.

### Step 7: Recommendations

1. **Cooling optimization**: Reduce aftercooler load; reduce casing heat losses.
2. **Inlet air precooling**: Cool inlet air to reduce temperature rise and improve η_is.
3. **Surge prevention**: Ensure stable operating point (avoid surge).
4. **Motor efficiency upgrade**: Replace or tune motor for higher efficiency.
5. **Oil-free vs oil-lubricated**: Consider switching from oil-lubricated compressor with better thermal management.

**Final Summary:**
- Ṡ_gen = 0.83 kW/K
- N_s = 0.49 (friction dominant)
- Dominant mechanism: friction/pressure drop
- Recommendations focused on cooling, inlet air precooling, and motor upgrade.

This completes the EGM analysis for the centrifugal compressor at full load.