import streamlit as st
import plotly.express as px
import pandas as pd

# Sample data for Plotly chart
df = px.data.iris()

# Create Plotly chart
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')

# Inject custom CSS to reduce spacing
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        padding-top: 0px;  /* Reduce spacing from the top */
    }
    .sidebar .stPlotlyChart {
        margin-bottom: 0px;  /* Reduce spacing below the Plotly chart */
    }
    .sidebar .stMultiSelect {
        margin-top: 0px;  /* Reduce spacing above the multi-selection widget */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Place Plotly chart and multi-selection widget in the sidebar
st.sidebar.plotly_chart(fig)
options = st.sidebar.multiselect('Select options:', df['species'].unique())
