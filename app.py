import streamlit as st
import streamlit.components.v1 as components
import requests
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime

# Set wide layout and inject animation
st.set_page_config(page_title="Today's Sky",page_icon="🌤️", layout="wide")

particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 500,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "image",
          "image": {
            "src": "https://cdn-icons-png.flaticon.com/512/4151/4151111.png",
            "width": 100,
            "height": 100
          }
        },

        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 1,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""

components.html(particles_js, height=300, width=0)

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Function to convert UTC time to IST
def utc_to_ist(utc_time):
    utc_dt = datetime.utcfromtimestamp(utc_time)
    ist_timezone = pytz.timezone("Asia/Kolkata")
    ist_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    return ist_dt.strftime("%I:%M %p")

# Function to get current weather data
def get_weather_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "City not found! Please check the spelling or try another city."
        else:
            return None, f"Error {response.status_code}: Unable to fetch weather data."
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"

# Function to get AQI data
def get_aqi_data(lat, lon, api_key):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, "AQI data not available."
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"

# Function to get 5-day forecast data
def get_forecast_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "Forecast data not available for this city."
        else:
            return None, f"Error {response.status_code}: Unable to fetch forecast data."
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"

# Function to get AQI level description
def aqi_review(value):
    if value <= 50:
        return "Good 🟢", "normal", "Air quality is considered satisfactory, and air pollution poses little or no risk."
    elif value <= 100:
        return "Moderate 🟡", "normal", "Air quality is acceptable; however, there may be a moderate health concern for a very small number of people who are sensitive to air pollution."
    elif value <= 150:
        return "Unhealthy for Sensitive Groups 🟠", "normal", "Members of sensitive groups (e.g., children, elderly, and people with respiratory conditions) may experience health effects."
    elif value <= 200:
        return "Unhealthy 🔴", "inverse", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
    elif value <= 300:
        return "Very Unhealthy 🟣", "inverse", "Health alert: everyone may experience more serious health effects."
    else:
        return "Hazardous ⚫", "inverse", "Health warning of emergency conditions. The entire population is more likely to be affected."

# Streamlit UI
def app():
    st.title("☁️ Today's Sky 🌞")
    st.write("📍 Weather & AQI insights—anywhere, anytime! 🌅")

    city = st.text_input("Enter City Name:")
    
    if city:
        with st.spinner("Fetching data..."):
            # Get current weather data
            data, error_message = get_weather_data(city, API_KEY)
            if data:
                st.subheader(f"Current Weather in {data['name']} 🌤️")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🌡️ Temperature", f"{data['main']['temp']} °C")
                col2.metric("🌤️ Weather", data['weather'][0]['description'].capitalize())
                col3.metric("💧 Humidity", f"{data['main']['humidity']}%")
                col4.metric("💨 Wind Speed", f"{data['wind']['speed']} m/s")
                
                col5, col6 = st.columns(2)
                col5.metric("🌅 Sunrise", utc_to_ist(data['sys']['sunrise']))
                col6.metric("🌇 Sunset", utc_to_ist(data['sys']['sunset']))

                # Get AQI data
                lat, lon = data['coord']['lat'], data['coord']['lon']
                aqi_data, aqi_error = get_aqi_data(lat, lon, API_KEY)
                
                if aqi_data:
                    st.subheader("Air Quality Index (AQI) 🌫️")
                    aqi_value = aqi_data['list'][0]['main']['aqi']
                    pm2_5 = aqi_data['list'][0]['components']['pm2_5']
                    level, style, health_implication = aqi_review(pm2_5)
                    
                    st.metric("🌫️ PM2.5 AQI", f"{pm2_5} µg/m³", level)
                    st.write("### Health Implications for PM2.5 AQI")
                    st.write(health_implication)
                    
                    st.write("### Other AQI Components:")
                    col1, col2 = st.columns(2)
                    col1.write(f"🌫️ PM10: {aqi_data['list'][0]['components']['pm10']} µg/m³")
                    col2.write(f"🧪 O3: {aqi_data['list'][0]['components']['o3']} µg/m³")
                    col1.write(f"💨 NO2: {aqi_data['list'][0]['components']['no2']} µg/m³")
                    col2.write(f"🌋 SO2: {aqi_data['list'][0]['components']['so2']} µg/m³")
                    col1.write(f"🛢️ CO: {aqi_data['list'][0]['components']['co']} µg/m³")

            elif error_message:
                st.error(error_message)
            
            # Get 5-day forecast data
            forecast_data, forecast_error = get_forecast_data(city, API_KEY)
            if forecast_data:
                st.subheader("5-Day Weather Forecast 📅")
                forecast_data = forecast_data['list']
                
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                for i in range(0, len(forecast_data), 8):  # Display one data point per day (8 intervals = 24 hours)
                    forecast = forecast_data[i]
                    date = datetime.utcfromtimestamp(forecast['dt'])
                    day_name = day_names[date.weekday()]
                    temp_min = min(f['main']['temp_min'] for f in forecast_data[i:i+8])
                    temp_max = max(f['main']['temp_max'] for f in forecast_data[i:i+8])
                    desc = forecast['weather'][0]['description'].capitalize()
                    
                    st.write(f"### 📅 **{day_name}, {date.strftime('%d-%m-%Y')}**")
                    col1, col2 = st.columns(2)
                    col1.metric("🌡️ Temp Range", f"{temp_min}°C - {temp_max}°C")
                    col2.metric("🌤️ Weather", desc)
            elif forecast_error:
                st.error(forecast_error)

    st.markdown("---")
    st.write("💡 **Tip:** The best journeys start with a quick weather check – go explore!")
    st.write("Made with ❤️ using Streamlit by AP Bhattacharya & Jagriti")

# Run the app
if __name__ == "__main__":
    app()
