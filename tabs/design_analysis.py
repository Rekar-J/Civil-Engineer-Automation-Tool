import streamlit as st
import pandas as pd
import numpy as np
from core import Beam
from plots import plot_beam_diagram, plot_sfd, plot_bmd

# --- Enhanced Structural Analysis Section (existing) ---
def run_structural_analysis():
    st.header("Structural Analysis")
    # ... your existing Structural Analysis code here ...

# --- Geotechnical Analysis Section ---
def run_geotechnical_analysis():
    st.header("Geotechnical Analysis")
    # ... existing code ...

# --- Hydraulic and Hydrological Modeling Section ---
def run_hydraulic_analysis():
    st.header("Hydraulic and Hydrological Modeling")
    # ... existing code ...

# --- Engineering Tests Section ---
def run_tests():
    st.header("Engineering Tests")
    # ... existing code ...

# --- New Beam Analysis Sub‑Tab ---
def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Analyze simply supported beams with point loads and UDLs.")

    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, key="beam_len")
    # Supports (must be 2 for now)
    st.write("#### Supports")
    supports = []
    for i in range(2):
        pos = st.number_input(
            f"Support #{i+1} Position (m)",
            min_value=0.0, max_value=length,
            value=(0.0 if i == 0 else length),
            key=f"beam_sup_pos_{i}"
        )
        sup_type = st.selectbox(
            f"Support #{i+1} Type",
            ["pin", "roller"],
            key=f"beam_sup_type_{i}"
        )
        supports.append({"pos": pos, "type": sup_type})

    # Point loads
    st.write("#### Point Loads")
    point_loads = []
    n_pl = st.number_input("How many point loads?", min_value=0, value=0, step=1, key="beam_pl_num")
    for i in range(int(n_pl)):
        pos = st.number_input(
            f"Load #{i+1} Position (m)",
            min_value=0.0, max_value=length,
            value=length / 2,
            key=f"beam_pl_pos_{i}"
        )
        mag = st.number_input(
            f"Load #{i+1} Magnitude (kN)",
            value=10.0,
            key=f"beam_pl_mag_{i}"
        )
        point_loads.append({"pos": pos, "mag": mag})

    # UDLs
    st.write("#### Uniformly Distributed Loads")
    udls = []
    n_udl = st.number_input("How many UDLs?", min_value=0, value=0, step=1, key="beam_udl_num")
    for i in range(int(n_udl)):
        start = st.number_input(
            f"UDL #{i+1} Start (m)",
            min_value=0.0, max_value=length,
            value=0.0,
            key=f"beam_udl_start_{i}"
        )
        end = st.number_input(
            f"UDL #{i+1} End (m)",
            min_value=0.0, max_value=length,
            value=length,
            key=f"beam_udl_end_{i}"
        )
        intensity = st.number_input(
            f"UDL #{i+1} Intensity (kN/m)",
            value=5.0,
            key=f"beam_udl_int_{i}"
        )
        udls.append({"start": start, "end": end, "int": intensity})

    # Build and solve
    beam = Beam(length)
    for sup in supports:
        beam.add_support(sup["pos"], sup["type"])
    for pl in point_loads:
        beam.add_point_load(pl["pos"], pl["mag"])
    for ud in udls:
        beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

    if st.button("🔎 Analyze Beam", key="analyze_beam"):
        beam.analyze()
        st.write("#### Support Reactions")
        for i, R in enumerate(beam.reactions):
            st.write(f"> Support #{i+1} at {supports[i]['pos']} m → **{R:.2f} kN**")

        xs = np.linspace(0, beam.length, 200)
        max_M = max(abs(beam.moment_at(x)) for x in xs)
        st.write(f"#### Maximum Bending Moment: **{max_M:.2f} kN·m**")

        st.write("#### Beam Schematic")
        st.pyplot(plot_beam_diagram(beam))

        st.write("#### Shear Force Diagram")
        st.pyplot(plot_sfd(beam))

        st.write("#### Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))

# --- Combined Tabs for Design & Analysis ---
def run():
    st.title("🛠️ Design and Analysis")
    tabs = st.tabs([
        "Structural Analysis",
        "Beam Analysis",
        "Geotechnical Analysis",
        "Hydraulic and Hydrological Modeling",
        "Tests"
    ])
    with tabs[0]:
        run_structural_analysis()
    with tabs[1]:
        run_beam_analysis()
    with tabs[2]:
        run_geotechnical_analysis()
    with tabs[3]:
        run_hydraulic_analysis()
    with tabs[4]:
        run_tests()
