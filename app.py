import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

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
    else:
        st.error(f"Column '{col_name}' not found!")
    df['Date of Record'] = pd.to_datetime(df['Date of Record'])
    return df

df = load_data()
if df.empty:
    st.stop()

st.title("Milk Records Dashboard")

# Overall KPIs with cards in 3 columns
total_days = df.shape[0]
milk_received_days = df[df['Milk Received?'] == 'Yes'].shape[0]
total_milk = df[col_name].sum()
average_milk = df[col_name].mean()
total_pay = (total_milk / 500) * 32.5

col1, col2, col3 = st.columns(3)
col1.metric("Total Days Logged", total_days)
col2.metric("Days Milk Received", milk_received_days)
col3.metric("Total Milk Received (ml)", total_milk)

col4, col5 = st.columns(2)
col4.metric("Average Daily Milk (ml)", f"{average_milk:.2f}")
col5.metric("Estimated Total Pay (₹)", f"{total_pay:.2f}")

st.markdown("---")

# Month selection for detailed view
months = df['Month'].unique()
selected_month = st.selectbox('Select Month to see details', months)

month_data = df[df['Month'] == selected_month]

st.subheader(f"Milk Records for Month: {selected_month}")
st.dataframe(month_data)

# Daily Milk Received Line Chart
st.markdown("### Daily Milk Received Trend")
st.line_chart(month_data.set_index('Date of Record')[col_name])

# Milk Received Yes/No Sum Bar Chart
st.markdown("### Milk Received Quantity by Received Status")
st.bar_chart(month_data.groupby('Milk Received?')[col_name].sum())

# Milk Received Ratio Pie Chart
st.markdown("### Milk Received Ratio (Yes / No)")
counts = month_data['Milk Received?'].value_counts()
fig, ax = plt.subplots()
ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['green', 'red'])
st.pyplot(fig)
