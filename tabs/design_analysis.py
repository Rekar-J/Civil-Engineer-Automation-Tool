# tabs/design_analysis.py
import streamlit as st
import numpy as np
from core import Beam
from plots import plot_beam_diagram, plot_sfd, plot_bmd

# … (structural, geo, hydro, tests unchanged) …

def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Analyze simply supported beams—choose load directions, see dimensions & get an academic summary.")

    st.write("**Note:** All distances measured from the left end (x = 0).")
    show_dims = st.checkbox("Show dimension lines", value=True)

    # Beam geometry
    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, key="beam_len")

    # Supports (exactly 2)
    st.write("#### Supports (2)")
    supports = []
    for i in range(2):
        pos = st.number_input(f"Support #{i+1} Position (m)", min_value=0.0, max_value=length,
                               value=(0.0 if i==0 else length), key=f"beam_sup_pos_{i}")
        sup_type = st.selectbox(f"Support #{i+1} Type", ["pin","roller"], key=f"beam_sup_type_{i}")
        supports.append({"pos":pos, "type":sup_type})

    # Point loads (unlimited)
    st.write("#### Point Loads")
    n_pl = st.number_input("How many point loads?", min_value=0, value=0, step=1, key="beam_pl_num")
    point_loads = []
    for i in range(int(n_pl)):
        pos = st.number_input(f"Load #{i+1} Position (m)", min_value=0.0, max_value=length,
                               value=length/2, key=f"beam_pl_pos_{i}")
        mag = st.number_input(f"Load #{i+1} Magnitude (kN)", value=10.0, key=f"beam_pl_mag_{i}")
        direction = st.selectbox(f"Load #{i+1} Direction", ["Downward","Upward"], key=f"beam_pl_dir_{i}")
        sign = 1 if direction=="Upward" else -1
        point_loads.append({"pos":pos, "mag":mag*sign})

    # Uniformly distributed loads
    st.write("#### Uniformly Distributed Loads")
    n_udl = st.number_input("How many UDLs?", min_value=0, value=0, step=1, key="beam_udl_num")
    udls = []
    for i in range(int(n_udl)):
        start = st.number_input(f"UDL #{i+1} Start (m)", min_value=0.0, max_value=length,
                                 value=0.0, key=f"beam_udl_start_{i}")
        end   = st.number_input(f"UDL #{i+1} End (m)",   min_value=0.0, max_value=length,
                                 value=length, key=f"beam_udl_end_{i}")
        intensity = st.number_input(f"UDL #{i+1} Intensity (kN/m)", value=5.0, key=f"beam_udl_int_{i}")
        direction = st.selectbox(f"UDL #{i+1} Direction", ["Downward","Upward"], key=f"beam_udl_dir_{i}")
        sign = 1 if direction=="Upward" else -1
        udls.append({"start":start, "end":end, "int":intensity*sign})

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
        reactions = beam.reactions

        # sample shear & moment
        xs = np.linspace(0, beam.length, 500)
        Vs = np.array([beam.shear_at(x) for x in xs])
        Ms = np.array([beam.moment_at(x) for x in xs])

        # max shear
        idx_v = np.argmax(np.abs(Vs))
        Vmax, x_vmax = Vs[idx_v], xs[idx_v]

        # zero‐shear location (first sign change)
        zero_idxs = np.where(Vs[:-1]*Vs[1:]<0)[0]
        if zero_idxs.size>0:
            i0 = zero_idxs[0]
            x0 = xs[i0] - Vs[i0]*(xs[i0+1]-xs[i0])/(Vs[i0+1]-Vs[i0])
        else:
            x0 = xs[np.argmax(np.abs(Ms))]

        # max moment
        idx_m = np.argmax(np.abs(Ms))
        Mmax, x_mmax = Ms[idx_m], xs[idx_m]

        # Display
        st.write("#### Support Reactions")
        for i,R in enumerate(reactions):
            st.write(f"> Support #{i+1} at x = {supports[i]['pos']:.2f} m → **{R:.2f} kN**")

        st.write("#### Beam Schematic")
        st.pyplot(plot_beam_diagram(beam, show_dimensions=show_dims))

        st.write("#### Shear Force Diagram")
        st.pyplot(plot_sfd(beam))

        st.write("#### Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))

        # academic summary
        st.markdown(f"""
**Academic Summary:**  
- **Reactions:** R₁ = {reactions[0]:.2f} kN at x=0, R₂ = {reactions[1]:.2f} kN at x={length:.2f} m.  
- **Maximum Shear:** |V|max = {abs(Vmax):.2f} kN at x = {x_vmax:.2f} m.  
- **Shear crosses zero** at x ≃ {x0:.2f} m, which locates the peak bending moment.  
- **Maximum Bending Moment:** |M|max = {abs(Mmax):.2f} kN·m at x = {x_mmax:.2f} m.  

These critical values identify sections requiring detailed design checks and reinforcement.
""")

# Combined Tabs
def run():
    st.title("🛠️ Design and Analysis")
    tabs = st.tabs([
        "Structural Analysis", "Beam Analysis",
        "Geotechnical Analysis", "Hydraulic & Hydrological Modeling", "Tests"
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
