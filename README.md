# 🥛 Intelligent Milk Dashboard

An interactive Streamlit web application that tracks and analyzes daily milk consumption patterns, costs, and habits with beautiful visualizations and insights.

## 🌟 Features

- **📊 Interactive Dashboard**: Real-time visualization of milk consumption data
- **📈 Monthly Analytics**: Track consumption trends, streaks, and patterns
- **💰 Cost Analysis**: Calculate estimated monthly costs based on consumption
- **🔥 Streak Tracking**: Monitor current and longest milk receiving streaks
- **📅 Calendar View**: Heatmap visualization of daily consumption
- **🌙 Dark/Light Mode**: Toggle between themes for better user experience
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Live Demo

🔗 **[View Live Dashboard](https://app-milk-dashboard.streamlit.app/)**

## 📸 Screenshots

### Dashboard Overview
![Dashboard](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Milk+Dashboard+Screenshot)

### Key Metrics
- **Total Consumption**: Monthly milk consumption in liters
- **Estimated Cost**: Calculated based on price per 500ml
- **Forecasted Total**: Projected monthly consumption
- **Current Streak**: Days of consecutive milk receiving

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kanaiya-rgb/streamlit-milk-dashboard.git
   cd streamlit-milk-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to view the dashboard

## 📊 Data Source

The application connects to a Google Sheets document containing milk consumption records with the following structure:

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | When the record was created | 9/30/2025 12:45:23 |
| Date of Record | Date of milk consumption | 1-Oct-2025 |
| Milk Received? | Whether milk was received | Yes/No |
| How much milk received? (ml/Liters) | Amount in ml | 500 ml |
| Month | Month number | 10 |

### Sample Data
```
Timestamp,Date of Record,Milk Received?,How much milk received? (ml/Liters),Month
9/30/2025 12:45:23,1-Oct-2025,Yes,500 ml,10
10/2/2025 8:45:23,2-Oct-2025,No,0 ml,10
```

## 🎯 Key Visualizations

### 1. Monthly Consumption Calendar
- **Heatmap** showing daily consumption patterns
- **Color-coded** intensity based on milk amount
- **Interactive** hover tooltips with exact values

### 2. Consumption vs. Missed Days
- **Pie chart** showing ratio of days with/without milk
- **Percentage breakdown** of successful vs. missed days

### 3. Daily Trends Analysis
- **Bar chart** of daily consumption amounts
- **Time series** visualization of consumption patterns

### 4. Day-of-Week Analysis
- **Average consumption** by weekday
- **Pattern identification** for weekly habits

## ⚙️ Configuration

### Sidebar Controls
- **Year Selection**: Filter data by year
- **Month Selection**: Choose specific month to analyze
- **Price Setting**: Set price per 500ml for cost calculations
- **Theme Toggle**: Switch between dark and light modes

### Customization
You can modify the Google Sheets URL in the `load_data()` function:
```python
sheet_url = 'YOUR_GOOGLE_SHEET_CSV_EXPORT_URL'
```

## 🎨 Themes

The application supports two beautiful themes:

### Dark Mode (Default)
- **Background**: Dark charcoal (#1a1a1a)
- **Cards**: Dark gray (#262730)
- **Primary**: Blue (#3399FF)
- **Secondary**: Red (#FF6B6B)

### Light Mode
- **Background**: Light gray (#f0f2f6)
- **Cards**: White (#FFFFFF)
- **Primary**: Blue (#0068C9)
- **Secondary**: Red (#D62728)

## 📱 Responsive Design

The dashboard is fully responsive and includes:
- **Mobile-friendly** layout
- **Touch-optimized** controls
- **Scalable** visualizations
- **Adaptive** sidebar

## 🔧 Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualizations**: Plotly Express & Graph Objects
- **Styling**: Custom CSS with Google Fonts
- **Data Source**: Google Sheets (CSV export)
- **Deployment**: Streamlit Cloud

## 📈 Analytics Features

### Streak Calculation
- **Current Streak**: Consecutive days of milk receiving
- **Longest Streak**: Best streak for the selected month
- **Streak Visualization**: Visual indicators in the interface

### Forecasting
- **Monthly Projection**: Based on current daily average
- **Trend Analysis**: Month-over-month comparison
- **Cost Estimation**: Projected monthly expenses

### Performance Metrics
- **Consumption Rate**: Percentage of days with milk
- **Average Daily**: Mean consumption per day
- **Monthly Totals**: Aggregated consumption data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Kanaiya**
- GitHub: [@Kanaiya-rgb](https://github.com/Kanaiya-rgb)
- Dashboard: [Live Demo](https://app-milk-dashboard.streamlit.app/)

## 🙏 Acknowledgments

- **Streamlit** for the amazing web app framework
- **Plotly** for interactive visualizations
- **Pandas** for data processing capabilities
- **Google Sheets** for easy data management

## 📞 Support

If you have any questions or need help with the dashboard, please:
1. Check the [Issues](https://github.com/Kanaiya-rgb/streamlit-milk-dashboard/issues) page
2. Create a new issue if your question isn't already answered
3. Provide detailed information about your problem

---

⭐ **Star this repository if you found it helpful!**
