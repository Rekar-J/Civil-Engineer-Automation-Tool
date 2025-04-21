import streamlit as st
import pandas as pd
import numpy as np
from core import Beam
from plots import plot_beam_diagram, plot_sfd, plot_bmd

# --- Structural Analysis (unchanged) ---
def run_structural_analysis():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info(
        "This tool evaluates loads acting on a structure and performs advanced calculations "
        "including bending moment analysis and load combination assessments, in accordance with ACI standards."
    )
    # ... your existing code ...

# --- Geotechnical Analysis (unchanged) ---
def run_geotechnical_analysis():
    st.header("Geotechnical Analysis")
    # ... existing code ...

# --- Hydraulic & Hydrological Modeling (unchanged) ---
def run_hydraulic_analysis():
    st.header("Hydraulic and Hydrological Modeling")
    # ... existing code ...

# --- Engineering Tests (unchanged) ---
def run_tests():
    st.header("Engineering Tests")
    # ... existing code ...

# --- Beam Analysis Sub‑Tab ---
def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Analyze simply supported beams with point loads and UDLs.")

    # 1) Point load direction
    direction = st.radio(
        "Point Loads Direction",
        ["Downward", "Upward"],
        index=0,
        key="beam_load_dir"
    )
    load_dir_flag = "down" if direction == "Downward" else "up"

    # 2) Show dimensions?
    show_dims = st.checkbox("Show dimensions on schematic", value=True, key="beam_show_dims")

    # Beam span
    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, key="beam_len")

    # Supports (exactly two)
    st.write("#### Supports (exactly two)")
    supports = []
    for i in range(2):
        pos = st.number_input(
            f"Support #{i+1} Position (m)",
            min_value=0.0,
            max_value=length,
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
            min_value=0.0,
            max_value=length,
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
            min_value=0.0,
            max_value=length,
            value=0.0,
            key=f"beam_udl_start_{i}"
        )
        end = st.number_input(
            f"UDL #{i+1} End (m)",
            min_value=0.0,
            max_value=length,
            value=length,
            key=f"beam_udl_end_{i}"
        )
        intensity = st.number_input(
            f"UDL #{i+1} Intensity (kN/m)",
            value=5.0,
            key=f"beam_udl_int_{i}"
        )
        udls.append({"start": start, "end": end, "int": intensity})

    # Build & solve
    beam = Beam(length)
    for sup in supports:
        beam.add_support(sup["pos"], sup["type"])
    for pl in point_loads:
        beam.add_point_load(pl["pos"], pl["mag"])
    for ud in udls:
        beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

    if st.button("🔎 Analyze Beam", key="analyze_beam"):
        beam.analyze()

        # Reactions
        st.write("#### Support Reactions")
        for i, R in enumerate(beam.reactions):
            st.write(f"> Support #{i+1} at {supports[i]['pos']:.2f} m → **{R:.2f} kN**")

        # Maximum moment
        xs = np.linspace(0, beam.length, 200)
        max_M = max(abs(beam.moment_at(x)) for x in xs)
        st.write(f"#### Maximum Bending Moment: **{max_M:.2f} kN·m**")

        # Diagrams
        st.write("#### Beam Schematic")
        st.pyplot(plot_beam_diagram(
            beam,
            load_dir=load_dir_flag,
            show_dimensions=show_dims
        ))
        st.write("#### Shear Force Diagram")
        st.pyplot(plot_sfd(beam))
        st.write("#### Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))

        # Short commentary
        st.write("#### Analysis Summary")
        st.write(
            f"The {length:.2f} m span beam, supported at {supports[0]['pos']:.2f} m and "
            f"{supports[1]['pos']:.2f} m, carries point loads "
            f"{[pl['mag'] for pl in point_loads]} kN "
            f"acting {'downward' if direction=='Downward' else 'upward'} and UDLs "
            f"{[(ud['int'], ud['start'], ud['end']) for ud in udls]} kN/m. "
            "Shear and moment diagrams show internal force distributions and highlight "
            "where critical sections occur."
        )

# --- Combine all tabs ---
def run():
    st.title("🛠️ Design and Analysis")
    tabs = st.tabs([
        "Structural Analysis",
        "Beam Analysis",
        "Geotechnical Analysis",
        "Hydraulic & Hydrological",
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
