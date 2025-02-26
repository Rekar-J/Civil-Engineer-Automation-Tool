import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.header("Data Visualization")
    st.subheader("📌 About Data Visualization")
    st.info("This tool helps engineers visualize project data using interactive charts and graphs.")

    # Sample dataset for visualization
    st.write("### Upload CSV Data for Visualization")
    uploaded_data = st.file_uploader("Upload CSV File", type=["csv"], key="data_viz_upload")

    if uploaded_data:
        df = pd.read_csv(uploaded_data)
        st.write("### Uploaded Data")
        st.dataframe(df)

        # Select column for visualization
        column_options = list(df.columns)
        selected_column = st.selectbox("Select Column for Visualization", column_options, key="data_viz_column")

        # Generate Bar Chart
        st.write("### Data Distribution")
        fig = px.histogram(df, x=selected_column, title=f"Distribution of {selected_column}")
        st.plotly_chart(fig, use_container_width=True)
