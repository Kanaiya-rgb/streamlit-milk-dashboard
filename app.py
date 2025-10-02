import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calendar import month_name
from datetime import datetime

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Intelligent Milk Dashboard",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("Settings & Filters")
st.sidebar.markdown("---")
# Add theme toggle at the top
dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode", value=True)

# --- THEME AND STYLING ---
if dark_mode:
    theme = {
        "bg_color": "#1a1a1a", "main_bg_color": "#262730", "metric_bg_color": "#333333",
        "text_color": "#FAFAFA", "primary_color": "#3399FF", "secondary_color": "#FF6B6B",
        "plotly_template": "plotly_dark"
    }
else:
    theme = {
        "bg_color": "#f0f2f6", "main_bg_color": "#FFFFFF", "metric_bg_color": "#FAFAFA",
        "text_color": "#31333F", "primary_color": "#0068C9", "secondary_color": "#D62728",
        "plotly_template": "plotly_white"
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
    .stAlert {{
        border-radius: 12px;
    }}
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data(ttl=300)
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
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
month_map = {i: month_name[i] for i in range(1, 13)}
available_months = sorted(df[df['Year'] == selected_year]['Month'].unique())
available_month_names = [month_map[m] for m in available_months]
selected_month_name = st.sidebar.selectbox("Select Month", available_month_names, index=len(available_month_names)-1)
selected_month_num = list(month_map.keys())[list(month_map.values()).index(selected_month_name)]

price_per_500ml = st.sidebar.number_input("Price per 500 ml (₹)", min_value=1.0, value=32.5, step=0.5)
monthly_goal = st.sidebar.number_input("Monthly Goal (Liters)", min_value=1.0, value=15.0, step=0.5)
goal_ml = monthly_goal * 1000

# --- Data Filtering ---
month_data = df[(df['Year'] == selected_year) & (df['Month'] == selected_month_num)].sort_values('Date of Record').copy()
col_name = "How much milk received? (ml/Liters)"

# --- Main Dashboard Area ---
st.title(f"🥛 Intelligent Milk Dashboard: {selected_month_name} {selected_year}")
st.markdown("An interactive analysis of your daily milk consumption, costs, and habits.")
st.markdown("---")

# --- KPI Calculations ---
total_milk = int(month_data[col_name].sum())
total_pay = (total_milk / 500) * price_per_500ml

# Month-over-Month Comparison
prev_month_year, prev_month_num = (selected_year, selected_month_num - 1) if selected_month_num > 1 else (selected_year - 1, 12)
prev_month_total_milk = int(df[(df['Year'] == prev_month_year) & (df['Month'] == prev_month_num)][col_name].sum())
delta_milk = f"{((total_milk - prev_month_total_milk) / prev_month_total_milk) * 100:.1f}%" if prev_month_total_milk > 0 else "N/A"

# Forecast Calculation
days_passed = len(month_data)
avg_daily = total_milk / days_passed if days_passed > 0 else 0
forecast = avg_daily * pd.Period(f'{selected_year}-{selected_month_num}-01').days_in_month if avg_daily > 0 else 0

# --- Sidebar Goal Progress ---
st.sidebar.markdown("---")
st.sidebar.subheader("Goal Progress")
progress = min(total_milk / goal_ml, 1.0) if goal_ml > 0 else 0
st.sidebar.progress(progress)
st.sidebar.markdown(f"**{total_milk/1000:.2f} L** of **{goal_ml/1000:.1f} L** goal achieved.")

# --- Display KPIs ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("🍶 Total Consumed", f"{total_milk/1000:.2f} L", delta=delta_milk, help="Change vs. previous month.")
kpi2.metric("💰 Estimated Cost", f"₹{total_pay:,.2f}")
kpi3.metric("📈 Forecasted Total", f"{forecast/1000:.2f} L", help="Estimated total consumption for the month.")

# --- Smart Insights Section ---
st.markdown("---")
st.subheader("Smart Insights")
month_data['weekday_name'] = month_data['Date of Record'].dt.day_name()
weekday_avg = month_data.groupby('weekday_name')[col_name].mean()
peak_day = weekday_avg.idxmax()
missed_days = len(month_data[month_data['Milk Received?'] == 'No'])

insight1, insight2 = st.columns(2)
with insight1:
    st.info(f"**Peak Consumption Day:** You tend to consume the most milk on **{peak_day}s**.")
with insight2:
    st.warning(f"**Missed Days:** You missed receiving milk on **{missed_days}** days this month.")

st.markdown("---")

# --- Charting Section ---
left_col, right_col = st.columns((2,1))

with left_col:
    st.subheader("Cumulative Consumption vs. Previous Month")
    month_data['Cumulative'] = month_data[col_name].cumsum()
    
    fig_progress = go.Figure()
    fig_progress.add_trace(go.Scatter(x=month_data['Date of Record'].dt.day, y=month_data['Cumulative'], mode='lines+markers', name='Current Month', line=dict(color=theme['primary_color'], width=4)))
    
    prev_month_data = df[(df['Year'] == prev_month_year) & (df['Month'] == prev_month_num)].sort_values('Date of Record').copy()
    if not prev_month_data.empty:
        prev_month_data['Cumulative'] = prev_month_data[col_name].cumsum()
        fig_progress.add_trace(go.Scatter(x=prev_month_data['Date of Record'].dt.day, y=prev_month_data['Cumulative'], mode='lines', name='Previous Month', line=dict(color='grey', dash='dash', width=2)))
    
    fig_progress.update_layout(template=theme['plotly_template'], height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title="Day of Month")
    st.plotly_chart(fig_progress, use_container_width=True)

with right_col:
    st.subheader("Consumption by Day")
    weekday_avg_df = weekday_avg.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
    fig_weekday = px.bar(weekday_avg_df, x='weekday_name', y=col_name, labels={'weekday_name': 'Day', col_name: 'Avg Milk (ml)'}, text_auto='.0f')
    fig_weekday.update_layout(height=400, template=theme['plotly_template'])
    fig_weekday.update_traces(marker_color=theme['primary_color'])
    st.plotly_chart(fig_weekday, use_container_width=True)

# --- Raw Data Table ---
st.markdown("---")
with st.expander("Show Raw Data for " + selected_month_name):
    display_df = month_data[['Date of Record', 'Milk Received?', col_name]].sort_values(by='Date of Record', ascending=False).copy()
    display_df['Date of Record'] = display_df['Date of Record'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df, use_container_width=True, height=350)

