import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Milk Records Dashboard",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading for Milk Dashboard ---
@st.cache_data(ttl=600) # Cache data for 10 minutes
def load_data():
    """Loads and cleans the Milk Records data from a Google Sheet URL."""
    # This is the CORRECTLY formatted URL for CSV export from the sheet you provided.
    sheet_url = 'https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/export?format=csv'
    
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    col_name = "How much milk received? (ml/Liters)"
    
    if col_name in df.columns:
        # Convert column to string before using .str accessor to avoid errors
        df[col_name] = df[col_name].astype(str).str.replace('ml', '', regex=False).str.strip()
        # Replace non-numeric values (like empty strings) with '0' before converting to int
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0).astype(int)
        
    df['Date of Record'] = pd.to_datetime(df['Date of Record'], errors='coerce')
    df.dropna(subset=['Date of Record'], inplace=True) # Drop rows where date conversion failed
    return df

# --- Main App ---
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data from Google Sheet: {e}")
    st.info("Please ensure the Google Sheet's sharing setting is 'Anyone with the link can view'.")
    st.stop()

if df.empty:
    st.error("No data could be loaded. The Google Sheet might be empty or in an incorrect format.")
    st.stop()

st.title("🥛 Milk Records Interactive Dashboard")
st.markdown("Track your daily milk consumption and payments.")

# --- Sidebar for Filters ---
st.sidebar.header('Filter Your Data')
# Ensure 'Month' column exists before proceeding
if 'Month' not in df.columns:
    st.error("The 'Month' column is missing from your Google Sheet.")
    st.stop()

months = sorted(df['Month'].unique())
selected_month = st.sidebar.selectbox("Select Month", months)
month_data = df[df['Month'] == selected_month].copy()

if month_data.empty:
    st.warning("No data available for the selected month.")
    st.stop()

# --- Sidebar KPIs ---
st.sidebar.header("Summary for " + str(selected_month))
col_name = "How much milk received? (ml/Liters)"
total_days = month_data.shape[0]
milk_received_days = month_data[month_data['Milk Received?']=='Yes'].shape[0]
total_milk = int(month_data[col_name].sum())
# Calculate average only for days milk was received to avoid skewing by zeros
average_milk = month_data[month_data[col_name] > 0][col_name].mean()
total_pay = (total_milk / 500) * 32.5

st.sidebar.metric("Total Days Recorded", total_days)
st.sidebar.metric("Milk Received Days", f"{milk_received_days} / {total_days}")
st.sidebar.metric("Total Milk Consumed (ml)", f"{total_milk:,}")
st.sidebar.metric("Avg. Consumption (ml/day)", f"{average_milk:,.2f}" if pd.notna(average_milk) else "0.00")
st.sidebar.metric("Estimated Total Pay (₹)", f"₹{total_pay:,.2f}")
st.markdown("---")


# --- Main Page Charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Milk Received Trend")
    fig1 = px.line(month_data, x='Date of Record', y=col_name, markers=True, template='plotly_white', labels={'Date of Record': 'Date', col_name: 'Milk (ml)'})
    fig1.update_traces(marker=dict(size=8), line=dict(width=3))
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Milk Quantity Distribution")
    fig2 = px.histogram(month_data[month_data[col_name] > 0], x=col_name, nbins=10, template='plotly_white', labels={col_name: 'Milk Quantity (ml)'})
    fig2.update_layout(bargap=0.1)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Milk Received vs. Not Received (Days)")
    status_count = month_data['Milk Received?'].value_counts().reset_index()
    fig4 = px.pie(status_count, names='Milk Received?', values='count', hole=0.4, color='Milk Received?', color_discrete_map={'Yes':'#00B388', 'No':'#FF6B6B'})
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Total Milk Quantity by Status")
    status_sum = month_data.groupby('Milk Received?')[col_name].sum().reset_index()
    fig3 = px.bar(status_sum, x='Milk Received?', y=col_name, color='Milk Received?', color_discrete_map={'Yes':'#00B388', 'No':'#FF6B6B'}, template='plotly_white', text_auto='.2s')
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

