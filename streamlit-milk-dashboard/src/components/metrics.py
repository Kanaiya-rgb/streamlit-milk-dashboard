import streamlit as st
import pandas as pd

def display_metrics(data):
    total_days = data.shape[0]
    milk_received_days = data[data['Milk Received?'] == 'Yes'].shape[0]
    total_milk = data['How much milk received? (ml/Liters)'].sum()
    average_milk = data['How much milk received? (ml/Liters)'].mean()
    total_pay = (total_milk / 500) * 32.5

    st.metric("Total Days", total_days)
    st.metric("Milk Received Days", milk_received_days)
    st.metric("Total Milk (ml)", total_milk)
    st.metric("Average Daily Milk (ml)", f"{average_milk:.2f}")
    st.metric("Estimated Total Pay (₹)", f"{total_pay:.2f}")