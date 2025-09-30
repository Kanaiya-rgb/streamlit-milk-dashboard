import streamlit as st
import pandas as pd
from src.data.load_data import load_data

st.set_page_config(page_title="Overview - Milk Records Dashboard", layout="wide")

df = load_data()

if df.empty:
    st.error("Failed to load data")
    st.stop()

st.title("🥛 Overview of Milk Records")

# Summary Metrics
st.header("Summary Metrics")
total_days = df.shape[0]
total_milk = df["How much milk received? (ml/Liters)"].sum()
average_milk = df["How much milk received? (ml/Liters)"].mean()
milk_received_days = df[df['Milk Received?'] == 'Yes'].shape[0]

st.metric("Total Days Recorded", total_days)
st.metric("Total Milk Received (ml)", total_milk)
st.metric("Average Daily Milk (ml)", f"{average_milk:.2f}")
st.metric("Days Milk Received", milk_received_days)

# Displaying DataFrame
st.subheader("Milk Records Data")
st.dataframe(df)