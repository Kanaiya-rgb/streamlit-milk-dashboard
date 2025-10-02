import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calendar import month_name
import numpy as np

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Advanced Milk Dashboard",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME AND STYLING ---
# Using a dictionary to hold theme colors for easy switching
theme = {
    "bg_color": "#1a1a1a",
    "main_bg_color": "#262730",
    "metric_bg_color": "#333333",
    "text_color": "#FAFAFA",
    "primary_color": "#3399FF",
    "secondary_color": "#FF6B6B",
    "plotly_template": "plotly_dark"
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    body, .stApp {{
        font-family: 'Roboto', sans-serif;
        background-color: {theme['bg_color']};
        color: {theme['text_color']};
    }}
    .main .block-container {{
        background-color: {theme['main_bg_color']};
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    }}
    div[data-testid="metric-container"] {{
        background-color: {theme['metric_bg_color']};
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }}
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.15);
    }}
    .css-1d391kg {{ /* Sidebar styling */
        background-color: {theme['main_bg_color']};
    }}
</style>
""", unsafe_allow_html=True)


# --- Data Loading ---
@st.cache_data(ttl=600)
def load_data():
    """Loads and cleans the Milk Records data from a Google Sheet URL."""
    sheet_url = 'https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/export?format=csv'
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    col_name = "How much milk received? (ml/Liters)"
    if col_name in df.columns:
        df[col_name] = pd.to_numeric(df[col_name].astype(str).str.replace('ml', '', regex=False).str.strip(), errors='coerce').fillna(0).astype(int)
    df['Date of Record'] = pd.to_datetime(df['Date of Record'], errors='coerce')
    df.dropna(subset=['Date of Record'], inplace=True)
    df['Year'] = df['Date of Record'].dt.year
    df['Month'] = df['Date of Record'].dt.month
    return df

# --- Main App ---
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data from Google Sheet: {e}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.title("Filters & Settings")
st.sidebar.markdown("---")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))

month_map = {i: month_name[i] for i in range(1, 13)}
# Filter available months based on selected year
available_months_in_year = sorted(df[df['Year'] == selected_year]['Month'].unique())
available_month_names = [month_map[m] for m in available_months_in_year]

selected_month_name = st.sidebar.selectbox("Select Month", available_month_names, index=len(available_month_names)-1)
selected_month_num = list(month_map.keys())[list(month_map.values()).index(selected_month_name)]

# --- Dynamic Price Input ---
st.sidebar.markdown("---")
st.sidebar.subheader("Cost Calculation")
price_per_500ml = st.sidebar.number_input("Price per 500 ml (₹)", min_value=1.0, value=32.5, step=0.5)

# --- Data Filtering ---
month_data = df[(df['Year'] == selected_year) & (df['Month'] == selected_month_num)].copy()

# --- Main Dashboard Area ---
st.title(f"🥛 Advanced Milk Dashboard: {selected_month_name} {selected_year}")
st.markdown("An interactive analysis of your daily milk consumption and estimated costs.")
st.markdown("---")

# --- KPI Calculations ---
col_name = "How much milk received? (ml/Liters)"
total_milk = int(month_data[col_name].sum())
total_pay = (total_milk / 500) * price_per_500ml

# --- Month-over-Month Comparison Logic ---
prev_month_year, prev_month_num = (selected_year, selected_month_num - 1) if selected_month_num > 1 else (selected_year - 1, 12)
prev_month_data = df[(df['Year'] == prev_month_year) & (df['Month'] == prev_month_num)]
prev_month_total_milk = int(prev_month_data[col_name].sum())

def get_percentage_change(current, previous):
    if previous > 0:
        return f"{((current - previous) / previous) * 100:.1f}%"
    return "- (No prev data)"

delta_milk = get_percentage_change(total_milk, prev_month_total_milk)

# --- Display KPIs ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("🍶 Total Consumed", f"{total_milk/1000:.2f} L", delta=delta_milk, help="Change compared to the previous month.")
kpi2.metric("💰 Estimated Cost", f"₹{total_pay:,.2f}")
kpi3.metric("✅ Received Days", f"{month_data[month_data['Milk Received?']=='Yes'].shape[0]} / {len(month_data)}")
st.markdown("---")


# --- Tabbed Layout ---
tab1, tab2 = st.tabs(["🗓️ Monthly Overview", "📊 Consumption Analysis"])

with tab1:
    st.subheader("Cumulative Progress")
    month_data = month_data.sort_values('Date of Record')
    month_data['Cumulative'] = month_data[col_name].cumsum()

    fig_progress = go.Figure()
    fig_progress.add_trace(go.Scatter(x=month_data['Date of Record'], y=month_data['Cumulative'], mode='lines+markers', name='Actual Consumption', line=dict(color=theme['primary_color'], width=4)))
    if not prev_month_data.empty:
        prev_month_data = prev_month_data.sort_values('Date of Record')
        prev_month_data['Cumulative'] = prev_month_data[col_name].cumsum()
        # Align day numbers for comparison
        prev_month_data['Day'] = prev_month_data['Date of Record'].dt.day
        month_data['Day'] = month_data['Date of Record'].dt.day
        merged_data = pd.merge(month_data, prev_month_data, on='Day', how='left', suffixes=('', '_prev'))
        fig_progress.add_trace(go.Scatter(x=merged_data['Date of Record'], y=merged_data['Cumulative_prev'], mode='lines', name='Previous Month', line=dict(color='grey', dash='dash', width=2)))

    fig_progress.update_layout(template=theme['plotly_template'], height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_progress, use_container_width=True)
    
    st.subheader("Daily Milk Received Trend")
    fig_line = px.bar(month_data, x='Date of Record', y=col_name, labels={'Date of Record': 'Date', col_name: 'Milk (ml)'})
    fig_line.update_traces(marker_color=theme['primary_color'])
    fig_line.update_layout(template=theme['plotly_template'])
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Milk Received Ratio")
        status_count = month_data['Milk Received?'].value_counts().reset_index()
        fig_pie = px.pie(status_count, names='Milk Received?', values='count', hole=0.6, color='Milk Received?', color_discrete_map={'Yes': theme['primary_color'], 'No': theme['secondary_color']})
        fig_pie.update_traces(textposition='outside', textinfo='percent+label')
        fig_pie.update_layout(showlegend=False, height=350, template=theme['plotly_template'])
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.subheader("Consumption by Day of Week")
        month_data.loc[:, 'weekday_name'] = month_data['Date of Record'].dt.day_name()
        weekday_avg = month_data.groupby('weekday_name')[col_name].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
        fig_weekday = px.bar(weekday_avg, x='weekday_name', y=col_name, labels={'weekday_name': 'Day of Week', col_name: 'Avg Milk (ml)'}, text_auto='.0f')
        fig_weekday.update_layout(height=350, template=theme['plotly_template'])
        fig_weekday.update_traces(marker_color=theme['primary_color'])
        st.plotly_chart(fig_weekday, use_container_width=True)

    st.markdown("---")
    st.subheader("Raw Data for " + selected_month_name)
    display_df = month_data[['Date of Record', 'Milk Received?', col_name]].sort_values(by='Date of Record').copy()
    display_df['Date of Record'] = display_df['Date of Record'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df, use_container_width=True, height=350)

