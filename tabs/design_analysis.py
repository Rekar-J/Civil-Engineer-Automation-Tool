# tabs/design_analysis.py

import streamlit as st
import pandas as pd
import numpy as np
from core import Beam
from plots import plot_beam_diagram, plot_sfd, plot_bmd


def run_structural_analysis():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info(
        "Enter multiple loads, choose code combinations, and get factored loads/moments "
        "and section requirements per ACI/ASCE standards."
    )

    # 1️⃣ Define Point Loads
    st.markdown("#### 1️⃣ Define Point Loads")
    if "struct_pt_loads" not in st.session_state:
        st.session_state.struct_pt_loads = pd.DataFrame(
            columns=["Load Type", "Magnitude (kN)", "Direction", "Distance (m)"]
        )
    with st.expander("Add a Point Load", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            lt = st.selectbox("Load Type", ["Dead","Live","Wind","Seismic","Snow"], key="sa_lt")
        with c2:
            mag = st.number_input("Magnitude (kN)", min_value=0.0, key="sa_mag")
        with c3:
            direction = st.selectbox("Direction", ["↓ Gravity","↑ Upward"], key="sa_dir")
        with c4:
            dist = st.number_input("Distance from LHS support (m)", min_value=0.0, key="sa_dist")
        if st.button("➕ Add Load", key="sa_add_load"):
            signed = mag if direction=="↓ Gravity" else -mag
            new = {
                "Load Type": lt,
                "Magnitude (kN)": signed,
                "Direction": direction,
                "Distance (m)": dist
            }
            st.session_state.struct_pt_loads = pd.concat([
                st.session_state.struct_pt_loads,
                pd.DataFrame([new])
            ], ignore_index=True)

    st.write("##### Defined Point Loads")
    st.dataframe(st.session_state.struct_pt_loads)

    # 2️⃣ Factored Load Combinations
    st.markdown("#### 2️⃣ Select Load Combination")
    combos = {
        "1.2D + 1.6L": {"Dead":1.2, "Live":1.6},
        "1.0D + 0.5L + 1.0W": {"Dead":1.0, "Live":0.5, "Wind":1.0},
        "0.9D + 1.0W": {"Dead":0.9, "Wind":1.0},
    }
    combo_name = st.selectbox("Combination", list(combos.keys()), key="sa_combo")
    factors = combos[combo_name]

    # 3️⃣ Compute Factored Results
    if st.button("🔎 Compute Factored Results", key="sa_compute"):
        df = st.session_state.struct_pt_loads.copy()
        df["Factored Force (kN)"] = df.apply(
            lambda r: r["Magnitude (kN)"] * factors.get(r["Load Type"], 0.0), axis=1
        )
        df["Factored Moment (kN·m)"] = df["Factored Force (kN)"] * df["Distance (m)"]
        st.session_state.struct_results = df

    # Display Results
    if "struct_results" in st.session_state:
        res = st.session_state.struct_results
        st.write("##### Factored Load & Moment Table")
        st.dataframe(res)

        total_fact_load = res["Factored Force (kN)"].sum()
        max_fact_moment = res["Factored Moment (kN·m)"].abs().max()
        crit_row = res.loc[res["Factored Moment (kN·m)"].abs().idxmax()]

        st.write("##### Summary")
        st.write(f"- **Total Factored Load:** {total_fact_load:.2f} kN")
        st.write(
            f"- **Maximum Factored Moment:** {max_fact_moment:.2f} kN·m "
            f"at x = {crit_row['Distance (m)']:.2f} m"
        )
        st.write(f"- **Largest Factored Shear:** {res['Factored Force (kN)'].abs().max():.2f} kN")

        # 4️⃣ Section Check
        st.markdown("#### 4️⃣ Section Check")
        material = st.selectbox(
            "Material", ["Steel I‑beam", "Reinforced Concrete"], key="sa_material"
        )

        if material == "Steel I‑beam":
            Fy = 250.0  # MPa
            φ  = 0.9
            Z_req = max_fact_moment * 1e6 / (φ * Fy)
            st.write("##### Steel Section Modulus")
            st.write(f"- **Required Z<sub>req</sub>:** {Z_req:,.0f} mm³")
            st.write("Select a W‑section with Z ≥ Z<sub>req</sub>.  "
                     "Also verify deflection, shear, and buckling per AISC.")

            comment = (
                f"Under **{combo_name}**, factored loads sum to **{total_fact_load:.2f} kN**, "
                f"max M = **{max_fact_moment:.2f} kN·m** at **x = {crit_row['Distance (m)']:.2f} m**.  "
                f"Z<sub>req</sub> = **{Z_req:,.0f} mm³** (φ=0.9, Fy=250 MPa)."
            )

        else:  # Reinforced Concrete
            with st.expander("RC Section Properties", expanded=True):
                b    = st.number_input("Width b (mm)", value=300.0, key="rc_b")
                d    = st.number_input("Eff. depth d (mm)", value=450.0, key="rc_d")
                fpc  = st.number_input("f'c (MPa)", value=30.0, key="rc_fc")
                fy   = st.number_input("f_y (MPa)", value=500.0, key="rc_fy")
                φ_rc = st.number_input("φ reduction", min_value=0.0, value=0.9, key="rc_phi")

            # approximate lever arm = 0.9 d
            M_Nmm  = max_fact_moment * 1e6
            As_req = M_Nmm / (φ_rc * fy * 0.9 * d)
            As_pct = As_req / (b * d) * 100

            st.write("##### RC Reinforcement")
            st.write(f"- **Required A<sub>s</sub>:** {As_req:,.0f} mm²  (~{As_pct:.2f}% )")
            st.write("Check crack control, deflection, and shear per ACI 318.")

            comment = (
                f"Under **{combo_name}**, factored loads = **{total_fact_load:.2f} kN**, "
                f"max M = **{max_fact_moment:.2f} kN·m** at **x = {crit_row['Distance (m)']:.2f} m**.  "
                f"RC A<sub>s</sub> req = **{As_req:,.0f} mm²** (~{As_pct:.2f}%)."
            )

        # 5️⃣ Academic Commentary
        st.markdown("##### Commentary")
        st.markdown(f"> {comment}  Verify service deflections, shear capacity, and additional code checks.")





# --- Geotechnical Analysis Section (enhanced, ASCII only) ---
def run_geotechnical_analysis():
    st.header("Geotechnical Analysis")
    st.subheader("📌 About Geotechnical Analysis")
    st.info("Compute bearing capacity, earth pressures, settlement and CPT correlations.")

    # 1) Soil & foundation inputs
    soil_type = st.selectbox("Soil Type", ["Clay", "Silt", "Sand", "Gravel", "Rock"])
    gamma = st.number_input("Unit Weight γ (kN/m³)",
                            value=(21.0 if soil_type=="Rock" else 18.0),
                            step=0.1, key="geo_gamma")
    cohesion = st.number_input("Cohesion c (kPa)", min_value=0.0, step=1.0, key="geo_c")
    phi = st.number_input("Friction Angle φ (°)", min_value=0.0, max_value=45.0,
                          step=0.5, key="geo_phi")

    B = st.number_input("Foundation Width B (m)", min_value=0.1, step=0.1, key="geo_B")
    Df = st.number_input("Foundation Depth Df (m)", min_value=0.0,
                         step=0.1, key="geo_Df")
    FS = st.number_input("Factor of Safety", value=2.0, min_value=1.0,
                         step=0.1, key="geo_FS")

    st.markdown("---")

    # 2) Settlement inputs
    e0 = st.number_input("Initial Void Ratio e0", min_value=0.5, max_value=1.0,
                         value=0.8, step=0.05, key="geo_e0")
    mv = st.number_input("Compressibility mv (m²/kN)", min_value=1e-5,
                         value=1e-4, step=1e-5, format="%.5f", key="geo_mv")
    delta_sigma = st.number_input("Δσ (kPa)", value=50.0, step=5.0,
                                  key="geo_dsigma")
    H = st.number_input("Clay Layer Thickness H (m)", value=1.0,
                        step=0.1, key="geo_H")

    st.markdown("---")

    # 3) CPT input
    qc = st.number_input("CPT Tip Resistance qc (MPa)", min_value=0.0,
                         value=0.5, step=0.1, key="geo_qc")
    sigma_v0 = st.number_input("Overburden σ'v0 (kPa)", value=gamma*Df,
                               step=5.0, key="geo_sigma_v0")

    if st.button("🔎 Compute Geotech Results", key="geo_compute"):
        # Earth-pressure coefficients
        K0  = 1 - np.sin(np.radians(phi))
        Ka  = np.tan(np.radians(45 - phi/2))**2
        Kp  = np.tan(np.radians(45 + phi/2))**2

        # Terzaghi bearing factors
        phi_rad = np.radians(phi)
        Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45 + phi/2)))**2
        Nc = (Nq - 1) / np.tan(phi_rad) if phi>0 else 5.7
        Ngamma = 2 * (Nq + 1) * np.tan(phi_rad)

        q0 = gamma * Df
        qult = cohesion * Nc + q0 * Nq + 0.5 * gamma * B * Ngamma
        qall = qult / FS

        # Consolidation settlement
        s = mv * H / (1 + e0) * delta_sigma

        # CPT correlation index
        Nkt = (qc * 1e3) / sigma_v0 if sigma_v0>0 else np.nan

        st.session_state.geotech_results = {
            "K0": K0,
            "Ka": Ka,
            "Kp": Kp,
            "qult (kPa)": qult,
            f"qall (kPa) @ FS={FS}": qall,
            "Settlement (m)": s,
            "CPT Nkt": Nkt
        }

    # Display results
    if "geotech_results" in st.session_state:
        df_res = pd.DataFrame.from_dict(
            st.session_state.geotech_results, orient="index", columns=["Value"]
        ).reset_index()
        df_res.columns = ["Parameter", "Value"]

        st.write("### Geotechnical Results")
        st.table(df_res.style.format("{:.3f}"))

        st.markdown("##### Commentary")
        st.markdown(
            f"> Soil: **{soil_type}**, φ={phi:.1f}°, c={cohesion:.1f} kPa\n\n"
            f"- K₀={K0:.2f}, Kₐ={Ka:.2f}, Kₚ={Kp:.2f}\n"
            f"- Terzaghi qult ≈ **{qult:.0f} kPa**, qall ≈ **{qall:.0f} kPa**\n"
            f"- Settlement ≈ **{s:.3f} m** under Δσ={delta_sigma} kPa\n"
            f"- CPT index Nkt ≈ **{Nkt:.2f}**"
        )

