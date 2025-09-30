import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
from src.data.load_data import load_data

st.set_page_config(page_title="Milk Records Analytics", layout="wide")

df = load_data()
if df.empty:
    st.error("Failed to load data")
    st.stop()

st.title("📊 Milk Records Analytics")

# Monthly analysis
months = sorted(df['Month'].unique())
selected_month = st.selectbox("Select Month", months)
month_data = df[df['Month'] == selected_month]

# Summary metrics
total_days = month_data.shape[0]
milk_received_days = month_data[month_data['Milk Received?'] == 'Yes'].shape[0]
total_milk = month_data["How much milk received? (ml/Liters)"].sum()
average_milk = month_data["How much milk received? (ml/Liters)"].mean()

st.header("Summary Metrics")
st.metric("Total Days", total_days)
st.metric("Milk Received Days", milk_received_days)
st.metric("Total Milk (ml)", total_milk)
st.metric("Average Daily Milk (ml)", f"{average_milk:.2f}")

# Visualizations
st.subheader("Daily Milk Received Trend")
fig1, ax1 = plt.subplots(figsize=(12, 4))
sns.lineplot(data=month_data, x='Date of Record', y="How much milk received? (ml/Liters)", marker='o', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Milk Received Quantity by Status")
fig2, ax2 = plt.subplots(figsize=(8, 4))
status_sum = month_data.groupby('Milk Received?')["How much milk received? (ml/Liters)"].sum().reset_index()
sns.barplot(x='Milk Received?', y="How much milk received? (ml/Liters)", data=status_sum, palette='Set2', ax=ax2)
st.pyplot(fig2)

st.subheader("Milk Received Ratio")
counts = month_data['Milk Received?'].value_counts()
fig3, ax3 = plt.subplots(figsize=(6, 6))
ax3.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')
st.pyplot(fig3)

st.subheader("Milk Quantity Distribution")
fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.histplot(month_data["How much milk received? (ml/Liters)"], bins=20, kde=True, ax=ax4)
st.pyplot(fig4)

st.subheader("Average Daily Milk per Date")
avg_daily = month_data.groupby('Date of Record')["How much milk received? (ml/Liters)"].mean().reset_index()
fig5, ax5 = plt.subplots(figsize=(12, 4))
sns.scatterplot(data=avg_daily, x='Date of Record', y="How much milk received? (ml/Liters)", ax=ax5)
plt.xticks(rotation=45)
st.pyplot(fig5)