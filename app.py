import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Streamlit Page Config
st.set_page_config(
    page_title="Today's Sky 🌞 - Weather & AQI Tracker",
    page_icon="☁️",
    layout="centered"
)

# Inject Meta Tags for SEO
meta_tags = """
<head>
    <meta name="description" content="Get real-time weather & air quality index (AQI) insights worldwide. Accurate forecasts & pollution data for better travel planning!">
    <meta name="keywords" content="weather, air quality, AQI, pollution, forecast, climate, Streamlit">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="Today's Sky - Weather & AQI">
    <meta property="og:description" content="Live weather updates & AQI tracker for cities worldwide.">
    <meta property="og:image" content="https://yourwebsite.com/preview-image.png">
    <meta property="og:url" content="https://yourwebsite.com">
    <meta name="twitter:card" content="summary_large_image">
</head>
"""
st.markdown(meta_tags, unsafe_allow_html=True)

# Inject Google Analytics
ga_script = """
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'YOUR_GA_ID');
</script>
"""
st.markdown(ga_script, unsafe_allow_html=True)

# Convert UTC to IST
def utc_to_ist(utc_time):
    utc_dt = datetime.utcfromtimestamp(utc_time)
    ist_timezone = pytz.timezone("Asia/Kolkata")
    ist_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    return ist_dt.strftime("%I:%M %p")

# Cache API Calls
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_weather_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

@st.cache_data(ttl=300)
def get_aqi_data(lat, lon, api_key):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

@st.cache_data(ttl=300)
def get_forecast_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

# AQI Levels
def aqi_review(value):
    if value <= 50: return "Good 🟢", "Air quality is satisfactory."
    elif value <= 100: return "Moderate 🟡", "Air quality is acceptable."
    elif value <= 150: return "Unhealthy for Sensitive Groups 🟠", "Sensitive people should take precautions."
    elif value <= 200: return "Unhealthy 🔴", "Everyone may experience health effects."
    elif value <= 300: return "Very Unhealthy 🟣", "Health alert for all people."
    else: return "Hazardous ⚫", "Emergency conditions, avoid outdoor activity."

# Streamlit UI
st.title("☁️ Today's Sky 🌞")
st.write("📍 Weather & AQI insights—anywhere, anytime! 🌅")

city = st.text_input("Enter City Name:")

if city:
    with st.spinner("Fetching data..."):
        data = get_weather_data(city, API_KEY)
        if data:
            st.subheader(f"Current Weather in {data['name']} 🌤️")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🌡️ Temperature", f"{data['main']['temp']} °C")
            col2.metric("🌤️ Weather", data['weather'][0]['description'].capitalize())
            col3.metric("💧 Humidity", f"{data['main']['humidity']}%")
            col4.metric("💨 Wind Speed", f"{data['wind']['speed']} m/s")
            
            st.metric("🌅 Sunrise", utc_to_ist(data['sys']['sunrise']))
            st.metric("🌇 Sunset", utc_to_ist(data['sys']['sunset']))

            lat, lon = data['coord']['lat'], data['coord']['lon']
            aqi_data = get_aqi_data(lat, lon, API_KEY)
            if aqi_data:
                st.subheader("Air Quality Index (AQI) 🌫️")
                aqi_value = aqi_data['list'][0]['main']['aqi']
                pm2_5 = aqi_data['list'][0]['components']['pm2_5']
                level, health_implication = aqi_review(pm2_5)
                
                st.metric("🌫️ PM2.5 AQI", f"{pm2_5} µg/m³", level)
                st.write(f"### Health Implication: {health_implication}")

            forecast_data = get_forecast_data(city, API_KEY)
            if forecast_data:
                st.subheader("5-Day Weather Forecast 📅")
                for i in range(0, len(forecast_data['list']), 8):
                    forecast = forecast_data['list'][i]
                    date = datetime.utcfromtimestamp(forecast['dt'])
                    st.write(f"📅 **{date.strftime('%A, %d-%m-%Y')}**")
                    st.metric("🌡️ Temp", f"{forecast['main']['temp']}°C")
                    st.metric("🌤️ Weather", forecast['weather'][0]['description'].capitalize())

st.markdown("---")
st.write("💡 **Tip:** Check the weather before stepping out! 🚀")
st.write("Made with ❤️ using Streamlit by AP Bhattacharya")