# … rest of your tabs/design_analysis.py unchanged …




# --- Hydraulic and Hydrological Modeling Section ---
def run_hydraulic_analysis():
    st.header("Hydraulic and Hydrological Modeling")
    st.subheader("📌 About Hydrological Modeling")
    st.info("Simulates **water flow and drainage systems**, helping engineers design networks.")

    simulation_time = st.number_input("Enter Simulation Time (s)", min_value=1)
    flow_rate = st.number_input("Enter Flow Rate (L/s)", min_value=1)

    if "hydraulic_data" not in st.session_state:
        st.session_state.hydraulic_data = pd.DataFrame(columns=["Time (s)", "Flow Rate (L/s)"])

    if st.button("Add Simulation Data"):
        new_row = pd.DataFrame({
            "Time (s)": [simulation_time],
            "Flow Rate (L/s)": [flow_rate]
        })
        st.session_state.hydraulic_data = pd.concat(
            [st.session_state.hydraulic_data, new_row], ignore_index=True
        )

    st.write("### Flow Simulation Data")
    st.dataframe(st.session_state.hydraulic_data)


# --- Engineering Tests Section ---
def run_tests():
    st.header("Engineering Tests")
    st.subheader("📌 About Engineering Tests")
    st.info("Conduct lab tests on **water, soil, and materials**.")

    test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"], key="test_category")

    if test_category == "Water Tests":
        test_type = st.selectbox("Select Water Test", ["TDS", "pH"], key="water_test_type")
        if test_type == "TDS":
            st.subheader("💧 TDS Test")
            ec = st.number_input("Enter EC (µS/cm)", key="tds_ec")
            conv = st.slider("Conversion Factor (0.5–0.7)", min_value=0.5, max_value=0.7, step=0.01, key="tds_conv")
            if st.button("Calculate TDS", key="calc_tds"):
                tds = ec * conv
                st.write(f"**TDS:** {tds:.2f} mg/L")
                if tds < 300:
                    st.success("💧 Excellent Water Quality")
                elif tds < 600:
                    st.info("✅ Good Water Quality")
                elif tds < 900:
                    st.warning("⚠️ Fair Water Quality")
                else:
                    st.error("❌ Poor Water Quality")


