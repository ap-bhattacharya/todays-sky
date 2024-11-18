# 🌤️ Today's Sky  

**Real-time Weather & AQI Insights – Anywhere, Anytime!**  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Streamlit App](https://img.shields.io/badge/Built_with-Streamlit-red)](https://streamlit.io/)  
[![API: OpenWeather](https://img.shields.io/badge/API-OpenWeather-blue)](https://openweathermap.org/)  

**Today's Sky** is a user-friendly weather application providing accurate weather updates and air quality information for any city worldwide. Whether you're planning your next trip or simply staying informed, this app is your go-to for everything about the sky above!  

---

## 🌟 **Features at a Glance**  

### 🌤️ **Current Weather Details**  
- 🌡️ **Temperature** – Feel the weather in °C.  
- 🌤️ **Condition** – Know if it's sunny, cloudy, or rainy.  
- 💧 **Humidity** – Check moisture levels in the air.  
- 💨 **Wind Speed** – See how breezy it is.  
- 🌅 **Sunrise & Sunset** – Find out when day begins and ends.  

### 🌫️ **Air Quality Insights (AQI)**  
- **PM2.5 Levels** with detailed health implications.  
- Additional pollutants: PM10, O3, NO2, SO2, and CO.  

### 📅 **5-Day Weather Forecast**  
- 🌡️ Daily **Temperature Ranges**.  
- 🌤️ Descriptions of upcoming weather conditions.  

---

## 🌐 **Check it Live!**  

Explore the app in action: [**Today's Sky**](https://ap-todays-sky.streamlit.app/)  

---

## 💻 **Tech Stack**  

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend**: Python  
- **API Integration**: [OpenWeatherMap](https://openweathermap.org/)  
- **Environment Variables**: [dotenv](https://pypi.org/project/python-dotenv/)  

---

## 🚀 **Getting Started**  

### Prerequisites  
1. Install **Python 3.x**.  
2. Create an account on [OpenWeatherMap](https://openweathermap.org/) and generate an API Key.  
3. Install required Python libraries:  
   ```bash
   pip install streamlit python-dotenv requests pytz
   ```  

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/ap-bhattacharya/todays-sky.git
   cd todays-sky
   ```  

2. Create a `.env` file and add your OpenWeather API key:  
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```  

3. Run the app:  
   ```bash
   streamlit run app.py
   ```  

4. Access the app in your browser at `http://localhost:8501`.  

---

## 🤝 **Meet the Makers**  

This project is a collaborative effort by:  

- **Arunangshu Prasad Bhattacharya**  
  - GitHub: [ap-bhattacharya](https://github.com/ap-bhattacharya)  

- **Jagriti**  
  - GitHub: [Jagriti1703](https://github.com/Jagriti1703)  

Together, we aimed to build a simple yet powerful weather app for everyone!  

---

## 📜 **License**  

This repository is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.  

---

💡 **Tip**: *The best journeys start with a quick weather check – go explore!*  
**Made with ❤️ using Streamlit by AP Bhattacharya & Jagriti.**  
