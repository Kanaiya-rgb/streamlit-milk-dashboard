import streamlit as st
import pandas as pd
import requests
from io import StringIO
import plotly.express as px

# Configure wide layout with page title & icon
st.set_page_config(page_title="Milk Records Dashboard", page_icon="🥛", layout="wide")


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
    st.error("No data available")
    st.stop()

st.title("🥛 Milk Records Interactive Dashboard")

months = sorted(df['Month'].unique())
selected_month = st.sidebar.selectbox("Select Month", months)

month_data = df[df['Month'] == selected_month]

# Sidebar metrics summary
st.sidebar.header("Summary Metrics")
total_days = month_data.shape[0]
milk_received_days = month_data[month_data['Milk Received?']=='Yes'].shape[0]
total_milk = month_data[col_name].sum()
average_milk = month_data[col_name].mean()
total_pay = (total_milk / 500) * 32.5

st.sidebar.metric("Total Days", total_days)
st.sidebar.metric("Milk Received Days", milk_received_days)
st.sidebar.metric("Total Milk (ml)", total_milk)
st.sidebar.metric("Avg Daily Milk (ml)", f"{average_milk:.2f}")
st.sidebar.metric("Estimated Total Pay (₹)", f"{total_pay:.2f}")

# Main page charts area with 2 columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Milk Received Trend")
    fig1 = px.line(month_data, x='Date of Record', y=col_name,
                   markers=True, title="Daily Milk Received")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Milk Quantity Distribution")
    fig2 = px.histogram(month_data, x=col_name, nbins=20,
                        title="Milk Quantity Distribution")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Milk Received Quantity by Status")
    status_sum = month_data.groupby('Milk Received?')[col_name].sum().reset_index()
    fig3 = px.bar(status_sum, x='Milk Received?', y=col_name,
                  title="Milk Received Quantity by Status",
                  color='Milk Received?', color_discrete_map={'Yes':'green', 'No':'red'})
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Milk Received Ratio")
    status_count = month_data['Milk Received?'].value_counts().reset_index()
    status_count.columns = ['Milk Received?', 'Count']
    fig4 = px.pie(status_count, names='Milk Received?', values='Count',
                  title="Milk Received Ratio",
                  color='Milk Received?', color_discrete_map={'Yes':'green', 'No':'red'})
    st.plotly_chart(fig4, use_container_width=True)