# --- Beam Analysis Sub‑Tab ---
def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Analyze simply supported beams—choose load directions, see dimensions & get an academic summary.")

    st.write("**Note:** All distances measured from the **left end** (x = 0).")
    show_dims = st.checkbox("Show dimension lines", value=True)

    # Beam geometry
    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, key="beam_len")

    # Supports
    st.write("#### Supports (2)")
    supports = []
    for i in range(2):
        pos = st.number_input(
            f"Support #{i+1} Position (m)", min_value=0.0, max_value=length,
            value=(0.0 if i==0 else length), key=f"beam_sup_pos_{i}"
        )
        sup_type = st.selectbox(
            f"Support #{i+1} Type", ["pin","roller"], key=f"beam_sup_type_{i}"
        )
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
        point_loads.append({"pos":pos, "mag":mag * sign})

    # Uniformly distributed loads (unlimited)
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
        udls.append({"start":start, "end":end, "int":intensity * sign})

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

        xs = np.linspace(0, beam.length, 500)
        Vs = np.array([beam.shear_at(x) for x in xs])
        Ms = np.array([beam.moment_at(x) for x in xs])

        # Critical values
        idx_v = np.argmax(np.abs(Vs))
        Vmax, x_vmax = Vs[idx_v], xs[idx_v]
        zero_idxs = np.where(Vs[:-1]*Vs[1:]<0)[0]
        if zero_idxs.size>0:
            i0 = zero_idxs[0]
            x0 = xs[i0] - Vs[i0]*(xs[i0+1]-xs[i0])/(Vs[i0+1]-Vs[i0])
        else:
            x0 = xs[np.argmax(np.abs(Ms))]
        idx_m = np.argmax(np.abs(Ms))
        Mmax, x_mmax = Ms[idx_m], xs[idx_m]

        # Output
        st.write("#### Support Reactions")
        for i,R in enumerate(reactions):
            st.write(f"> Support #{i+1} at x = {supports[i]['pos']:.2f} m → **{R:.2f} kN**")

        st.write("#### Beam Schematic")
        st.pyplot(plot_beam_diagram(beam, show_dimensions=show_dims))

        st.write("#### Shear Force Diagram")
        st.pyplot(plot_sfd(beam))

        st.write("#### Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))

        st.markdown(f"""
**Academic Summary:**  
- **Reactions** at x=0: {reactions[0]:.2f} kN, at x={length:.2f} m: {reactions[1]:.2f} kN  
- **Max Shear** |V|ₘₐₓ = {abs(Vmax):.2f} kN at x = {x_vmax:.2f} m  
- **Shear zero‐crossing** at x ≃ {x0:.2f} m → location of peak M  
- **Max Moment** |M|ₘₐₓ = {abs(Mmax):.2f} kN·m at x = {x_mmax:.2f} m  

Use these critical points for detailed design and reinforcement checks.
""")

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
