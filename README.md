🥛 Intelligent Milk Dashboard
Ek smart aur interactive Streamlit dashboard jo aapke daily milk consumption, kharch, aur aadaton ko track aur analyze karta hai. Yeh dashboard Google Sheet se live data leta hai aur use behtareen charts aur insights mein badal deta hai.

Dashboard ka Ek Jhalak (Screenshots)
Yeh demo screenshots hain. Jab aapke paas sheet mein aacha data ho jaaye, to aap inko apne actual dashboard ke screenshots se badal sakte hain.

<p align="center">
<b>Dark Mode 🌑</b>




<img src="https://www.google.com/url?sa=E&source=gmail&q=https://i.imgur.com/2zZ0w8g.png" alt="Dark Mode Screenshot" width="80%">
</p>
<p align="center">
<b>Light Mode ☀️</b>




<img src="https://www.google.com/url?sa=E&source=gmail&q=https://i.imgur.com/rN2J2f2.png" alt="Light Mode Screenshot" width="80%">
</p>

✨ Features
Interactive UI: Ek clean aur modern user interface jo istemal karne mein aasan hai.

Light & Dark Mode: Apni pasand ke anusaar light ya dark theme chunein.

Live Data: Google Sheet se real-time mein data fetch karta hai.

Smart KPIs: Ek nazar mein zaroori jaankari jaise:

Kul Kitna Doodh Aaya (Total Consumption)

Kul Kitna Kharch Hua (Estimated Cost)

Mahine ka Anumanit Kharch (Monthly Forecast)

Aadat Tracking (Habit Tracking):

Streak Analysis: Lagataar kitne din doodh liya, uska record rakhta hai.

Dynamic Filters: Saal aur Mahine ke hisab se data filter karein.

Dynamic Pricing: Doodh ka price badalne par use aasani se sidebar se update karein.

Behtareen Visuals:

Calendar Heatmap: Poore mahine ka consumption ek calendar view mein dekhein.

Daily Trend Chart: Roz ka consumption track karein.

Day-wise Analysis: Hafte ke kis din average consumption zyada ya kam rehta hai, woh dekhein.

Ratio Pie Chart: Kitne din doodh liya aur kitne din miss hua, uska anupat (ratio) dekhein.

🛠️ Technology Stack
🚀 Is Project ko Apne Computer par Kaise Chalayein
Is dashboard ko apne local machine par chalane ke liye yeh steps follow karein:

1. Repository ko Clone Karein:

git clone [https://github.com/Kanaiya-rgb/streamlit-milk-dashboard.git](https://github.com/Kanaiya-rgb/streamlit-milk-dashboard.git)
cd streamlit-milk-dashboard

2. Zaroori Libraries Install Karein:
Ek requirements.txt file banayein aur usmein yeh likhein:

streamlit
pandas
plotly

Phir terminal mein yeh command chalayein:

pip install -r requirements.txt

3. Google Sheet Setup Karein:

Ek Google Sheet banayein jismein yeh columns hon: Date of Record, Milk Received?, How much milk received? (ml/Liters), Month.

Apni sheet ko File > Share > Publish to the web par jaakar .csv format mein publish karein aur uska link copy karein.

milk_dashboard.py file mein sheet_url variable ki value ko apne naye link se badal dein.

4. Streamlit App Chalayein:
Apne terminal mein yeh command dein:

streamlit run milk_dashboard.py

Aapka browser ek naye tab mein khulega jahan dashboard live hoga.

📄 Data Source
Yeh dashboard data ke liye ek public Google Sheet ka istemal karta hai. Data entry ke liye sheet ka structure neeche diye gaye format mein hona chahiye:

Date of Record

Milk Received?

How much milk received? (ml/Liters)

Month

1-Oct-2025

Yes

500

10

2-Oct-2025

No

0

10

👤 Author
Kanaiya

GitHub: @Kanaiya-rgb

