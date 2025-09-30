import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Configure page
st.set_page_config(
    page_title="Milk Records Dashboard",
    page_icon="🥛",
    layout="wide"
)

# Data loading and caching
@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/export?format=csv&gid=725446854"
    response = requests.get(url)
    response.raise_for_status()
    data = StringIO(response.text)
    df = pd.read_csv(data)
    df.columns = df.columns.str.strip()
    col_name = "How much milk received? (ml/Liters)"
    if col_name in df.columns:
        df[col_name] = df[col_name].str.replace('ml', '').str.strip().astype(int)
    df['Date of Record'] = pd.to_datetime(df['Date of Record'])
    return df

df = load_data()
if df.empty:
    st.error("Data loading failed or data is empty.")
    st.stop()

st.title("🥛 Milk Records Interactive Dashboard")

# Month filter and selection
months = sorted(df['Month'].unique())
selected_month = st.selectbox("Select Month", months)
month_data = df[df['Month'] == selected_month]

# KPIs in columns
col1, col2, col3, col4, col5 = st.columns(5)

total_days = month_data.shape[0]
milk_received_days = month_data[month_data['Milk Received?'] == 'Yes'].shape[0]
total_milk = month_data["How much milk received? (ml/Liters)"].sum()
average_milk = month_data["How much milk received? (ml/Liters)"].mean()
total_pay = (total_milk / 500) * 32.5

col1.metric("Total Days", total_days)
col2.metric("Milk Received Days", milk_received_days)
col3.metric("Total Milk (ml)", total_milk)
col4.metric("Avg Daily Milk (ml)", f"{average_milk:.2f}")
col5.metric("Total Pay (₹)", f"{total_pay:.2f}")

st.markdown("---")
st.header("Milk Received Trend Over the Month")
fig1 = px.line(month_data, x='Date of Record', y="How much milk received? (ml/Liters)", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.header("Milk Received by Status")
status_summary = month_data.groupby('Milk Received?')["How much milk received? (ml/Liters)"].sum().reset_index()
fig2 = px.bar(status_summary, x='Milk Received?', y="How much milk received? (ml/Liters)", color='Milk Received?', color_discrete_map={'Yes':'green', 'No':'red'})
st.plotly_chart(fig2, use_container_width=True)

st.header("Milk Received Proportion")
count_status = month_data['Milk Received?'].value_counts().reset_index()
count_status.columns = ['Milk Received?', 'Count']
fig3 = px.pie(count_status, names='Milk Received?', values='Count', color='Milk Received?',
              color_discrete_map={'Yes':'green', 'No':'red'}, title="Received vs Not Received")
st.plotly_chart(fig3, use_container_width=True)
