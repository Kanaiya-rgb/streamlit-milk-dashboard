import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

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
    st.error("No data loaded")
    st.stop()

st.title("🥛 Milk Records Interactive Dashboard")

months = sorted(df['Month'].unique())
selected_month = st.selectbox("Select Month", months)
month_data = df[df['Month'] == selected_month]

sns.set(style="whitegrid")

# Layout columns: summary (left), charts (right)
summary_col, charts_col = st.columns([1, 3])

with summary_col:
    st.header("Summary Metrics")
    total_days = month_data.shape[0]
    milk_received_days = month_data[month_data['Milk Received?'] == 'Yes'].shape[0]
    total_milk = month_data[col_name].sum()
    average_milk = month_data[col_name].mean()
    total_pay = (total_milk / 500) * 32.5

    st.metric("Total Days", total_days)
    st.metric("Milk Received Days", milk_received_days)
    st.metric("Total Milk (ml)", total_milk)
    st.metric("Average Daily Milk (ml)", f"{average_milk:.2f}")
    st.metric("Estimated Total Pay (₹)", f"{total_pay:.2f}")

with charts_col:
    st.subheader("Daily Milk Received Trend")
    fig1, ax1 = plt.subplots(figsize=(10,4))
    sns.lineplot(data=month_data, x='Date of Record', y=col_name, marker='o', ax=ax1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig1)

    st.subheader("Milk Received Quantity by Status")
    fig2, ax2 = plt.subplots(figsize=(6,4))
    status_sum = month_data.groupby('Milk Received?')[col_name].sum().reset_index()
    sns.barplot(x='Milk Received?', y=col_name, data=status_sum, palette='Set2', ax=ax2)
    plt.tight_layout()
    st.pyplot(fig2)

    st.subheader("Milk Received Ratio")
    counts = month_data['Milk Received?'].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#4CAF50','#F44336'], startangle=90)
    ax3.axis('equal')
    st.pyplot(fig3)

    st.subheader("Milk Quantity Distribution")
    fig4, ax4 = plt.subplots(figsize=(8,4))
    sns.histplot(month_data[col_name], bins=20, ax=ax4)
    plt.tight_layout()
    st.pyplot(fig4)

    st.subheader("Average Daily Milk per Date")
    avg_daily = month_data.groupby('Date of Record')[col_name].mean().reset_index()
    fig5, ax5 = plt.subplots(figsize=(10,4))
    sns.scatterplot(data=avg_daily, x='Date of Record', y=col_name, ax=ax5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig5)
