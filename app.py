import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calendar import month_name
import numpy as np

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Milk Records Dashboard",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("Filters & Settings")
st.sidebar.markdown("---")
# Placeholder for filters, will be populated after data loading
# Add theme toggle at the top
dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode", value=True)

# --- THEME AND STYLING ---
if dark_mode:
    theme = {
        "bg_color": "#1a1a1a",
        "main_bg_color": "#262730",
        "metric_bg_color": "#333333",
        "text_color": "#FAFAFA",
        "primary_color": "#3399FF", # A bright blue for accents
        "secondary_color": "#FF6B6B", # A warm red for negative/missed
        "plotly_template": "plotly_dark"
    }
else:
    theme = {
        "bg_color": "#f0f2f6",
        "main_bg_color": "#FFFFFF",
        "metric_bg_color": "#FAFAFA",
        "text_color": "#31333F",
        "primary_color": "#0068C9", # A deeper blue for light mode
        "secondary_color": "#D62728",
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
    .stPlotlyChart {{
        border-radius: 12px;
        overflow: hidden;
        background-color: transparent;
    }}
    button[data-baseweb="tab"] {{
        font-size: 16px;
        font-weight: 500;
        border-radius: 8px;
        margin: 2px;
        background-color: transparent;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        background-color: {theme['primary_color']};
        color: white;
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
    return df

# --- Main App ---
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data from Google Sheet: {e}")
    st.stop()

if df.empty:
    st.error("No data could be loaded. The Google Sheet might be empty or in an incorrect format.")
    st.stop()

# --- Populate Sidebar Filters ---
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
year_data = df[df['Year'] == selected_year].copy()
month_map = {i: month_name[i] for i in range(1, 13)}
year_data.loc[:, 'Month_Name'] = year_data['Month'].map(month_map)
selected_month_name = st.sidebar.selectbox("Select Month", sorted(year_data['Month_Name'].unique(), key=lambda m: list(month_map.values()).index(m)))
month_data = year_data[year_data['Month_Name'] == selected_month_name].copy()

st.sidebar.markdown("---")
st.sidebar.subheader("Monthly Goal")
monthly_goal = st.sidebar.number_input("Set Goal (Liters)", min_value=1.0, value=15.0, step=0.5)
goal_ml = monthly_goal * 1000

if month_data.empty:
    st.warning("No data available for the selected period.")
    st.stop()

# --- Main Dashboard Area ---
st.title(f"🥛 Milk Dashboard: {selected_month_name} {selected_year}")
st.markdown("An interactive analysis of your daily milk consumption and estimated costs.")
st.markdown("---")

# --- Top Row KPIs ---
col_name = "How much milk received? (ml/Liters)"
total_milk = int(month_data[col_name].sum())
total_pay = (total_milk / 500) * 32.5
milk_received_days = month_data[month_data['Milk Received?']=='Yes'].shape[0]
total_days_in_month = month_data.shape[0]
avg_consumption = month_data[month_data[col_name] > 0][col_name].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("🍶 Total Consumed", f"{total_milk/1000:.2f} L")
kpi2.metric("💰 Estimated Cost", f"₹{total_pay:,.2f}")
kpi3.metric("✅ Received Days", f"{milk_received_days} / {total_days_in_month}")
kpi4.metric("📊 Avg. Daily Intake", f"{avg_consumption:,.0f} ml" if pd.notna(avg_consumption) else "0 ml")
st.markdown("---")

# --- Tabbed Layout ---
tab1, tab2, tab3 = st.tabs(["🗓️ Monthly Overview", "📊 Consumption Analysis", "📈 Historical View"])

with tab1:
    st.subheader("Cumulative Progress vs. Goal")
    month_data = month_data.sort_values('Date of Record')
    month_data['Cumulative'] = month_data[col_name].cumsum()
    days_in_month = len(month_data)
    month_data['Goal_Line'] = np.linspace(start=0, stop=goal_ml, num=days_in_month)

    fig_progress = go.Figure()
    fig_progress.add_trace(go.Scatter(x=month_data['Date of Record'], y=month_data['Cumulative'], mode='lines+markers', name='Actual Consumption', line=dict(color=theme['primary_color'], width=4)))
    fig_progress.add_trace(go.Scatter(x=month_data['Date of Record'], y=month_data['Goal_Line'], mode='lines', name='Target Goal Line', line=dict(color=theme['text_color'], dash='dash', width=2)))
    fig_progress.update_layout(template=theme['plotly_template'], height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_progress, use_container_width=True)
    
    st.subheader("Daily Milk Received Trend")
    fig_line = px.line(month_data, x='Date of Record', y=col_name, markers=True, labels={'Date of Record': 'Date', col_name: 'Milk (ml)'})
    fig_line.update_traces(marker=dict(size=8), line=dict(width=3, color=theme['primary_color']))
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
        
        st.subheader("Consumption by Day of Week")
        month_data.loc[:, 'weekday_name'] = month_data['Date of Record'].dt.day_name()
        weekday_avg = month_data.groupby('weekday_name')[col_name].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
        fig_weekday = px.bar(weekday_avg, x='weekday_name', y=col_name, labels={'weekday_name': 'Day of Week', col_name: 'Avg Milk (ml)'}, text_auto='.0f')
        fig_weekday.update_layout(height=350, template=theme['plotly_template'])
        fig_weekday.update_traces(marker_color=theme['primary_color'])
        st.plotly_chart(fig_weekday, use_container_width=True)

    with col2:
        st.subheader("Monthly Goal Progress")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta", value = total_milk,
            title = {'text': "Consumption Goal (ml)"},
            gauge = {'axis': {'range': [None, goal_ml]}, 'bar': {'color': theme['primary_color']}},
            delta = {'reference': goal_ml, 'increasing': {'color': theme['secondary_color']}, 'decreasing': {'color': theme['primary_color']}}
        ))
        fig_gauge.update_layout(height=350, template=theme['plotly_template'])
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.subheader("Raw Data for " + selected_month_name)
        st.dataframe(month_data[['Date of Record', 'Milk Received?', col_name]].sort_values(by='Date of Record'), use_container_width=True, height=350)

with tab3:
    st.subheader(f"Year-over-Year Comparison for {selected_month_name}")
    selected_month_num = list(month_map.keys())[list(month_map.values()).index(selected_month_name)]
    historical_data = df[df['Date of Record'].dt.month == selected_month_num]
    yearly_summary = historical_data.groupby('Year')[col_name].sum().reset_index()

    if len(yearly_summary) > 1:
        fig_yoy = px.bar(yearly_summary, x='Year', y=col_name, text_auto=True, labels={'Year': 'Year', col_name: 'Total Milk (Liters)'})
        fig_yoy.update_traces(marker_color=theme['primary_color'], texttemplate='%{y/1000:.2f} L', textposition='outside')
        fig_yoy.update_layout(template=theme['plotly_template'], yaxis_title="Total Milk (ml)")
        st.plotly_chart(fig_yoy, use_container_width=True)
    else:
        st.info(f"Not enough data for a year-over-year comparison for {selected_month_name}. Data is only available for {selected_year}.")

    st.subheader("Daily Consumption Over the Years")
    fig_hist = px.histogram(historical_data, x='Date of Record', y=col_name, nbins=30, labels={'Date of Record': 'Date', col_name: 'Milk (ml)'}, title="Daily Milk Consumption Distribution")
    fig_hist.update_layout(template=theme['plotly_template'], height=500)   