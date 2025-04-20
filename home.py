import streamlit as st
st.set_page_config(page_title="Civil Beam Analyzer", layout="wide")

from core import Beam, Support, Load
from plots import plot_beam_diagram, plot_sfd, plot_bmd
import matplotlib.pyplot as plt

def run():
    st.title("Civil Beam Analyzer 📐")

    st.markdown("Use this tool to define a beam, apply loads and supports, and visualize the Shear Force Diagram (SFD) and Bending Moment Diagram (BMD).")

    st.subheader("1. Define Beam Properties")
    length = st.number_input("Beam Length (m)", min_value=1.0, step=0.5)

    st.subheader("2. Add Supports")
    support_positions = st.text_input("Support Positions (comma-separated in meters)", "0, 5")

    st.subheader("3. Add Loads")
    point_loads_str = st.text_area("Point Loads (Format: pos(kN), e.g. 2@10, 4@5)", "2@10, 4@5")
    udl_loads_str = st.text_area("UDLs (Format: start,end,intensity, e.g. 2,4,3)", "2,4,3")

    if st.button("Analyze"):
        beam = Beam(length)

        try:
            supports = [Support(float(p)) for p in support_positions.split(",")]
            for s in supports:
                beam.add_support(s)

            if point_loads_str.strip():
                point_loads = point_loads_str.split(",")
                for p in point_loads:
                    pos, mag = map(float, p.split("@"))
                    beam.add_load(Load("point", magnitude=mag, position=pos))

            if udl_loads_str.strip():
                udls = udl_loads_str.split(",")
                for i in range(0, len(udls), 3):
                    start = float(udls[i])
                    end = float(udls[i+1])
                    intensity = float(udls[i+2])
                    beam.add_load(Load("udl", magnitude=intensity, start=start, end=end))

            beam.analyze()

            st.success("Analysis complete!")

            st.subheader("4. Beam Visualization")

            st.pyplot(plot_beam_diagram(beam))
            st.pyplot(plot_sfd(beam))
            st.pyplot(plot_bmd(beam))

        except Exception as e:
            st.error(f"Error in input or analysis: {e}")
