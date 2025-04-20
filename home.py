import streamlit as st
import numpy as np

from core import Beam
from plots import plot_sfd, plot_bmd

def run():
    st.title("Civil Beam Analyzer")

    # --- Beam definition inputs ---
    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0)

    # --- Supports ---
    st.write("#### Supports")
    num_supports = st.number_input(
        "How many supports?", min_value=0, max_value=2, value=2, step=1
    )
    supports = []
    for i in range(int(num_supports)):
        pos = st.number_input(
            f"Support #{i+1} position (m)",
            min_value=0.0,
            max_value=length,
            value=0.0 if i == 0 else length,
            key=f"sup_pos_{i}",
        )
        sup_type = st.selectbox(
            f"Support #{i+1} type",
            ["pin", "roller"],
            key=f"sup_type_{i}"
        )
        supports.append({"pos": pos, "type": sup_type})

    # --- Point Loads ---
    st.write("#### Point Loads")
    num_point_loads = st.number_input(
        "How many point loads?", min_value=0, value=0, step=1
    )
    point_loads = []
    for i in range(int(num_point_loads)):
        pos = st.number_input(
            f"Load #{i+1} position (m)",
            min_value=0.0,
            max_value=length,
            value=length / 2,
            key=f"pl_pos_{i}",
        )
        mag = st.number_input(
            f"Load #{i+1} magnitude (kN)",
            value=10.0,
            key=f"pl_mag_{i}",
        )
        point_loads.append({"pos": pos, "mag": mag})

    # --- Uniformly Distributed Loads (UDLs) ---
    st.write("#### Uniformly Distributed Loads")
    num_udls = st.number_input(
        "How many UDLs?", min_value=0, value=0, step=1
    )
    udls = []
    for i in range(int(num_udls)):
        start = st.number_input(
            f"UDL #{i+1} start (m)",
            min_value=0.0,
            max_value=length,
            value=0.0,
            key=f"udl_start_{i}",
        )
        end = st.number_input(
            f"UDL #{i+1} end (m)",
            min_value=0.0,
            max_value=length,
            value=length,
            key=f"udl_end_{i}",
        )
        intensity = st.number_input(
            f"UDL #{i+1} intensity (kN/m)",
            value=5.0,
            key=f"udl_int_{i}",
        )
        udls.append({"start": start, "end": end, "int": intensity})

    # --- Build and Solve the Beam ---
    # pass empty lists for supports and loads to satisfy the new __init__
    beam = Beam(length, supports=[], loads=[])

    # register supports
    for sup in supports:
        beam.add_support(sup["pos"], sup["type"])

    # register point loads
    for pl in point_loads:
        beam.add_point_load(pl["pos"], pl["mag"])

    # register UDLs
    for ud in udls:
        beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

    # only analyze when ready
    if st.button("🔎 Analyze"):
        beam.analyze()

        # --- Display Reactions ---
        st.write("#### Support Reactions")
        for i, R in enumerate(beam.reactions):
            pos = supports[i]["pos"] if i < len(supports) else "?"
            st.write(f"> Support #{i+1} at {pos} m → {R:.2f} kN")

        # --- Display Maximum Moment ---
        xs = np.linspace(0, beam.length, 200)
        max_M = max(abs(beam.moment_at(x)) for x in xs)
        st.write(f"#### Maximum Bending Moment: **{max_M:.2f} kN·m**")

        # --- Plot Diagrams ---
        st.write("#### Shear Force Diagram")
        st.pyplot(plot_sfd(beam))
        st.write("#### Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))
