import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

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
    st.error("Error loading data or empty dataset.")
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
total_milk = month_data[col_name].sum()
average_milk = month_data[col_name].mean()
total_pay = (total_milk / 500) * 32.5

col1.metric("Total Days", total_days)
col2.metric("Milk Received Days", milk_received_days)
col3.metric("Total Milk (ml)", total_milk)
col4.metric("Avg Daily Milk (ml)", f"{average_milk:.2f}")
col5.metric("Total Pay (₹)", f"{total_pay:.2f}")

st.markdown("---")

# Chart 1: Daily Milk Trend
fig1 = px.line(month_data, x='Date of Record', y=col_name,
               title='Daily Milk Received Trend', markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Milk Received Quantity by Status
status_sum = month_data.groupby('Milk Received?')[col_name].sum().reset_index()
fig2 = px.bar(status_sum, x='Milk Received?', y=col_name,
              title='Milk Received Quantity by Status', color='Milk Received?')
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Milk Received Ratio Pie Chart
status_counts = month_data['Milk Received?'].value_counts().reset_index()
status_counts.columns = ['Milk Received?', 'Count']
fig3 = px.pie(status_counts, names='Milk Received?', values='Count',
              title='Milk Received Ratio', color='Milk Received?')
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Milk Received Quantity Histogram
fig4 = px.histogram(month_data, x=col_name, nbins=20,
                    title='Milk Quantity Distribution')
st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Milk Received Days vs Not Received Days (Count)
fig5 = px.bar(status_counts, x='Milk Received?', y='Count',
              title='Milk Received Day Count', color='Milk Received?')
st.plotly_chart(fig5, use_container_width=True)

# Chart 6: Average Daily Milk per Date
avg_daily = month_data.groupby('Date of Record')[col_name].mean().reset_index()
fig6 = px.scatter(avg_daily, x='Date of Record', y=col_name,
                  title='Average Daily Milk Per Date')
st.plotly_chart(fig6, use_container_width=True)
