import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calendar import month_name

# --- Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Milk Records Dashboard",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    /* Main app background */
    .main {
        background-color: #f5f5f5;
    }
    /* Metric cards styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.08);
    }
    /* Chart container styling */
    .stPlotlyChart {
        border-radius: 10px;
        overflow: hidden;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)


# --- Data Loading for Milk Dashboard ---
@st.cache_data(ttl=600) # Cache data for 10 minutes
def load_data():
    """Loads and cleans the Milk Records data from a Google Sheet URL."""
    sheet_url = 'https://docs.google.com/spreadsheets/d/1tAnw43L2nrF-7wGqqppF51w6tE8w42qhmPKSXBO3fmo/export?format=csv'
    
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    col_name = "How much milk received? (ml/Liters)"
    
    if col_name in df.columns:
        df[col_name] = df[col_name].astype(str).str.replace('ml', '', regex=False).str.strip()
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0).astype(int)
        
    df['Date of Record'] = pd.to_datetime(df['Date of Record'], errors='coerce')
    df.dropna(subset=['Date of Record'], inplace=True)
    df['Year'] = df['Date of Record'].dt.year
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

# --- Sidebar for Filters ---
st.sidebar.title("Filters")
st.sidebar.markdown("---")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
year_data = df[df['Year'] == selected_year]

if 'Month' not in df.columns:
    st.error("The 'Month' column is missing from your Google Sheet.")
    st.stop()
    
# Convert numeric month to month name for better display
month_map = {i: month_name[i] for i in range(1, 13)}
year_data['Month_Name'] = year_data['Month'].map(month_map)

selected_month_name = st.sidebar.selectbox("Select Month", sorted(year_data['Month_Name'].unique(), key=lambda m: list(month_map.values()).index(m)))
month_data = year_data[year_data['Month_Name'] == selected_month_name].copy()

if month_data.empty:
    st.warning("No data available for the selected period.")
    st.stop()

# --- Main Dashboard Area ---
st.title(f"🥛 Milk Dashboard for {selected_month_name} {selected_year}")
st.markdown("An overview of your daily milk consumption and estimated costs.")
st.markdown("---")

# --- Top Row KPIs ---
col_name = "How much milk received? (ml/Liters)"
total_milk = int(month_data[col_name].sum())
total_pay = (total_milk / 500) * 32.5
milk_received_days = month_data[month_data['Milk Received?']=='Yes'].shape[0]
total_days_in_month = month_data.shape[0]
avg_consumption = month_data[month_data[col_name] > 0][col_name].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Milk Consumed", f"{total_milk/1000:.2f} L")
kpi2.metric("Estimated Cost", f"₹{total_pay:,.2f}")
kpi3.metric("Milk Received Days", f"{milk_received_days} / {total_days_in_month}")
kpi4.metric("Avg. Daily Intake", f"{avg_consumption:,.0f} ml" if pd.notna(avg_consumption) else "0 ml")

st.markdown("---")

# --- Main Page Charts ---
col1, col2 = st.columns((2, 1)) # Give more space to the left column

with col1:
    st.subheader("🗓️ Monthly Consumption Calendar")
    # Calendar Heatmap Logic
    month_data['weekday'] = month_data['Date of Record'].dt.dayofweek
    month_data['week_of_month'] = (month_data['Date of Record'].dt.day - 1) // 7
    calendar_data = month_data.pivot_table(index='week_of_month', columns='weekday', values=col_name, aggfunc='sum').fillna(0)
    # Ensure all weekdays are present
    for i in range(7):
        if i not in calendar_data.columns:
            calendar_data[i] = 0
    calendar_data = calendar_data[[0,1,2,3,4,5,6]] # Sort columns Mon-Sun
    
    fig_cal = go.Figure(data=go.Heatmap(
        z=calendar_data.values,
        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        y=[f"Week {i+1}" for i in calendar_data.index],
        colorscale='Greens',
        hoverongaps=False,
        hovertemplate='<b>Milk: %{z:.0f} ml</b><extra></extra>'
    ))
    fig_cal.update_layout(title="Hover over a day to see consumption", title_font_size=14, yaxis_title=None, xaxis_title=None)
    st.plotly_chart(fig_cal, use_container_width=True)
    
    st.subheader("📈 Daily Milk Received Trend")
    fig_line = px.line(month_data, x='Date of Record', y=col_name, markers=True, labels={'Date of Record': 'Date', col_name: 'Milk (ml)'})
    fig_line.update_traces(marker=dict(size=8), line=dict(width=3))
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("📊 Milk Received Ratio")
    status_count = month_data['Milk Received?'].value_counts().reset_index()
    fig_pie = px.pie(status_count, names='Milk Received?', values='count', hole=0.5, color='Milk Received?', color_discrete_map={'Yes':'#2ca02c', 'No':'#d62728'})
    fig_pie.update_traces(textposition='outside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("🎯 Monthly Goal")
    goal = 15000 # 15 Liters goal
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_milk,
        title = {'text': "Consumption Goal (ml)"},
        gauge = {'axis': {'range': [None, goal]},
                 'bar': {'color': "#2ca02c"},
                 'steps' : [
                     {'range': [0, goal * 0.5], 'color': "lightgray"},
                     {'range': [goal * 0.5, goal * 0.8], 'color': "gray"}],
                 }))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gauge, use_container_width=True)

