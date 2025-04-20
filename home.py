import streamlit as st
import io
import pandas as pd

from core import Beam
from plots import plot_sfd, plot_bmd

def run():
    st.title("🛠 Beam Analysis")

    # --- Beam definition inputs ---
    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, step=0.1)
    beam = Beam(length)

    st.write("#### Point Loads")
    num_point_loads = st.number_input("How many point loads?", min_value=0, step=1, value=0, key="n_pl")
    for i in range(num_point_loads):
        col1, col2 = st.columns(2)
        with col1:
            mag = st.number_input(f"Load #{i+1} (kN)", key=f"pl_mag_{i}")
        with col2:
            pos = st.number_input(f"Position #{i+1} (m)", key=f"pl_pos_{i}", max_value=length)
        if mag != 0:
            beam.add_point_load(mag, pos)

    st.write("#### Uniform Distributed Loads")
    num_udl = st.number_input("How many UDLs?", min_value=0, step=1, value=0, key="n_udl")
    for j in range(num_udl):
        c1, c2, c3 = st.columns(3)
        with c1:
            start = st.number_input(f"UDL #{j+1} start (m)", key=f"udl_start_{j}", max_value=length)
        with c2:
            end = st.number_input(f"UDL #{j+1} end (m)", key=f"udl_end_{j}", min_value=start, max_value=length)
        with c3:
            intensity = st.number_input(f"UDL #{j+1} intensity (kN/m)", key=f"udl_int_{j}")
        if intensity != 0 and end > start:
            beam.add_distributed_load(start, end, intensity)

    if st.button("🔍 Analyze Beam"):
        # Run the analysis
        beam.analyze()
        reactions   = beam.get_reactions()
        max_moment  = beam.get_max_moment()

        # Display numeric results
        st.subheader("📊 Support Reactions")
        reactions_df = pd.DataFrame(
            list(reactions.items()),
            columns=["Support", "Reaction (kN)"]
        )
        st.dataframe(reactions_df)

        st.subheader("⚙️ Max Bending Moment")
        st.write(f"- **Value:** {max_moment[0]:.2f} kN·m")
        st.write(f"- **Location:** {max_moment[1]:.2f} m from left support")

        # --- Export Reactions CSV ---
        csv_buf = io.StringIO()
        reactions_df.to_csv(csv_buf, index=False)
        st.download_button(
            "📥 Download Reactions CSV",
            data=csv_buf.getvalue().encode("utf-8"),
            file_name="beam_reactions.csv",
            mime="text/csv",
        )

        # Plot & export Shear Force
        st.subheader("📈 Shear Force Diagram")
        fig_shear = plot_sfd(beam)
        st.pyplot(fig_shear)
        shear_buf = io.BytesIO()
        fig_shear.savefig(shear_buf, format="png", bbox_inches="tight")
        st.download_button(
            "📥 Download Shear Diagram",
            data=shear_buf.getvalue(),
            file_name="shear_diagram.png",
            mime="image/png",
        )

        # Plot & export Bending Moment
        st.subheader("📉 Bending Moment Diagram")
        fig_moment = plot_bmd(beam)
        st.pyplot(fig_moment)
        moment_buf = io.BytesIO()
        fig_moment.savefig(moment_buf, format="png", bbox_inches="tight")
        st.download_button(
            "📥 Download Moment Diagram",
            data=moment_buf.getvalue(),
            file_name="moment_diagram.png",
            mime="image/png",
        )
