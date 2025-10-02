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
        background-color: #f0f2f6; /* Lighter gray */
    }
    /* Metric cards styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    /* Chart container styling */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
        background-color: #ffffff;
        padding: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    /* Streamlit tabs styling */
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 500;
        border-radius: 8px;
        margin: 2px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #e6f1ff;
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
st.sidebar.title("Filters & Settings")
st.sidebar.markdown("---")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
year_data = df[df['Year'] == selected_year]

if 'Month' not in df.columns:
    st.error("The 'Month' column is missing from your Google Sheet.")
    st.stop()
    
# Convert numeric month to month name for better display
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
kpi1.metric("Total Milk Consumed", f"{total_milk/1000:.2f} L")
kpi2.metric("Estimated Cost", f"₹{total_pay:,.2f}")
kpi3.metric("Milk Received Days", f"{milk_received_days} / {total_days_in_month}")
kpi4.metric("Avg. Daily Intake", f"{avg_consumption:,.0f} ml" if pd.notna(avg_consumption) else "0 ml")
st.markdown("---")

# --- Tabbed Layout ---
tab1, tab2, tab3 = st.tabs(["🗓️ Monthly Overview", "📊 Consumption Analysis", "📈 Historical View"])

with tab1:
    st.subheader("Monthly Consumption Calendar")
    month_data.loc[:, 'weekday'] = month_data['Date of Record'].dt.dayofweek
    month_data.loc[:, 'week_of_month'] = (month_data['Date of Record'].dt.day - 1) // 7
    calendar_data = month_data.pivot_table(index='week_of_month', columns='weekday', values=col_name, aggfunc='sum').fillna(0)
    for i in range(7):
        if i not in calendar_data.columns: calendar_data[i] = 0
    calendar_data = calendar_data[[0,1,2,3,4,5,6]]
    
    fig_cal = go.Figure(data=go.Heatmap(
        z=calendar_data.values,
        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        y=[f"Week {i+1}" for i in calendar_data.index],
        colorscale='Greens', hoverongaps=False,
        hovertemplate='<b>Milk: %{z:.0f} ml</b><extra></extra>'
    ))
    fig_cal.update_layout(height=300, yaxis_title=None, xaxis_title=None, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_cal, use_container_width=True)
    
    st.subheader("Daily Milk Received Trend")
    fig_line = px.line(month_data, x='Date of Record', y=col_name, markers=True, labels={'Date of Record': 'Date', col_name: 'Milk (ml)'})
    fig_line.update_traces(marker=dict(size=8), line=dict(width=3, color='#2ca02c'))
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Milk Received Ratio")
        status_count = month_data['Milk Received?'].value_counts().reset_index()
        fig_pie = px.pie(status_count, names='Milk Received?', values='count', hole=0.5, color='Milk Received?', color_discrete_map={'Yes':'#2ca02c', 'No':'#d62728'})
        fig_pie.update_traces(textposition='outside', textinfo='percent+label')
        fig_pie.update_layout(showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.subheader("Consumption by Day of Week")
        month_data.loc[:, 'weekday_name'] = month_data['Date of Record'].dt.day_name()
        weekday_avg = month_data.groupby('weekday_name')[col_name].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
        fig_weekday = px.bar(weekday_avg, x='weekday_name', y=col_name, labels={'weekday_name': 'Day of Week', col_name: 'Avg Milk (ml)'}, text_auto='.0f')
        fig_weekday.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_weekday.update_traces(marker_color='#2ca02c')
        st.plotly_chart(fig_weekday, use_container_width=True)

    with col2:
        st.subheader("Monthly Goal Progress")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = total_milk,
            title = {'text': "Consumption Goal (ml)"},
            gauge = {'axis': {'range': [None, goal_ml]}, 'bar': {'color': "#2ca02c"}},
            delta = {'reference': goal_ml, 'increasing': {'color': "#d62728"}, 'decreasing': {'color': "green"}}
        ))
        fig_gauge.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
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
        fig_yoy.update_traces(marker_color='#2ca02c', texttemplate='%{y/1000:.2f} L', textposition='outside')
        fig_yoy.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Total Milk (ml)")
        st.plotly_chart(fig_yoy, use_container_width=True)
    else:
        st.info(f"Not enough data for a year-over-year comparison for {selected_month_name}. Data is only available for {selected_year}.")

