import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Civil Engineering Tool - Beam Analyzer")

# Input parameters
st.header("Beam Parameters")
L = st.number_input("Beam Length (m)", min_value=1.0, value=6.0)
E = st.number_input("Modulus of Elasticity (Pa)", min_value=1e7, value=200e9)
I = st.number_input("Moment of Inertia (m^4)", min_value=1e-9, value=8.1e-6)

st.header("Point Load")
load_pos = st.number_input("Load Position (m)", min_value=0.0, max_value=L, value=3.0)
load_mag = st.number_input("Load Magnitude (N, negative is downward)", value=-10000.0)

if st.button("Analyze Beam"):
    # Structural analysis
    def analyze_beam(length, point_loads):
        x = np.linspace(0, length, 500)
        V = np.zeros_like(x)
        M = np.zeros_like(x)

        total_moment = sum(-load['magnitude'] * (length - load['position']) for load in point_loads)
        R1 = total_moment / length
        R2 = sum(load['magnitude'] for load in point_loads) - R1

        for load in point_loads:
            P = load['magnitude']
            a = load['position']
            for i, xi in enumerate(x):
                if xi < a:
                    V[i] += R1
                    M[i] += R1 * xi
                else:
                    V[i] += R1 + P
                    M[i] += R1 * xi + P * (xi - a)
            V -= R2
            M -= R2 * x
        return x, V, M, R1, R2

    loads = [{'position': load_pos, 'magnitude': load_mag}]
    x, shear, moment, R1, R2 = analyze_beam(L, loads)

    st.subheader("Support Reactions")
    st.write(f"Left Support (R1): {R1:.2f} N")
    st.write(f"Right Support (R2): {R2:.2f} N")

    st.subheader("Maximum Bending Moment")
    st.write(f"Max Moment: {max(moment):.2f} Nm")

    st.subheader("Shear Force Diagram")
    fig_v, ax_v = plt.subplots()
    ax_v.plot(x, shear)
    ax_v.set_title("Shear Force Diagram")
    ax_v.set_xlabel("Beam Length (m)")
    ax_v.set_ylabel("Shear Force (N)")
    ax_v.grid(True)
    st.pyplot(fig_v)

    st.subheader("Bending Moment Diagram")
    fig_m, ax_m = plt.subplots()
    ax_m.plot(x, moment)
    ax_m.set_title("Bending Moment Diagram")
    ax_m.set_xlabel("Beam Length (m)")
    ax_m.set_ylabel("Moment (Nm)")
    ax_m.grid(True)
    st.pyplot(fig_m)
