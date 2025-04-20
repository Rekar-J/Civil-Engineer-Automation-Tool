# tabs/design_analysis.py

import streamlit as st
import pandas as pd
import numpy as np
from core import Beam
from plots import plot_sfd, plot_bmd

# --- Beam Analysis Sub‑tab ---
def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Define a simply‑supported beam, add supports, point loads, UDLs, then analyze.")

    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, key="beam_length")

    # Supports
    st.write("#### Supports")
    num_sup = st.number_input("How many supports? (max 2)", min_value=0, max_value=2, value=2, step=1, key="beam_num_sup")
    supports = []
    for i in range(int(num_sup)):
        pos = st.number_input(f"Support #{i+1} position (m)", 0.0, length, 0.0 if i==0 else length, key=f"beam_sup_pos_{i}")
        typ = st.selectbox(f"Support #{i+1} type", ["pin","roller"], key=f"beam_sup_type_{i}")
        supports.append({"pos": pos, "type": typ})

    # Point loads
    st.write("#### Point Loads")
    num_pl = st.number_input("How many point loads?", min_value=0, value=0, step=1, key="beam_num_pl")
    point_loads = []
    for i in range(int(num_pl)):
        pos = st.number_input(f"Load #{i+1} position (m)", 0.0, length, length/2, key=f"beam_pl_pos_{i}")
        mag = st.number_input(f"Load #{i+1} magnitude (kN)", min_value=0.0, value=10.0, key=f"beam_pl_mag_{i}")
        point_loads.append({"pos": pos, "mag": mag})

    # UDLs
    st.write("#### Uniformly Distributed Loads")
    num_udl = st.number_input("How many UDLs?", min_value=0, value=0, step=1, key="beam_num_udl")
    udls = []
    for i in range(int(num_udl)):
        start = st.number_input(f"UDL #{i+1} start (m)", 0.0, length, 0.0, key=f"beam_udl_start_{i}")
        end   = st.number_input(f"UDL #{i+1} end (m)",   0.0, length, length, key=f"beam_udl_end_{i}")
        inte  = st.number_input(f"UDL #{i+1} intensity (kN/m)", min_value=0.0, value=5.0, key=f"beam_udl_int_{i}")
        udls.append({"start": start, "end": end, "int": inte})

    # Build beam object
    beam = Beam(length, supports=[], loads=[])
    for sup in supports:
        beam.add_support(sup["pos"], sup["type"])
    for pl in point_loads:
        beam.add_point_load(pl["pos"], pl["mag"])
    for ud in udls:
        beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

    if st.button("🔎 Analyze Beam", key="analyze_beam"):
        try:
            beam.analyze()

            # Reactions
            st.write("#### Support Reactions")
            for i, R in enumerate(beam.reactions):
                pos = supports[i]["pos"] if i < len(supports) else "?"
                st.write(f"> Support #{i+1} @ {pos:.2f} m → **{R:.2f} kN**")

            # Max moment
            xs = np.linspace(0, beam.length, 200)
            max_M = max(abs(beam.moment_at(x)) for x in xs)
            st.write(f"#### Maximum Bending Moment: **{max_M:.2f} kN·m**")

            # Shear & Moment diagrams
            st.write("#### Shear Force Diagram")
            st.pyplot(plot_sfd(beam))

            st.write("#### Bending Moment Diagram")
            st.pyplot(plot_bmd(beam))

        except Exception as e:
            st.error(f"Error during analysis: {e}")

# --- Your existing Structural, Geo, Hydro & Tests sections follow unchanged ---
def run_structural_analysis():
    # ... your code as before ...
    st.header("Structural Analysis")
    # (no changes)

def run_geotechnical_analysis():
    # ... your code as before ...
    st.header("Geotechnical Analysis")
    # (no changes)

def run_hydraulic_analysis():
    # ... your code as before ...
    st.header("Hydraulic & Hydrological Modeling")
    # (no changes)

def run_tests():
    # ... your code as before ...
    st.header("Engineering Tests")
    # (no changes)

# --- Top‑level for the Design & Analysis tab ---
def run():
    st.title("🛠️ Design & Analysis")
    tabs = st.tabs([
        "Beam Analysis",
        "Structural Analysis",
        "Geotechnical Analysis",
        "Hydraulic & Hydrological",
        "Tests"
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
