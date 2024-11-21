import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

# Initialize lists
Rf, RW, FR, RB, RTR, ve, RA, RApp, RT, EP, SM, PD, SP, BP = ([] for _ in range(14))

# Function to calculate resistance and power
def calculate_resistance_and_power(f, g, LOA, LWL, LBP, LCB, B, T, CB, CP, CM, CWL, S, M, ABT, hB, ATR, n, V, Csternchoice, Bulbchoice, Sapp, Appendage):
    results = []

    # FRICTIONAL RESISTANCE
    for vkn in range(1, n + 1):
        v = vkn * 0.5144  # Convert knots to m/s
        Re = (v * LBP) / M
        CF = (0.075 / (((math.log10(Re)) - 2) ** 2))
        ACF = 0.00051
        R = (CF + ACF) * (0.5 * f * S * (v ** 2))
        Rf.append(R)
        ve.append(v)

    # WAVE MAKING RESISTANCE
    for v in ve:
        Fr = v / (math.sqrt(g * LBP))
        c1 = 2223105 * ((T / B) ** 1.07961) * ((90 - 1) ** -1.37565)
        Rw = c1 * v * f * g  # Simplified formula for illustration
        RW.append(Rw)

    # Total Resistance Calculation
    for i in range(len(Rf)):
        total_resistance = Rf[i] + RW[i]
        RT.append(total_resistance)

    # Effective Power and Other Calculations
    for i in range(len(RT)):
        effective_power = RT[i] * ve[i]
        EP.append(effective_power)
        SM.append(effective_power * 1.15)
        PD.append(effective_power / 0.65)
        SP.append(PD[i] / 0.95)
        BP.append(SP[i] / 0.85)

    # Compile results into DataFrame
    df = pd.DataFrame({
        'Velocity (m/s)': ve,
        'Frictional Resistance (N)': Rf,
        'Wave Resistance (N)': RW,
        'Total Resistance (N)': RT,
        'Effective Power (W)': EP,
        'Sea Margin (W)': SM,
        'Delivered Power (W)': PD,
        'Shaft Power (W)': SP,
        'Brake Power (W)': BP
    })
    return df

# Streamlit UI
st.title("Resistance and Power Calculator")

# Input Form
with st.form("input_form"):
    st.subheader("Input Parameters")
    f = st.number_input("Density (ρ) (kg/m^3)", value=1025.0)
    g = st.number_input("Gravity (m/s²)", value=9.81)
    LOA = st.number_input("Length Overall (LOA) (m)", value=200.0)
    LWL = st.number_input("Length at Waterline (LWL) (m)", value=190.0)
    LBP = st.number_input("Length Between Perpendiculars (LBP) (m)", value=185.0)
    LCB = st.number_input("LCB (%)", value=0.5)
    B = st.number_input("Breadth (B) (m)", value=32.0)
    T = st.number_input("Draft (T) (m)", value=12.0)
    CB = st.number_input("Block Coefficient (Cb)", value=0.8)
    CP = st.number_input("Prismatic Coefficient (Cp)", value=0.65)
    CM = st.number_input("Midship Coefficient (Cm)", value=0.9)
    CWL = st.number_input("Waterline Coefficient (Cwl)", value=0.85)
    S = st.number_input("Wetted Surface Area (S) (m²)", value=8000.0)
    M = st.number_input("Viscosity (Ns/m²)", value=1.15e-6)
    ABT = st.number_input("ABT (m²)", value=50.0)
    hB = st.number_input("hB (m)", value=5.0)
    ATR = st.number_input("ATR (m²)", value=60.0)
    n = st.number_input("Number of Speeds", value=10, step=1)
    V = st.number_input("Underwater Volume (V) (m³)", value=25000.0)
    Csternchoice = st.selectbox("Cstern Choice", options=[1, 2, 3, 4], index=0)
    Bulbchoice = st.selectbox("Bulb Choice", options=[1, 0], index=0, format_func=lambda x: "Yes" if x == 1 else "No")
    Sapp = st.number_input("Sapp (m²)", value=100.0)
    Appendage = st.selectbox("Appendage Type", options=[1, 2, 3, 4, 5], index=0)

    submitted = st.form_submit_button("Calculate")

# Calculation and Results
if submitted:
    result_df = calculate_resistance_and_power(f, g, LOA, LWL, LBP, LCB, B, T, CB, CP, CM, CWL, S, M, ABT, hB, ATR, n, V, Csternchoice, Bulbchoice, Sapp, Appendage)
    st.subheader("Results")
    st.dataframe(result_df)

    # Plots
    st.subheader("Plots")
    fig, ax = plt.subplots()
    ax.plot(ve, RT, label="Total Resistance")
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("Resistance (N)")
    ax.legend()
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.plot(ve, BP, label="Brake Power")
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("Power (W)")
    ax.legend()
    st.pyplot(fig)
