import streamlit as st
import pandas as pd
import requests
from io import StringIO

sheet_url = "https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/export?format=csv&gid=725446854"

col_name = "How much milk received? (ml/Liters)"  # Global variable

@st.cache_data(ttl=600)
def load_data():
    try:
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
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

st.title("Milk Records Live Dashboard")

months = df['Month'].unique()
selected_month = st.selectbox('Select Month', months)

month_data = df[df['Month'] == selected_month]

st.write(f"## Summary for Month: {selected_month}")
st.write(month_data)

total_days = month_data.shape[0]
milk_received_days = month_data[month_data['Milk Received?'] == 'Yes'].shape[0]
total_milk = month_data[col_name].sum()
total_pay = (total_milk / 500) * 32.5

st.write(f"Total Days: {total_days}")
st.write(f"Milk Received Days: {milk_received_days}")
st.write(f"Total Milk: {total_milk} ml")
st.write(f"Total Pay: ₹{total_pay}")

st.line_chart(month_data.set_index('Date of Record')[col_name])
