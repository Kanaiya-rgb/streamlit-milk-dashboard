import streamlit as st
import pandas as pd

# Google Sheet CSV export link - replace YOUR_SHEET_ID & GID 0 if needed
sheet_url = "https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/edit?usp=sharing"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(sheet_url)
    df['How much milk received? (ml/Liters)'] = df['How much milk received? (ml/Liters)'].str.replace('ml', '').astype(int)
    df['Date of Record'] = pd.to_datetime(df['Date of Record'])
    return df

df = load_data()

st.title("Milk Records Live Dashboard")

month_options = df['Month'].unique()
selected_month = st.selectbox('Select Month', month_options)

month_data = df[df['Month'] == selected_month]

st.write(f"## Summary for Month: {selected_month}")
st.write(month_data)

total_days = month_data.shape[0]
milk_received_days = month_data[month_data['Milk Received?'] == 'Yes'].shape[0]
total_milk = month_data['How much milk received? (ml/Liters)'].sum()
total_pay = (total_milk / 500) * 32.5

st.write(f"Total Days: {total_days}")
st.write(f"Milk Received Days: {milk_received_days}")
st.write(f"Total Milk: {total_milk} ml")
st.write(f"Total Pay: ₹{total_pay}")

st.line_chart(month_data.set_index('Date of Record')['How much milk received? (ml/Liters)'])
