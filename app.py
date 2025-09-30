import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# Google Sheet CSV export URL
sheet_url = "https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/export?format=csv&gid=725446854"
col_name = "How much milk received? (ml/Liters)"

@st.cache_data(ttl=600)
def load_data():
    response = requests.get(sheet_url)
    response.raise_for_status()
    data = StringIO(response.text)
    df = pd.read_csv(data)
    df.columns = df.columns.str.strip()
    if col_name in df.columns:
        df[col_name] = df[col_name].str.replace('ml', '').str.strip().astype(int)
    df['Date of Record'] = pd.to_datetime(df['Date of Record'])
    return df

df = load_data()
if df.empty:
    st.stop()

st.title("Milk Records Analysis Dashboard")

# KPIs
total_days = df.shape[0]
milk_received_days = df[df['Milk Received?'] == 'Yes'].shape[0]
total_milk = df[col_name].sum()
average_milk = df[col_name].mean()
total_pay = (total_milk / 500) * 32.5

st.header("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Days", total_days)
col2.metric("Milk Received Days", milk_received_days)
col3.metric("Total Milk", f"{total_milk} ml")

col4, col5 = st.columns(2)
col4.metric("Average Daily Milk", f"{average_milk:.2f} ml")
col5.metric("Total Pay", f"₹{total_pay:.2f}")

# Filter by Month
st.subheader("Filter by Month")
months = sorted(df['Month'].unique())
selected_month = st.selectbox("Select Month", months)
month_data = df[df['Month'] == selected_month]

sns.set(style="whitegrid")

# Line plot for daily milk received trend with better layout
st.subheader("Daily Milk Received Trend")
fig1, ax1 = plt.subplots(figsize=(12,6))
sns.lineplot(data=month_data, x='Date of Record', y=col_name, marker='o', ax=ax1)
ax1.set_ylabel("Milk (ml)")
ax1.set_xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# Bar plot for milk received quantity by status with proper layout
st.subheader("Milk Received Quantity by Status")
fig2, ax2 = plt.subplots(figsize=(8,5))
bar_data = month_data.groupby('Milk Received?')[col_name].sum().reset_index()
sns.barplot(x='Milk Received?', y=col_name, data=bar_data, palette='Set2', ax=ax2)
ax2.set_ylabel("Total Milk (ml)")
plt.tight_layout()
st.pyplot(fig2)

# Pie chart for milk received ratio with balanced aspect ratio
st.subheader("Milk Received Ratio")
counts = month_data['Milk Received?'].value_counts()
fig3, ax3 = plt.subplots(figsize=(6,6))
ax3.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#4CAF50','#F44336'], startangle=90)
ax3.axis('equal')
st.pyplot(fig3)
