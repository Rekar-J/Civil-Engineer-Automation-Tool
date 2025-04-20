import streamlit as st
from core import Beam, Support, Load
from plots import plot_beam_diagram, plot_sfd, plot_bmd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Civil Beam Analyzer", layout="wide")

st.title("Civil Beam Analyzer 📐")

# Beam length input
beam_length = st.number_input("Enter beam length (m):", min_value=1.0, step=0.5)

# Initialize session state
if "supports" not in st.session_state:
    st.session_state.supports = []
if "point_loads" not in st.session_state:
    st.session_state.point_loads = []

st.markdown("## 🧷 Add Supports")

col1, col2, col3 = st.columns(3)

with col1:
    support_type = st.selectbox("Support Type", ["pin", "roller", "fixed"])
with col2:
    support_position = st.number_input("Support Position (m)", min_value=0.0, max_value=beam_length, step=0.1)
with col3:
    if st.button("Add Support"):
        st.session_state.supports.append(Support(support_position, support_type))
        st.success(f"{support_type.capitalize()} support added at {support_position} m")

# Show current supports
if st.session_state.supports:
    st.markdown("**Current Supports:**")
    for idx, sup in enumerate(st.session_state.supports):
        st.markdown(f"- `{sup.kind}` at {sup.position} m")

st.markdown("---")
st.markdown("## 🪶 Add Point Loads")

col4, col5, col6 = st.columns(3)

with col4:
    load_magnitude = st.number_input("Magnitude (kN)", step=0.1, format="%.2f")
with col5:
    load_position = st.number_input("Load Position (m)", min_value=0.0, max_value=beam_length, step=0.1)
with col6:
    if st.button("Add Load"):
        st.session_state.point_loads.append(Load("point", load_position, magnitude=load_magnitude))
        st.success(f"Point load of {load_magnitude} kN added at {load_position} m")

# Show current point loads
if st.session_state.point_loads:
    st.markdown("**Current Point Loads:**")
    for idx, load in enumerate(st.session_state.point_loads):
        st.markdown(f"- `{load.kind}` load of {load.magnitude} kN at {load.position} m")

st.markdown("---")

# Analyze button
if st.button("Analyze Beam"):
    beam = Beam(beam_length)

    for support in st.session_state.supports:
        beam.add_support(support)

    for load in st.session_state.point_loads:
        beam.add_point_load(load)

    x, V, M = beam.analyze()

    st.markdown("## 🖼️ Beam Diagram")
    st.pyplot(plot_beam_diagram(beam))

    st.markdown("## 📉 Shear Force Diagram (SFD)")
    st.pyplot(plot_sfd(x, V))

    st.markdown("## 📈 Bending Moment Diagram (BMD)")
    st.pyplot(plot_bmd(x, M))

st.markdown("---")

if st.button("Reset All"):
    st.session_state.supports = []
    st.session_state.point_loads = []
    st.success("Session reset — ready to start fresh.")
