
import os
from datetime import datetime, timezone, timedelta
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Optional browser-geolocation component.
try:
    from streamlit_geolocation import streamlit_geolocation
except ImportError:
    streamlit_geolocation = None

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(
    page_title="Today's Sky",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
<style>
:root {
    --sky-bg: #07101f;
    --sky-surface: #0e1727;
    --sky-surface-2: #121e31;
    --sky-border: rgba(148, 163, 184, 0.16);
    --sky-text: #f8fafc;
    --sky-muted: #94a3b8;
    --sky-blue: #60a5fa;
    --sky-blue-soft: rgba(96, 165, 250, 0.12);
}

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 12% 0%, rgba(59, 130, 246, .10), transparent 28%),
        radial-gradient(circle at 88% 8%, rgba(245, 158, 11, .08), transparent 24%),
        var(--sky-bg);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--sky-border);
    border-radius: 28px;
    padding: 34px 38px;
    margin-bottom: 20px;
    background:
        linear-gradient(135deg, rgba(30, 64, 175, .22), rgba(15, 23, 42, .86) 52%, rgba(120, 53, 15, .14)),
        rgba(15, 23, 42, .78);
    box-shadow: 0 20px 55px rgba(0,0,0,.18);
}

.hero::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -90px;
    top: -100px;
    border-radius: 50%;
    background: rgba(251, 191, 36, .08);
    filter: blur(8px);
}

.eyebrow {
    position: relative;
    z-index: 1;
    color: #93c5fd;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero h1 {
    position: relative;
    z-index: 1;
    margin: 0;
    color: white;
    font-size: clamp(2.1rem, 4vw, 3.4rem);
    line-height: 1.05;
    letter-spacing: -.04em;
}

.hero p {
    position: relative;
    z-index: 1;
    color: #cbd5e1;
    max-width: 720px;
    margin: 14px 0 0;
    line-height: 1.65;
    font-size: 1rem;
}

.search-panel {
    border: 1px solid var(--sky-border);
    border-radius: 18px;
    padding: 14px;
    background: rgba(15, 23, 42, .72);
    margin-bottom: 26px;
}

.section {
    margin-top: 30px;
    margin-bottom: 12px;
}

.section-kicker {
    color: #60a5fa;
    font-size: .70rem;
    font-weight: 800;
    letter-spacing: .16em;
    text-transform: uppercase;
    margin-bottom: 3px;
}

.section-title {
    color: white;
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -.02em;
    margin: 0;
}

.section-subtitle {
    color: #94a3b8;
    font-size: .88rem;
    margin-top: 4px;
}

.section-rule {
    height: 1px;
    margin-top: 14px;
    background: linear-gradient(90deg, rgba(96,165,250,.5), rgba(148,163,184,.12), transparent);
}

.weather-card {
    border: 1px solid var(--sky-border);
    border-radius: 24px;
    padding: 26px;
    background: linear-gradient(145deg, rgba(17, 30, 50, .95), rgba(10, 18, 31, .95));
    box-shadow: 0 18px 45px rgba(0,0,0,.14);
}

.location-line {
    color: #94a3b8;
    font-size: .88rem;
}

.current-temp {
    font-size: clamp(4rem, 8vw, 6.2rem);
    line-height: .95;
    font-weight: 800;
    letter-spacing: -.07em;
    color: white;
    margin: 10px 0 8px;
}

.condition {
    color: #cbd5e1;
    font-size: 1.05rem;
    text-transform: capitalize;
}

.weather-icon {
    font-size: 4.2rem;
    line-height: 1;
    text-align: center;
    margin-top: 10px;
}

.feels {
    color: #94a3b8;
    margin-top: 5px;
}

.info-card {
    border: 1px solid var(--sky-border);
    border-radius: 16px;
    padding: 15px 16px;
    background: rgba(15, 23, 42, .68);
    min-height: 84px;
}

.info-label {
    color: #64748b;
    font-size: .72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
}

.info-value {
    color: #f8fafc;
    font-size: 1.08rem;
    font-weight: 750;
    margin-top: 6px;
}

.forecast-card {
    border: 1px solid var(--sky-border);
    border-radius: 18px;
    padding: 18px;
    background: rgba(15, 23, 42, .78);
    height: 100%;
}

.forecast-time {
    color: #93c5fd;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: .05em;
}

