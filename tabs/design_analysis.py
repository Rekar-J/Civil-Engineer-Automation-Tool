# tabs/design_analysis.py

import streamlit as st
import pandas as pd
import numpy as np
from core import Beam
from plots import plot_beam_diagram, plot_sfd, plot_bmd

# --- (Your existing Structural, Geo, Hydro & Tests code stays the same) ---
def run_structural_analysis():
    st.header("Structural Analysis")
    # … your code …

def run_geotechnical_analysis():
    st.header("Geotechnical Analysis")
    # … your code …

def run_hydraulic_analysis():
    st.header("Hydraulic and Hydrological Modeling")
    # … your code …

def run_tests():
    st.header("Engineering Tests")
    # … your code …

# --- Beam Analysis Sub‑Tab ---
def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Analyze simply supported beams with point loads and UDLs.")

    # 1. Beam length
    length = st.number_input(
        "Beam Length (m)",
        min_value=0.1,
        value=5.0,
        key="beam_len"
    )

    # 2. Supports (two‑support beam)
    st.write("#### Supports (distance from **left end** in meters)")
    supports = []
    for i in range(2):
        pos = st.number_input(
            f"Support #{i+1} distance from left end (m)",
            min_value=0.0,
            max_value=length,
            value=(0.0 if i == 0 else length),
            key=f"beam_sup_pos_{i}"
        )
        sup_type = st.selectbox(
            f"Support #{i+1} type",
            ["pin", "roller"],
            key=f"beam_sup_type_{i}"
        )
        supports.append({"pos": pos, "type": sup_type})

    # 3. Point loads
    st.write("#### Point Loads (distance from **left end** in meters)")
    point_loads = []
    n_pl = st.number_input(
        "Number of point loads",
        min_value=0,
        value=0,
        step=1,
        key="beam_pl_num"
    )
    for i in range(int(n_pl)):
        pos = st.number_input(
            f"Point load #{i+1} distance from left end (m)",
            min_value=0.0,
            max_value=length,
            value=length / 2,
            key=f"beam_pl_pos_{i}"
        )
        mag = st.number_input(
            f"Point load #{i+1} magnitude (kN)",
            value=10.0,
            key=f"beam_pl_mag_{i}"
        )
        point_loads.append({"pos": pos, "mag": mag})

    # 4. Uniformly distributed loads
    st.write("#### Uniformly Distributed Loads (UDLs)")
    udls = []
    n_udl = st.number_input(
        "Number of UDLs",
        min_value=0,
        value=0,
        step=1,
        key="beam_udl_num"
    )
    for i in range(int(n_udl)):
        start = st.number_input(
            f"UDL #{i+1} start (m from left end)",
            min_value=0.0,
            max_value=length,
            value=0.0,
            key=f"beam_udl_start_{i}"
        )
        end = st.number_input(
            f"UDL #{i+1} end (m from left end)",
            min_value=0.0,
            max_value=length,
            value=length,
            key=f"beam_udl_end_{i}"
        )
        intensity = st.number_input(
            f"UDL #{i+1} intensity (kN/m)",
            value=5.0,
            key=f"beam_udl_int_{i}"
        )
        udls.append({"start": start, "end": end, "int": intensity})

    # 5. Build Beam object
    beam = Beam(length)
    for sup in supports:
        beam.add_support(sup["pos"], sup["type"])
    for pl in point_loads:
        beam.add_point_load(pl["pos"], pl["mag"])
    for ud in udls:
        beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

    # 6. Analyze on demand
    if st.button("🔎 Analyze Beam", key="analyze_beam"):
        beam.analyze()

        # 6a. Show support reactions
        st.subheader("Support Reactions")
        for i, R in enumerate(beam.reactions):
            st.write(f"- Support #{i+1} at x={supports[i]['pos']:.2f} m → **{R:.2f} kN**")

        # 6b. Prepare arrays for diagrams & interpretation
        xs = np.linspace(0, beam.length, 500)
        Vs = np.array([beam.shear_at(x) for x in xs])
        Ms = np.array([beam.moment_at(x) for x in xs])

        # 6c. Beam schematic
        st.subheader("Beam Schematic")
        st.pyplot(plot_beam_diagram(beam))

        # 6d. Shear force diagram
        st.subheader("Shear Force Diagram")
        st.pyplot(plot_sfd(beam))

        # 6e. Bending moment diagram
        st.subheader("Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))

        # 6f. Automated interpretation
        V_max, x_Vmax = Vs.max(), xs[Vs.argmax()]
        V_min, x_Vmin = Vs.min(), xs[Vs.argmin()]
        M_max, x_Mmax = Ms.max(), xs[Ms.argmax()]
        M_min, x_Mmin = Ms.min(), xs[Ms.argmin()]

        st.markdown("**Interpretation**")
        if point_loads:
            desc = ", ".join(f"{p['mag']:.1f} kN @ {p['pos']:.2f} m" for p in point_loads)
            st.write(f"- Point loads: {desc}.")
        if udls:
            desc = ", ".join(
                f"{u['int']:.1f} kN/m from {u['start']:.2f} m to {u['end']:.2f} m"
                for u in udls
            )
            st.write(f"- UDL(s): {desc}.")
        st.write(f"- Shear varies between **{V_min:.2f} kN** (at x={x_Vmin:.2f} m) and **{V_max:.2f} kN** (at x={x_Vmax:.2f} m).")
        st.write(f"- Moment peaks at **{M_max:.2f} kN·m** (x={x_Mmax:.2f} m) and minimum **{M_min:.2f} kN·m** (x={x_Mmin:.2f} m).")
        st.write(
            "Use these values to identify the critical sections and verify that "
            "your support reactions correctly balance all applied loads."
        )

# --- Combine into your existing tab layout ---
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
