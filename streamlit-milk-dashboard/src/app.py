import streamlit as st
import pandas as pd
from src.data.load_data import load_data
from src.components.metrics import display_metrics
from src.components.charts import display_charts

st.set_page_config(page_title="Milk Records Dashboard", layout="wide")

df = load_data()
if df.empty:
    st.error("Failed to load data")
    st.stop()

st.title("🥛 Milk Records Interactive Dashboard")

# Display metrics
display_metrics(df)

# Display charts
display_charts(df)