.forecast-icon {
    font-size: 2rem;
    margin: 10px 0 3px;
}

.forecast-temp {
    color: white;
    font-size: 1.65rem;
    font-weight: 800;
}

.forecast-desc {
    color: #94a3b8;
    font-size: .8rem;
    min-height: 34px;
    margin-top: 3px;
}

.rain {
    color: #60a5fa;
    font-size: .76rem;
    margin-top: 8px;
}

.aqi-card {
    border: 1px solid var(--sky-border);
    border-radius: 24px;
    padding: 24px;
    background: linear-gradient(145deg, rgba(17, 30, 50, .96), rgba(10, 18, 31, .96));
}

.aqi-number {
    font-size: 4rem;
    font-weight: 850;
    line-height: .9;
    color: white;
}

.aqi-label {
    color: #cbd5e1;
    font-weight: 750;
    margin-top: 10px;
}

.aqi-description {
    color: #94a3b8;
    line-height: 1.55;
    margin-top: 8px;
}

.aqi-meter {
    margin-top: 22px;
    height: 10px;
    border-radius: 99px;
    background: linear-gradient(90deg, #22c55e 0 20%, #eab308 20% 40%, #f97316 40% 60%, #ef4444 60% 80%, #a855f7 80% 92%, #334155 92% 100%);
    position: relative;
}

.aqi-dot {
    position: absolute;
    top: 50%;
    width: 18px;
    height: 18px;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: white;
    border: 4px solid #0f172a;
    box-shadow: 0 2px 10px rgba(0,0,0,.4);
}

.sun-card {
    border: 1px solid var(--sky-border);
    border-radius: 22px;
    padding: 22px;
    background: rgba(15, 23, 42, .78);
}

.sun-time {
    color: white;
    font-size: 1.25rem;
    font-weight: 800;
    margin-top: 4px;
}

.sun-label {
    color: #64748b;
    font-size: .72rem;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: .1em;
}

.daylight-track {
    position: relative;
    height: 12px;
    margin: 24px 0 9px;
    border-radius: 99px;
    background: linear-gradient(90deg, #1e293b, #fbbf24, #f59e0b, #1e293b);
}

.daylight-dot {
    position: absolute;
    top: 50%;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    background: #fff;
    border: 4px solid #f59e0b;
    box-shadow: 0 0 0 4px rgba(245,158,11,.14), 0 3px 14px rgba(0,0,0,.35);
}

.daylight-caption {
    color: #94a3b8;
    font-size: .82rem;
}

.chart-wrap {
    border: 1px solid var(--sky-border);
    border-radius: 22px;
    padding: 18px 18px 8px;
    background: rgba(15, 23, 42, .72);
}

.empty-state {
    border: 1px dashed rgba(148,163,184,.22);
    border-radius: 20px;
    padding: 40px 24px;
    text-align: center;
    color: #94a3b8;
    background: rgba(15,23,42,.4);
}

.footer {
    border-top: 1px solid var(--sky-border);
    margin-top: 46px;
    padding-top: 22px;
    color: #64748b;
    font-size: .82rem;
    text-align: center;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem .75rem 2.5rem;
    }
    .hero {
        border-radius: 20px;
        padding: 25px 20px;
    }
    .hero h1 {
        font-size: 2.25rem;
    }
    .current-temp {
        font-size: 4.2rem;
    }
    .weather-card, .aqi-card {
        padding: 20px;
        border-radius: 20px;
    }
    .section {
        margin-top: 25px;
    }
    .forecast-card {
        padding: 14px;
    }
    .weather-icon {
        font-size: 3.3rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Helpers
# -----------------------------
def api_error_message(response, default):
    if response.status_code == 401:
        return "OpenWeather API key is invalid or not active."
    if response.status_code == 404:
        return "City not found. Please check the spelling."
    if response.status_code == 429:
        return "OpenWeather rate limit reached. Please wait a moment and try again."
    return f"{default} (HTTP {response.status_code})"


def request_json(url, params=None, timeout=12):
    try:
        response = requests.get(url, params=params, timeout=timeout)
        if response.ok:
            return response.json(), None
        return None, api_error_message(response, "Unable to fetch weather data.")
    except requests.exceptions.Timeout:
        return None, "The weather service took too long to respond."
    except requests.exceptions.RequestException as exc:
        return None, f"Network error: {exc}"


@st.cache_data(ttl=300, show_spinner=False)
def get_weather_data(city, api_key):
    if not api_key:
        return None, "OPENWEATHER_API_KEY is not configured."
    return request_json(
        "https://api.openweathermap.org/data/2.5/weather",
        {"q": city, "appid": api_key, "units": "metric"},
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_forecast_data(city, api_key):
    if not api_key:
        return None, "OPENWEATHER_API_KEY is not configured."
    return request_json(
        "https://api.openweathermap.org/data/2.5/forecast",
        {"q": city, "appid": api_key, "units": "metric"},
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_weather_by_coords(lat, lon, api_key):
    if not api_key:
        return None, "OPENWEATHER_API_KEY is not configured."
    return request_json(
        "https://api.openweathermap.org/data/2.5/weather",
        {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_aqi_data(lat, lon, api_key):
    if not api_key:
        return None, "AQI data is unavailable."
    return request_json(
        "https://api.openweathermap.org/data/2.5/air_pollution",
        {"lat": lat, "lon": lon, "appid": api_key},
    )


def local_dt(timestamp, offset_seconds=0):
    return datetime.fromtimestamp(
        timestamp, tz=timezone.utc
    ) + timedelta(seconds=offset_seconds)


def format_time(timestamp, offset_seconds):
    return local_dt(timestamp, offset_seconds).strftime("%I:%M %p")


def weather_icon(condition, icon_code=""):
    code = icon_code or ""
    if code.startswith("01"):
        return "☀️" if code.endswith("d") else "🌙"
    if code.startswith("02"):
        return "🌤️"
    if code.startswith("03") or code.startswith("04"):
        return "☁️"
    if code.startswith("09"):
        return "🌧️"
    if code.startswith("10"):
        return "🌦️"
    if code.startswith("11"):
        return "⛈️"
    if code.startswith("13"):
        return "❄️"
    if code.startswith("50"):
        return "🌫️"
    return "🌤️"


def section_header(kicker, title, subtitle=""):
    st.markdown(
        f"""
        <div class="section">
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
            <div class="section-rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(label, value):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">{label}</div>
            <div class="info-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def aqi_info(aqi):
    mapping = {
        1: ("Good", "Air quality is good with little or no health concern.", 10),
        2: ("Fair", "Air quality is generally acceptable, though some pollutants may be elevated.", 30),
        3: ("Moderate", "Some people may experience effects from air pollution.", 50),
        4: ("Poor", "Health effects are possible, especially for sensitive groups.", 70),
        5: ("Very poor", "Health alert: stronger effects are possible for the general population.", 90),
    }
    return mapping.get(aqi, ("Unknown", "AQI information is unavailable.", 0))


def daylight_position(current_ts, sunrise_ts, sunset_ts):
    if sunset_ts <= sunrise_ts:
        return 50, "Daylight information unavailable."
    if current_ts < sunrise_ts:
        return 0, "Before sunrise"
    if current_ts > sunset_ts:
        return 100, "After sunset"
    pct = ((current_ts - sunrise_ts) / (sunset_ts - sunrise_ts)) * 100
    return max(0, min(100, pct)), "Daylight right now"


def render_weather(data, forecast_data, aqi_data):
    offset = data.get("timezone", 0)
    main = data["main"]
    condition = data["weather"][0]
    icon = weather_icon(condition.get("description", ""), condition.get("icon", ""))

    section_header(
        "Current conditions",
        f"{data['name']}, {data.get('sys', {}).get('country', '')}",
        "Live weather conditions and atmospheric details.",
    )

    st.markdown('<div class="weather-card">', unsafe_allow_html=True)
    left, right = st.columns([1.7, 1], gap="large")

    with left:
        st.markdown(
            f'<div class="location-line">CURRENT WEATHER • {format_time(data["dt"], offset)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="current-temp">{main["temp"]:.0f}°C</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="condition">{condition["description"]}</div>'
            f'<div class="feels">Feels like {main["feels_like"]:.0f}°C</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(f'<div class="weather-icon">{icon}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cards = [
        ("Humidity", f'{main["humidity"]}%'),
        ("Wind", f'{data["wind"].get("speed", 0):.1f} m/s'),
        ("Pressure", f'{main["pressure"]} hPa'),
        ("Visibility", f'{data.get("visibility", 0) / 1000:.1f} km'),
    ]
    cols = st.columns(4)
    for col, (label, value) in zip(cols, cards):
        with col:
            info_card(label, value)
    st.markdown("</div>", unsafe_allow_html=True)

    # Sunrise / sunset
    section_header(
        "Daylight",
        "Sunrise & sunset",
        "A simple view of today's daylight window.",
    )
    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]
    current = data["dt"]
    pct, caption = daylight_position(current, sunrise, sunset)

    st.markdown('<div class="sun-card">', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('<div class="sun-label">🌅 Sunrise</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sun-time">{format_time(sunrise, offset)}</div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="sun-label">🌇 Sunset</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sun-time">{format_time(sunset, offset)}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="daylight-track">
            <div class="daylight-dot" style="left:{pct}%"></div>
        </div>
        <div class="daylight-caption">{caption}</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # AQI
    section_header(
        "Air quality",
        "Air quality",
        "OpenWeather air pollution index and pollutant concentrations.",
    )

    if aqi_data and aqi_data.get("list"):
        item = aqi_data["list"][0]
        aqi = item["main"]["aqi"]
        label, description, meter = aqi_info(aqi)
        components = item["components"]

        st.markdown('<div class="aqi-card">', unsafe_allow_html=True)
        top_left, top_right = st.columns([.8, 2.2], gap="large")
        with top_left:
            st.markdown(f'<div class="aqi-number">{aqi}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="aqi-label">AQI • {label}</div>', unsafe_allow_html=True)
        with top_right:
            st.markdown(f'<div class="aqi-description">{description}</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="aqi-meter">
                    <div class="aqi-dot" style="left:{meter}%"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        pollutant_values = [
            ("PM2.5", components.get("pm2_5", 0)),
            ("PM10", components.get("pm10", 0)),
            ("O₃", components.get("o3", 0)),
            ("NO₂", components.get("no2", 0)),
            ("SO₂", components.get("so2", 0)),
            ("CO", components.get("co", 0)),
        ]
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(6)
        for col, (name, value) in zip(cols, pollutant_values):
            with col:
                info_card(name, f"{value:.1f} µg/m³")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Air quality data is currently unavailable.")

    # Forecast data
    if forecast_data and forecast_data.get("list"):
        forecast_list = forecast_data["list"]

        # Next 24 hours
        section_header(
            "Short-term forecast",
            "Next 24 hours",
            "Three-hour forecast intervals from OpenWeather.",
        )

        next_24 = forecast_list[:8]
        # chart
        labels = [
            local_dt(item["dt"], offset).strftime("%I %p").lstrip("0")
            for item in next_24
        ]
        temps = [round(item["main"]["temp"], 1) for item in next_24]

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown("**Temperature trend**")
        chart_df = pd.DataFrame({"Time": labels, "Temperature (°C)": temps})
        st.line_chart(
            chart_df,
            x="Time",
            y="Temperature (°C)",
            use_container_width=True,
            height=280,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(4)
        for col, item in zip(cols, next_24[:4]):
            with col:
                dt = local_dt(item["dt"], offset)
                icon = weather_icon(
                    item["weather"][0].get("description", ""),
                    item["weather"][0].get("icon", ""),
                )
                rain = item.get("rain", {}).get("3h", 0)
                st.markdown(
                    f"""
                    <div class="forecast-card">
                        <div class="forecast-time">{dt.strftime("%I %p").lstrip("0")}</div>
                        <div class="forecast-icon">{icon}</div>
                        <div class="forecast-temp">{item["main"]["temp"]:.0f}°C</div>
                        <div class="forecast-desc">{item["weather"][0]["description"].capitalize()}</div>
                        <div class="rain">💧 {rain:.2f} mm</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        cols = st.columns(4)
        for col, item in zip(cols, next_24[4:8]):
            with col:
                dt = local_dt(item["dt"], offset)
                icon = weather_icon(
                    item["weather"][0].get("description", ""),
                    item["weather"][0].get("icon", ""),
                )
                rain = item.get("rain", {}).get("3h", 0)
                st.markdown(
                    f"""
                    <div class="forecast-card">
                        <div class="forecast-time">{dt.strftime("%I %p").lstrip("0")}</div>
                        <div class="forecast-icon">{icon}</div>
                        <div class="forecast-temp">{item["main"]["temp"]:.0f}°C</div>
                        <div class="forecast-desc">{item["weather"][0]["description"].capitalize()}</div>
                        <div class="rain">💧 {rain:.2f} mm</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # 5-day forecast
        section_header(
            "Extended forecast",
            "5-day forecast",
            "Daily high/low ranges derived from the available 3-hour forecast points.",
        )

        grouped = {}
        for item in forecast_list:
            day = local_dt(item["dt"], offset).date()
            grouped.setdefault(day, []).append(item)

        daily = list(grouped.items())[:5]
        cols = st.columns(5)
        for col, (day, items) in zip(cols, daily):
            with col:
                high = max(x["main"]["temp_max"] for x in items)
                low = min(x["main"]["temp_min"] for x in items)
                representative = items[len(items) // 2]
                icon = weather_icon(
                    representative["weather"][0].get("description", ""),
                    representative["weather"][0].get("icon", ""),
                )
                desc = representative["weather"][0]["description"].capitalize()
                st.markdown(
                    f"""
                    <div class="forecast-card">
                        <div class="forecast-time">{day.strftime("%a • %d %b")}</div>
                        <div class="forecast-icon">{icon}</div>
                        <div class="forecast-temp">{high:.0f}° / {low:.0f}°</div>
                        <div class="forecast-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def app():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Weather • Air quality • Forecast</div>
            <h1>Today's Sky ☁️</h1>
            <p>
                Clear, useful weather insights for any city — live conditions,
                air quality, daylight and short-term forecasts in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    with st.form("city_search", clear_on_submit=False):
        c1, c2 = st.columns([5, 1])
        with c1:
            city_input = st.text_input(
                "City",
                placeholder="Enter a city, e.g. Chandigarh",
                label_visibility="collapsed",
            )
        with c2:
            submitted = st.form_submit_button("🔎 Search", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Location lookup: browser GPS if streamlit-geolocation is installed.
    loc_col, note_col = st.columns([1.1, 2.9])
    with loc_col:
        use_location = st.button("📍 Use my location", use_container_width=True)
    with note_col:
        if streamlit_geolocation is None:
            st.caption("For precise browser location, install: pip install streamlit-geolocation")
        else:
            st.caption("Uses your browser's location permission; no IP geolocation service is required.")

    if use_location:
        if streamlit_geolocation is None:
            st.error("Install `streamlit-geolocation` and restart the app to enable browser location.")
        else:
            location = streamlit_geolocation()
            if location and location.get("latitude") is not None and location.get("longitude") is not None:
                with st.spinner("Finding your location..."):
                    data, error = get_weather_by_coords(
                        float(location["latitude"]),
                        float(location["longitude"]),
                        API_KEY,
                    )
                if data:
                    st.session_state["weather_data"] = data
                    st.session_state["selected_city"] = data["name"]
                elif error:
                    st.error(error)
            elif location and location.get("error"):
                st.error(f"Location permission/error: {location['error']}")
            else:
                st.info("Please allow location access in your browser.")

    if submitted and city_input.strip():
        with st.spinner("Loading weather..."):
            data, error = get_weather_data(city_input.strip(), API_KEY)
        if data:
            st.session_state["weather_data"] = data
            st.session_state["selected_city"] = data["name"]
        elif error:
            st.error(error)

    data = st.session_state.get("weather_data")

    if not data:
        st.markdown(
            """
            <div class="empty-state">
                <div style="font-size:2.4rem">🌤️</div>
                <div style="color:#f8fafc;font-size:1.1rem;font-weight:750;margin-top:8px">
                    Search for a city to get started
                </div>
                <div style="margin-top:6px">
                    Current conditions, AQI, daylight and a 5-day forecast will appear here.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        city = data["name"]
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]

        with st.spinner("Updating forecast and air quality..."):
            forecast_data, forecast_error = get_forecast_data(city, API_KEY)
            aqi_data, aqi_error = get_aqi_data(lat, lon, API_KEY)

        render_weather(data, forecast_data, aqi_data)

        if forecast_error:
            st.warning(forecast_error)
        if aqi_error:
            st.warning(aqi_error)

    st.markdown(
        """
        <div class="footer">
            💡 The best journeys start with a quick weather check — go explore!<br><br>
            Made with ❤️ using Streamlit by AP Bhattacharya & Jagriti
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    if "weather_data" not in st.session_state:
        st.session_state["weather_data"] = None
    app()
