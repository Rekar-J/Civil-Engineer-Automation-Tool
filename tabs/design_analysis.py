# tabs/design_analysis.py

import streamlit as st
import numpy as np
import pandas as pd

from core import Beam
from plots import plot_sfd, plot_bmd

# --- Beam Analysis Section ---
def run_beam_analysis():
    st.header("📐 Beam Analysis")

    # Beam length
    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0)

    # Supports
    st.subheader("Supports")
    num_supports = st.number_input(
        "How many supports?", min_value=0, max_value=3, value=2, step=1
    )
    supports = []
    for i in range(int(num_supports)):
        pos = st.number_input(
            f"Support #{i+1} position (m)",
            min_value=0.0,
            max_value=length,
            value=0.0 if i == 0 else length,
            key=f"beam_sup_pos_{i}",
        )
        sup_type = st.selectbox(
            f"Support #{i+1} type",
            ["pin", "roller"],
            key=f"beam_sup_type_{i}"
        )
        supports.append({"pos": pos, "type": sup_type})

    # Point Loads
    st.subheader("Point Loads")
    num_pl = st.number_input("Number of point loads", min_value=0, value=0, step=1)
    point_loads = []
    for i in range(int(num_pl)):
        pos = st.number_input(
            f"Load #{i+1} position (m)",
            min_value=0.0,
            max_value=length,
            value=length / 2,
            key=f"beam_pl_pos_{i}"
        )
        mag = st.number_input(
            f"Load #{i+1} magnitude (kN)",
            value=10.0,
            key=f"beam_pl_mag_{i}"
        )
        point_loads.append({"pos": pos, "mag": mag})

    # UDLs
    st.subheader("Uniformly Distributed Loads")
    num_udl = st.number_input("Number of UDLs", min_value=0, value=0, step=1)
    udls = []
    for i in range(int(num_udl)):
        start = st.number_input(
            f"UDL #{i+1} start (m)",
            min_value=0.0, max_value=length,
            value=0.0,
            key=f"beam_udl_start_{i}"
        )
        end = st.number_input(
            f"UDL #{i+1} end (m)",
            min_value=0.0, max_value=length,
            value=length,
            key=f"beam_udl_end_{i}"
        )
        intensity = st.number_input(
            f"UDL #{i+1} intensity (kN/m)",
            value=5.0,
            key=f"beam_udl_int_{i}"
        )
        udls.append({"start": start, "end": end, "int": intensity})

    # Build & solve
    if st.button("🔎 Analyze Beam"):
        beam = Beam(length, supports=[], loads=[])
        for sup in supports:
            beam.add_support(sup["pos"], sup["type"])
        for pl in point_loads:
            beam.add_point_load(pl["pos"], pl["mag"])
        for ud in udls:
            beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

        beam.analyze()

        # Reactions
        st.subheader("Support Reactions")
        reactions = beam.reactions
        df_react = pd.DataFrame([
            {"Position (m)": supports[i]["pos"], "Reaction (kN)": r}
            for i, r in enumerate(reactions)
        ])
        st.table(df_react)

        # Maximum moment
        xs = np.linspace(0, beam.length, 200)
        max_M = max(abs(beam.moment_at(x)) for x in xs)
        st.write(f"**Maximum Bending Moment:** {max_M:.2f} kN·m")

        # Diagrams
        st.subheader("Shear Force Diagram")
        st.pyplot(plot_sfd(beam))
        st.subheader("Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))


# --- Enhanced Structural Analysis Section (unchanged) ---
def run_structural_analysis():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info(
        "This tool evaluates loads acting on a structure and performs advanced calculations "
        "including bending moment analysis and load combination assessments, in accordance with ACI standards."
    )
    # ... (rest of your existing structural‐analysis code)


# --- Geotechnical, Hydraulic & Tests sections (unchanged) ---
def run_geotechnical_analysis():
    # ... your existing code

    pass  # keep your original implementation here


def run_hydraulic_analysis():
    # ... your existing code

    pass


def run_tests():
    # ... your existing code

    pass


# --- Main entrypoint for this tab ---
def run():
    st.title("🛠️ Design and Analysis")
    tabs = st.tabs([
        "Beam Analysis",
        "Structural Analysis",
        "Geotechnical Analysis",
        "Hydraulic & Hydrological",
        "Lab Tests"
    ])

    with tabs[0]:
        run_beam_analysis()
    with tabs[1]:
        run_structural_analysis()
    with tabs[2]:
        run_geotechnical_analysis()
    with tabs[3]:
        run_hydraulic_analysis()
    with tabs[4]:
        run_tests()
