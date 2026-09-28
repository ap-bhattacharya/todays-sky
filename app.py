import os
from datetime import datetime, timezone, timedelta

import requests
import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Today's Sky",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Overall page */
    .stApp {
        background: linear-gradient(180deg, #0b0f17 0%, #101622 55%, #0b0f17 100%);
    }

    .block-container {
        max-width: 1180px;
        padding: 2rem 2rem 3rem;
    }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.5rem 2.4rem 2.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,.09);
        border-radius: 28px;
        background:
            radial-gradient(circle at 85% 20%, rgba(255,193,7,.16), transparent 28%),
            radial-gradient(circle at 10% 90%, rgba(66,153,225,.13), transparent 30%),
            rgba(19, 25, 38, .82);
        box-shadow: 0 18px 50px rgba(0,0,0,.24);
    }

    .hero-kicker {
        color: #9fb0c7;
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: .55rem;
    }

    .hero-title {
        margin: 0;
        color: #f8fafc;
        font-size: clamp(2.2rem, 5vw, 4.4rem);
        line-height: .98;
        font-weight: 800;
        letter-spacing: -.04em;
    }

    .hero-subtitle {
        margin: .9rem 0 0;
        color: #b7c2d3;
        font-size: 1.05rem;
        max-width: 650px;
    }

    /* Cards */
    .card {
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 22px;
        background: rgba(19,25,38,.76);
        padding: 1.25rem;
        box-shadow: 0 12px 35px rgba(0,0,0,.18);
        margin-bottom: 1rem;
    }

    .section-title {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 750;
        margin: .25rem 0 .8rem;
    }

    .section-caption {
        color: #8f9db0;
        font-size: .9rem;
        margin-bottom: .9rem;
    }

    .weather-main-temp {
        font-size: clamp(3.4rem, 7vw, 5.6rem);
        font-weight: 800;
        line-height: .9;
        color: #ffffff;
        letter-spacing: -.06em;
    }

    .weather-location {
        color: #f8fafc;
        font-size: 1.55rem;
        font-weight: 750;
    }

    .weather-description {
        color: #aebacc;
        font-size: 1rem;
        margin-top: .25rem;
    }

    .weather-icon {
        font-size: 4.5rem;
        line-height: 1;
    }

    .mini-label {
        color: #8290a5;
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .mini-value {
        color: #eef2f7;
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: .2rem;
    }

    .aqi-score {
        font-size: 3.8rem;
        line-height: 1;
        font-weight: 800;
        color: #ffffff;
    }

    .aqi-pill {
        display: inline-block;
        padding: .35rem .75rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: .85rem;
        margin-top: .45rem;
        background: rgba(255,255,255,.09);
        color: #e9eef6;
    }

    .sun-time {
        color: #e9eef6;
        font-weight: 750;
    }

    .sun-bar {
        height: 9px;
        border-radius: 999px;
        background: linear-gradient(90deg, #52647a 0%, #f7c948 48%, #52647a 100%);
        margin: .8rem 0 .45rem;
        position: relative;
        overflow: hidden;
    }

    .sun-marker {
        position: absolute;
        top: -4px;
        width: 17px;
        height: 17px;
        border-radius: 50%;
        background: #ffffff;
        border: 3px solid #f7c948;
        box-shadow: 0 0 14px rgba(247,201,72,.7);
        transform: translateX(-50%);
    }

    .forecast-card {
        border: 1px solid rgba(255,255,255,.07);
        border-radius: 18px;
        padding: .95rem;
        background: rgba(255,255,255,.025);
        min-height: 125px;
    }

    .forecast-time {
        color: #8f9db0;
        font-size: .78rem;
        font-weight: 700;
    }

    .forecast-temp {
        color: #f8fafc;
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: .5rem;
    }

    .forecast-desc {
        color: #9eabbd;
        font-size: .78rem;
        margin-top: .2rem;
    }

    /* Streamlit controls */
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,.06) !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        border-radius: 14px !important;
        color: #fff !important;
        min-height: 48px;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        min-height: 48px;
        border-radius: 14px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,.12);
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.06);
        padding: .8rem;
        border-radius: 15px;
    }

    /* Mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem .85rem 2rem;
        }

        .hero {
            padding: 1.6rem 1.25rem;
            border-radius: 20px;
        }

        .hero-title {
            font-size: 2.65rem;
        }

        .hero-subtitle {
            font-size: .95rem;
        }

        .card {
            border-radius: 18px;
            padding: 1rem;
        }

        .weather-main-temp {
            font-size: 4rem;
        }

        .weather-icon {
            font-size: 3.4rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# API helpers
# -----------------------------------------------------------------------------
def api_get(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=12)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as exc:
        if response.status_code == 404:
            return None, "Location not found. Please check the city name."
        if response.status_code == 401:
            return None, "OpenWeather API key is invalid or not configured."
        return None, f"Weather service error ({response.status_code})."
    except requests.exceptions.RequestException as exc:
        return None, f"Network error: {exc}"


def get_weather_data(city, api_key):
    return api_get(
        "https://api.openweathermap.org/data/2.5/weather",
        {"q": city, "appid": api_key, "units": "metric"},
    )


def get_weather_by_coords(lat, lon, api_key):
    return api_get(
        "https://api.openweathermap.org/data/2.5/weather",
        {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
    )


def get_aqi_data(lat, lon, api_key):
    return api_get(
        "https://api.openweathermap.org/data/2.5/air_pollution",
        {"lat": lat, "lon": lon, "appid": api_key},
    )


def get_forecast_data(city, api_key):
    return api_get(
        "https://api.openweathermap.org/data/2.5/forecast",
        {"q": city, "appid": api_key, "units": "metric"},
    )


def get_forecast_by_coords(lat, lon, api_key):
    return api_get(
        "https://api.openweathermap.org/data/2.5/forecast",
        {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
    )


def get_ip_location():
    """Approximate 'Use my location' using the visitor's public IP.

    Streamlit's basic HTML component cannot directly return browser GPS
    coordinates to Python, so IP geolocation is used without adding another
    package/dependency. It is approximate, not device GPS.
    """
    try:
        response = requests.get("https://ipapi.co/json/", timeout=8)
        response.raise_for_status()
        data = response.json()
        if data.get("latitude") is None or data.get("longitude") is None:
            return None, "Unable to determine your approximate location."
        return data, None
    except requests.exceptions.RequestException as exc:
        return None, f"Location lookup failed: {exc}"


# -----------------------------------------------------------------------------
# Formatting helpers
# -----------------------------------------------------------------------------
def local_dt_from_timestamp(timestamp, timezone_offset_seconds=0):
    return datetime.fromtimestamp(
        timestamp, tz=timezone.utc
    ) + timedelta(seconds=timezone_offset_seconds)


def format_time(timestamp, timezone_offset_seconds=0):
    return local_dt_from_timestamp(timestamp, timezone_offset_seconds).strftime("%I:%M %p")


def format_short_time(timestamp, timezone_offset_seconds=0):
    return local_dt_from_timestamp(timestamp, timezone_offset_seconds).strftime("%I %p")


def weather_emoji(icon_code, description=""):
    mapping = {
        "01": "☀️",
        "02": "🌤️",
        "03": "☁️",
        "04": "☁️",
        "09": "🌧️",
        "10": "🌦️",
        "11": "⛈️",
        "13": "❄️",
        "50": "🌫️",
    }
    return mapping.get((icon_code or "")[:2], "🌤️")


def openweather_aqi_label(aqi):
    labels = {
        1: ("Good", "🟢", "Air quality is generally satisfactory."),
        2: ("Fair", "🟡", "Air quality is acceptable, with some pollutants at moderate levels."),
        3: ("Moderate", "🟠", "Some people may experience effects from air pollution."),
        4: ("Poor", "🔴", "Air pollution is elevated; sensitive people may be affected more."),
        5: ("Very Poor", "🟣", "Air pollution is very high; consider reducing prolonged outdoor exposure."),
    }
    return labels.get(aqi, ("Unknown", "⚪", "AQI information is unavailable."))


def sun_progress(weather):
    offset = weather.get("timezone", 0)
    sunrise = weather["sys"]["sunrise"]
    sunset = weather["sys"]["sunset"]
    now = datetime.now(timezone.utc).timestamp()
    if sunset <= sunrise:
        return 50
    progress = ((now - sunrise) / (sunset - sunrise)) * 100
    return max(0, min(100, progress))


# -----------------------------------------------------------------------------
# UI sections
# -----------------------------------------------------------------------------
def render_hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Weather • Air quality • Forecast</div>
            <h1 class="hero-title">Today's Sky ☁️</h1>
            <p class="hero-subtitle">
                Clear, useful weather insights for any city — with live conditions,
                air quality and short-term forecasts in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_current_weather(data):
    offset = data.get("timezone", 0)
    weather = data["weather"][0]
    main = data["main"]
    wind = data.get("wind", {})
    visibility_km = data.get("visibility")
    visibility_km = visibility_km / 1000 if visibility_km is not None else None

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Current weather</div>', unsafe_allow_html=True)

    left, middle, right = st.columns([1.1, 2.2, 1.5])
    with left:
        st.markdown(
            f'<div class="weather-icon">{weather_emoji(weather.get("icon"), weather.get("description"))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="weather-main-temp">{round(main["temp"])}°</div>',
            unsafe_allow_html=True,
        )
    with middle:
        st.markdown(
            f'<div class="weather-location">{data["name"]}, {data.get("sys", {}).get("country", "")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="weather-description">{weather["description"].capitalize()} · Feels like {round(main["feels_like"])}°C</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="mini-label">Humidity</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-value">💧 {main["humidity"]}%</div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="mini-label">Wind</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-value">💨 {wind.get("speed", 0)} m/s</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="mini-label">Pressure</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mini-value">{main.get("pressure", "—")} hPa</div>', unsafe_allow_html=True)
        if visibility_km is not None:
            st.markdown('<div class="mini-label" style="margin-top:.8rem">Visibility</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-value">👁️ {visibility_km:.1f} km</div>', unsafe_allow_html=True)
        st.markdown('<div class="mini-label" style="margin-top:.8rem">Updated</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mini-value">{format_time(datetime.now(timezone.utc).timestamp(), offset)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_sun_card(data):
    offset = data.get("timezone", 0)
    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]
    progress = sun_progress(data)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sunrise & sunset</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="mini-label">Sunrise</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sun-time">🌅 {format_time(sunrise, offset)}</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="mini-label">Sunset</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sun-time">🌇 {format_time(sunset, offset)}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="sun-bar"><div class="sun-marker" style="left:{progress}%;"></div></div>',
        unsafe_allow_html=True,
    )
    now = datetime.now(timezone.utc).timestamp()
    if now < sunrise:
        caption = "Before sunrise"
    elif now > sunset:
        caption = "After sunset"
    else:
        caption = "Daylight right now"
    st.caption(caption)
    st.markdown('</div>', unsafe_allow_html=True)


def render_24_hour(forecast_data, timezone_offset):
    items = forecast_data["list"][:8]
    st.markdown('<div class="section-title">Next 24 hours</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Three-hour forecast intervals from OpenWeather.</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for index, item in enumerate(items):
        with cols[index % 4]:
            time_label = format_short_time(item["dt"], timezone_offset)
            icon = weather_emoji(item["weather"][0].get("icon"))
            temp = round(item["main"]["temp"])
            rain = item.get("rain", {}).get("3h", 0)
            st.markdown(
                f"""
                <div class="forecast-card">
                    <div class="forecast-time">{time_label}</div>
                    <div style="font-size:1.8rem;margin-top:.35rem">{icon}</div>
                    <div class="forecast-temp">{temp}°C</div>
                    <div class="forecast-desc">{item['weather'][0]['description'].capitalize()}</div>
                    <div class="forecast-desc">💧 {rain:g} mm</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_temperature_chart(forecast_data, timezone_offset):
    items = forecast_data["list"][:8]
    chart_data = {
        format_short_time(item["dt"], timezone_offset): round(item["main"]["temp"], 1)
        for item in items
    }
    st.markdown('<div class="section-title">Temperature trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Expected temperature over the next 24 hours.</div>', unsafe_allow_html=True)
    st.line_chart(chart_data, height=260, y_label="°C")


def render_aqi(aqi_data):
    entry = aqi_data["list"][0]
    aqi = entry["main"].get("aqi")
    label, emoji, description = openweather_aqi_label(aqi)
    components = entry.get("components", {})

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Air quality</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">OpenWeather air pollution index and pollutant concentrations.</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 2.2])
    with left:
        st.markdown(f'<div class="aqi-score">{aqi if aqi is not None else "—"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="aqi-pill">{emoji} {label}</div>', unsafe_allow_html=True)
    with right:
        st.info(description)

    c1, c2, c3, c4, c5 = st.columns(5)
    pollutants = [
        (c1, "PM2.5", components.get("pm2_5"), "µg/m³"),
        (c2, "PM10", components.get("pm10"), "µg/m³"),
        (c3, "O₃", components.get("o3"), "µg/m³"),
        (c4, "NO₂", components.get("no2"), "µg/m³"),
        (c5, "CO", components.get("co"), "µg/m³"),
    ]
    for column, name, value, unit in pollutants:
        with column:
            st.metric(name, f"{value:g} {unit}" if value is not None else "—")

    st.markdown('</div>', unsafe_allow_html=True)


def render_5_day(forecast_data, timezone_offset):
    items = forecast_data["list"]
    # Group the 3-hour points by local calendar date.
    grouped = {}
    for item in items:
        local_date = local_dt_from_timestamp(item["dt"], timezone_offset).date()
        grouped.setdefault(local_date, []).append(item)

    st.markdown('<div class="section-title">5-day forecast</div>', unsafe_allow_html=True)
    cards = list(grouped.items())[:5]
    cols = st.columns(min(5, len(cards)))
    for index, (date_value, day_items) in enumerate(cards):
        with cols[index % len(cols)]:
            min_temp = min(x["main"]["temp_min"] for x in day_items)
            max_temp = max(x["main"]["temp_max"] for x in day_items)
            representative = day_items[len(day_items) // 2]
            icon = weather_emoji(representative["weather"][0].get("icon"))
            desc = representative["weather"][0]["description"].capitalize()
            st.markdown(
                f"""
                <div class="forecast-card">
                    <div class="forecast-time">{date_value.strftime('%a, %d %b')}</div>
                    <div style="font-size:2rem;margin-top:.35rem">{icon}</div>
                    <div class="forecast-temp">{round(min_temp)}° — {round(max_temp)}°</div>
                    <div class="forecast-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------------------
# Main application
# -----------------------------------------------------------------------------
def app():
    render_hero()

    if not API_KEY:
        st.error("OPENWEATHER_API_KEY is not configured. Add it to your .env file.")
        return

    # Search controls
    with st.form("location_form"):
        search_col, button_col = st.columns([5, 1])
        with search_col:
            city_input = st.text_input(
                "Search city",
                placeholder="Enter a city, e.g. Chandigarh",
                label_visibility="collapsed",
            )
        with button_col:
            search_clicked = st.form_submit_button("🔎 Search", use_container_width=True)

    location_col, status_col = st.columns([1.35, 3.65])
    with location_col:
        use_location = st.button("📍 Use my location", use_container_width=True)
    with status_col:
        if use_location:
            st.caption("Finding your approximate location from your public IP…")

    data = None
    forecast_data = None
    location_name = None

    # Explicit city search takes precedence.
    if search_clicked and city_input.strip():
        location_name = city_input.strip()
        with st.spinner("Fetching weather data…"):
            data, error = get_weather_data(location_name, API_KEY)
            if error:
                st.error(error)
                return
            forecast_data, forecast_error = get_forecast_data(location_name, API_KEY)
            if forecast_error:
                st.warning(forecast_error)

    elif use_location:
        with st.spinner("Finding your approximate location…"):
            location, location_error = get_ip_location()
        if location_error:
            st.error(location_error)
            return
        lat, lon = location["latitude"], location["longitude"]
        location_name = location.get("city") or "Your location"
        with st.spinner("Fetching weather for your location…"):
            data, error = get_weather_by_coords(lat, lon, API_KEY)
            forecast_data, forecast_error = get_forecast_by_coords(lat, lon, API_KEY)
        if error:
            st.error(error)
            return
        if forecast_error:
            st.warning(forecast_error)

    if data:
        timezone_offset = data.get("timezone", 0)
        render_current_weather(data)

        # Sunrise / sunset visualization
        render_sun_card(data)

        # AQI
        aqi_data, aqi_error = get_aqi_data(data["coord"]["lat"], data["coord"]["lon"], API_KEY)
        if aqi_data:
            render_aqi(aqi_data)
        elif aqi_error:
            st.warning(aqi_error)

        if forecast_data:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            render_temperature_chart(forecast_data, timezone_offset)
            render_24_hour(forecast_data, timezone_offset)
            st.markdown('</div>', unsafe_allow_html=True)

            render_5_day(forecast_data, timezone_offset)

    # Footer
    st.markdown("---")
    st.caption("💡 The best journeys start with a quick weather check — go explore!")
    st.caption("Made with ❤️ using Streamlit by AP Bhattacharya & Jagriti")


if __name__ == "__main__":
    app()
