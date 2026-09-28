
import os
from datetime import datetime, timezone, timedelta
import requests
import streamlit as st
from dotenv import load_dotenv

# Browser geolocation component.
# This is a small local Streamlit component so the app's own
# "Use my location" button directly calls navigator.geolocation.
import streamlit.components.v1 as components
from pathlib import Path

_LOCATION_COMPONENT = components.declare_component(
    "sky_location",
    path=str(Path(__file__).parent / "sky_location"),
)

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

.search-panel { margin-bottom: 26px; }

/* Streamlit widgets cannot be reliably wrapped by raw markdown HTML.
   Style the real form so no empty wrapper box is rendered. */
[data-testid="stForm"] {
    border: 1px solid var(--sky-border) !important;
    border-radius: 18px !important;
    padding: 14px !important;
    background: rgba(15, 23, 42, .72) !important;
    margin-bottom: 26px !important;
}

.section {
    margin-top: 34px;
    margin-bottom: 14px;
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
    margin: 0 0 14px;
    background: linear-gradient(90deg, rgba(96,165,250,.55), rgba(148,163,184,.14), transparent);
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
    min-height: 190px;
    box-sizing: border-box;
}

.forecast-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    width: 100%;
    margin-top: 2px;
}

.forecast-grid.five-day {
    grid-template-columns: repeat(5, minmax(0, 1fr));
}

.weather-main-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.7fr) minmax(180px, 1fr);
    gap: 28px;
    align-items: center;
}

.weather-info-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 24px;
}

.sun-summary {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 24px;
}

.sun-end {
    text-align: right;
}

.daylight-wrap {
    margin-top: 24px;
}

.aqi-card-grid {
    display: grid;
    grid-template-columns: minmax(170px, 1fr) minmax(0, 2fr);
    gap: 32px;
    align-items: center;
}

.pollutant-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 10px;
    margin-top: 18px;
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
    height: 12px;
    border-radius: 99px;
    background: linear-gradient(90deg,
        #22c55e 0%,
        #4ade80 10%,
        #a3e635 20%,
        #eab308 35%,
        #facc15 42%,
        #f97316 58%,
        #fb7185 68%,
        #ef4444 82%,
        #b91c1c 100%);
    box-shadow: inset 0 0 18px rgba(255,255,255,.08);
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


.aqi-score-panel {
    display: flex;
    align-items: baseline;
    gap: 12px;
}
.aqi-scale {
    color: #64748b;
    font-size: .78rem;
    margin-top: 3px;
}
.aqi-note {
    margin-top: 12px;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(96,165,250,.08);
    color: #93c5fd;
    font-size: .78rem;
    line-height: 1.45;
}
.wind-line {
    color: #93c5fd;
    font-size: .78rem;
    margin-top: 4px;
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
    background: linear-gradient(90deg, #172033 0%, #d59b22 18%, #fbbf24 38%, #f59e0b 62%, #d59b22 82%, #172033 100%);
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

@media (max-width: 1000px) {
    .forecast-grid.five-day {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .weather-info-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .pollutant-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
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
    .weather-card, .aqi-card, .sun-card {
        padding: 16px;
        border-radius: 18px;
    }
    .weather-main-grid { gap: 10px; }
    .weather-info-grid { gap: 8px; margin-top: 16px; }
    .info-card { min-height: 68px; padding: 11px 12px; border-radius: 13px; }
    .info-value { font-size: .98rem; margin-top: 4px; }
    .aqi-card-grid { gap: 18px; }
    .aqi-card { padding: 16px; }
    .pollutant-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 8px;
        margin-top: 14px;
    }
    .pollutant-grid .info-card { min-height: 0; }
    .section {
        margin-top: 25px;
    }
    .forecast-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }
    .forecast-grid.five-day {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .forecast-card {
        padding: 12px;
        min-height: 0;
        height: auto;
    }
    .forecast-time {
        font-size: .68rem;
        line-height: 1.35;
    }
    .forecast-icon {
        font-size: 1.7rem;
        margin: 7px 0 2px;
    }
    .forecast-temp {
        font-size: 1.35rem;
    }
    .forecast-desc {
        min-height: 0;
        font-size: .72rem;
        line-height: 1.3;
    }
    .rain {
        font-size: .68rem;
        margin-top: 5px;
    }
    .weather-main-grid, .aqi-card-grid {
        grid-template-columns: 1fr;
    }
    .weather-icon {
        font-size: 3.3rem;
        text-align: left;
        margin-top: 0;
    }
}

@media (max-width: 520px) {
    .block-container {
        padding-left: .55rem;
        padding-right: .55rem;
    }
    .weather-info-grid, .pollutant-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 7px;
    }
    .info-card { padding: 10px; min-height: 64px; }
    .info-label { font-size: .64rem; }
    .info-value { font-size: .88rem; line-height: 1.25; overflow-wrap: anywhere; }
    .weather-card, .aqi-card, .sun-card { padding: 13px; border-radius: 16px; }
    .current-temp { font-size: 3.5rem; }
    .weather-icon { font-size: 2.8rem; }
    .aqi-number { font-size: 3.25rem; }
    .aqi-score-panel { gap: 8px; flex-wrap: wrap; }
    .forecast-grid, .forecast-grid.five-day {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 7px;
    }
    .forecast-card { min-height: 0; padding: 10px; border-radius: 13px; }
    .sun-summary { align-items: flex-start; gap: 12px; }
    .sun-time { font-size: 1.05rem; }
    .sun-end { text-align: right; }
    .daylight-wrap { margin-top: 18px; }
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


@st.cache_data(ttl=600, show_spinner=False)
def geocode_city(city, api_key):
    """Resolve a city name to OpenWeather's canonical coordinates.

    Search mode deliberately uses the OpenWeather Geocoding API first instead
    of the deprecated weather-by-city-name lookup. This gives current weather,
    forecast and AQI one canonical lat/lon pair for the searched place.
    """
    if not api_key:
        return None, "OPENWEATHER_API_KEY is not configured."

    query = city.strip()
    if not query:
        return None, "Please enter a city name."

    result, error = request_json(
        "https://api.openweathermap.org/geo/1.0/direct",
        {"q": query, "limit": 5, "appid": api_key},
    )
    if error:
        return None, error
    if not result:
        return None, "City not found. Please check the spelling."

    # Prefer an exact city-name match when the API returns several candidates.
    query_name = query.split(",")[0].strip().casefold()
    exact = [
        item for item in result
        if str(item.get("name", "")).strip().casefold() == query_name
    ]
    selected = exact[0] if exact else result[0]

    return selected, None


@st.cache_data(ttl=60, show_spinner=False)
def get_weather_data_by_search(city, api_key):
    """Search a city, then fetch current weather using its resolved coordinates."""
    location, error = geocode_city(city, api_key)
    if error or not location:
        return None, error or "City not found. Please check the spelling."

    lat = float(location["lat"])
    lon = float(location["lon"])
    weather, weather_error = get_weather_by_coords(lat, lon, api_key)
    if weather_error:
        return None, weather_error

    # Keep the canonical geocoded place metadata with the weather response so
    # the UI can show exactly what location was searched/resolved.
    weather["_search_location"] = {
        "name": location.get("name"),
        "state": location.get("state"),
        "country": location.get("country"),
        "lat": lat,
        "lon": lon,
    }
    return weather, None


@st.cache_data(ttl=180, show_spinner=False)
def get_forecast_data(lat, lon, api_key):
    if not api_key:
        return None, "OPENWEATHER_API_KEY is not configured."
    return request_json(
        "https://api.openweathermap.org/data/2.5/forecast",
        {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
    )


@st.cache_data(ttl=60, show_spinner=False)
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



def wind_direction(degrees):
    """Convert meteorological wind degrees to a 16-point compass direction."""
    if degrees is None:
        return "—"
    try:
        deg = float(degrees) % 360
    except (TypeError, ValueError):
        return "—"
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
    ]
    return directions[int((deg + 11.25) / 22.5) % 16]


# CPCB-style breakpoints for a user-facing estimate.
# IMPORTANT: OpenWeather's current pollution values are point-in-time
# concentrations, while India's official AQI is based on specified
# averaging periods. Therefore this is explicitly an estimate, not an
# official CPCB daily AQI.
CPCB_BREAKPOINTS = {
    "pm25": [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200),
             (91, 120, 201, 300), (121, 250, 301, 400), (251, 500, 401, 500)],
    "pm10": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200),
             (251, 350, 201, 300), (351, 430, 301, 400), (431, 1000, 401, 500)],
    "no2": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200),
            (181, 280, 201, 300), (281, 400, 301, 400), (401, 800, 401, 500)],
    "o3": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200),
           (169, 208, 201, 300), (209, 748, 301, 400), (749, 1000, 401, 500)],
    "co": [(0, 1.0, 0, 50), (1.1, 2.0, 51, 100), (2.1, 10, 101, 200),
           (10.1, 17, 201, 300), (17.1, 34, 301, 400), (34.1, 100, 401, 500)],
    "so2": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200),
            (381, 800, 201, 300), (801, 1600, 301, 400), (1601, 3000, 401, 500)],
    "nh3": [(0, 200, 0, 50), (201, 400, 51, 100), (401, 800, 101, 200),
            (801, 1200, 201, 300), (1201, 1800, 301, 400), (1801, 3000, 401, 500)],
}

def sub_index(value, breakpoints):
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    for clo, chi, ilo, ihi in breakpoints:
        if clo <= value <= chi:
            if chi == clo:
                return float(ihi)
            return ((ihi - ilo) / (chi - clo)) * (value - clo) + ilo
    if value > breakpoints[-1][1]:
        return 500.0
    return 0.0

def estimated_india_aqi(components):
    values = {
        "pm25": components.get("pm2_5"),
        "pm10": components.get("pm10"),
        "no2": components.get("no2"),
        "o3": components.get("o3"),
        # OpenWeather CO is µg/m³; CPCB breakpoint is mg/m³.
        "co": (components.get("co") / 1000) if components.get("co") is not None else None,
        "so2": components.get("so2"),
        "nh3": components.get("nh3"),
    }
    subindices = {
        key: sub_index(value, CPCB_BREAKPOINTS[key])
        for key, value in values.items()
    }
    valid = {k: v for k, v in subindices.items() if v is not None}
    if not valid:
        return None, {}
    return round(max(valid.values())), valid

def india_aqi_category(aqi):
    if aqi is None:
        return "Unavailable"
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Satisfactory"
    if aqi <= 200:
        return "Moderate"
    if aqi <= 300:
        return "Poor"
    if aqi <= 400:
        return "Very Poor"
    return "Severe"

def section_header(kicker, title, subtitle=""):
    st.markdown(
        f"""
        <div class="section">
            <div class="section-rule"></div>
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
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

    wind = data.get("wind", {})
    wind_speed = float(wind.get("speed", 0) or 0)
    wind_deg = wind.get("deg")
    wind_dir = wind_direction(wind_deg)
    wind_display = f'{wind_speed:.1f} m/s'
    if wind_deg is not None:
        wind_display += f' • {wind_dir} ({float(wind_deg):.0f}°)'

    weather_cards = [
        ("Humidity", f'{main["humidity"]}%'),
        ("Wind", wind_display),
        ("Pressure", f'{main["pressure"]} hPa'),
        ("Visibility", f'{data.get("visibility", 0) / 1000:.1f} km'),
    ]
    weather_info_html = "".join(
        f'<div class="info-card"><div class="info-label">{label}</div><div class="info-value">{value}</div></div>'
        for label, value in weather_cards
    )

    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-main-grid">
                <div>
                    <div class="location-line">CURRENT WEATHER • {format_time(data["dt"], offset)}</div>
                    <div class="current-temp">{main["temp"]:.0f}°C</div>
                    <div class="condition">{condition["description"]}</div>
                    <div class="feels">Feels like {main["feels_like"]:.0f}°C</div>
                </div>
                <div class="weather-icon">{icon}</div>
            </div>
            <div class="weather-info-grid">{weather_info_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Weather conditions are fetched from OpenWeather using the same coordinates used for the forecast and AQI.")

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

    st.markdown(
        f"""
        <div class="sun-card">
            <div class="sun-summary">
                <div>
                    <div class="sun-label">🌅 Sunrise</div>
                    <div class="sun-time">{format_time(sunrise, offset)}</div>
                </div>
                <div class="sun-end">
                    <div class="sun-label">🌇 Sunset</div>
                    <div class="sun-time">{format_time(sunset, offset)}</div>
                </div>
            </div>
            <div class="daylight-wrap">
                <div class="daylight-track">
                    <div class="daylight-dot" style="left:{pct}%"></div>
                </div>
                <div class="daylight-caption" style="margin-top:12px">{caption}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # AQI
    section_header(
        "Air quality",
        "Air quality",
        "OpenWeather pollution data with an India-style AQI estimate.",
    )

    if aqi_data and aqi_data.get("list"):
        item = aqi_data["list"][0]
        ow_aqi = int(round(item["main"]["aqi"]))
        ow_label, ow_description, _ = aqi_info(ow_aqi)
        components = item["components"]
        india_aqi, subindices = estimated_india_aqi(components)
        india_label = india_aqi_category(india_aqi)

        if india_aqi is not None:
            score_html = (
                f'<div class="aqi-number">{india_aqi}</div>'
                f'<div class="aqi-label">Estimated India AQI • {india_label}</div>'
                '<div class="aqi-scale">0 Good • 51 Satisfactory • 101 Moderate • '
                '201 Poor • 301 Very Poor • 401 Severe</div>'
            )
            meter = max(0, min(100, india_aqi / 5))
            meter_html = f'<div class="aqi-meter"><div class="aqi-dot" style="left:{meter}%"></div></div>'
        else:
            score_html = (
                '<div class="aqi-number">—</div>'
                '<div class="aqi-label">India AQI unavailable</div>'
            )
            meter_html = ''

        pollutant_values = [
            ("PM2.5", components.get("pm2_5", 0)),
            ("PM10", components.get("pm10", 0)),
            ("O₃", components.get("o3", 0)),
            ("NO₂", components.get("no2", 0)),
            ("SO₂", components.get("so2", 0)),
            ("CO", components.get("co", 0)),
        ]
        pollutant_html = "".join(
            f'<div class="info-card"><div class="info-label">{name}</div><div class="info-value">{value:.1f} µg/m³</div></div>'
            for name, value in pollutant_values
        )

        st.markdown(
            f"""
            <div class="aqi-card">
                <div class="aqi-card-grid">
                    <div>{score_html}</div>
                    <div>
                        <div class="aqi-label">OpenWeather air quality: {ow_label} <span style="color:#64748b">({ow_aqi}/5)</span></div>
                        <div class="aqi-description">{ow_description}</div>
                        {meter_html}
                        <div class="aqi-note">The numeric India AQI shown here is an estimate from the available OpenWeather pollutant concentrations. Official CPCB AQI uses specified averaging periods, so this should not be treated as an official CPCB daily AQI.</div>
                    </div>
                </div>
                <div class="pollutant-grid">{pollutant_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
        forecast_cards = []
        for item in next_24:
            dt = local_dt(item["dt"], offset)
            icon = weather_icon(
                item["weather"][0].get("description", ""),
                item["weather"][0].get("icon", ""),
            )
            rain = item.get("rain", {}).get("3h", 0)
            forecast_cards.append(
                f"""<div class="forecast-card">
                    <div class="forecast-time">{dt.strftime("%a, %d %b")} • {dt.strftime("%I %p").lstrip("0")}</div>
                    <div class="forecast-icon">{icon}</div>
                    <div class="forecast-temp">{item["main"]["temp"]:.0f}°C</div>
                    <div class="forecast-desc">{item["weather"][0]["description"].capitalize()}</div>
                    <div class="rain">💧 {rain:.2f} mm</div>
                </div>"""
            )
        st.markdown(f'<div class="forecast-grid">{"".join(forecast_cards)}</div>', unsafe_allow_html=True)

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
        daily_cards = []
        for day, items in daily:
            high = max(x["main"]["temp_max"] for x in items)
            low = min(x["main"]["temp_min"] for x in items)
            representative = items[len(items) // 2]
            icon = weather_icon(
                representative["weather"][0].get("description", ""),
                representative["weather"][0].get("icon", ""),
            )
            desc = representative["weather"][0]["description"].capitalize()
            daily_cards.append(
                f"""<div class="forecast-card">
                    <div class="forecast-time">{day.strftime("%a • %d %b")}</div>
                    <div class="forecast-icon">{icon}</div>
                    <div class="forecast-temp">{high:.0f}° / {low:.0f}°</div>
                    <div class="forecast-desc">{desc}</div>
                </div>"""
            )
        st.markdown(f'<div class="forecast-grid five-day">{"".join(daily_cards)}</div>', unsafe_allow_html=True)


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

    # Browser GPS lookup. The local component owns the visible button and
    # directly calls navigator.geolocation.getCurrentPosition(). This avoids
    # the extra crosshair button from streamlit-geolocation.
    location = _LOCATION_COMPONENT(
        key="sky_location_button",
        button_label="📍 Use my location",
    )

    if location:
        if location.get("latitude") is not None and location.get("longitude") is not None:
            lat = float(location["latitude"])
            lon = float(location["longitude"])
            location_key = (round(lat, 5), round(lon, 5))

            # Streamlit reruns after the component sends its value. The component
            # may return the same value on that rerun, so only process a new
            # coordinate pair once to avoid an API/rerun loop.
            if location_key != st.session_state.get("last_location_key"):
                st.session_state["last_location_key"] = location_key
                with st.spinner("Finding your location and loading weather..."):
                    data, error = get_weather_by_coords(lat, lon, API_KEY)
                if data:
                    st.session_state["weather_data"] = data
                    st.session_state["selected_city"] = data["name"]
                    st.session_state["location_accuracy"] = location.get("accuracy")
                    st.session_state["location_source"] = "browser"
                    st.rerun()
                elif error:
                    st.error(error)
        elif location.get("error"):
            code = location["error"].get("code")
            message = location["error"].get("message", "Unable to determine your location.")
            if code == 1:
                st.warning("Location permission was denied. Allow location access for this site and try again.")
            elif code == 2:
                st.warning("Your device could not determine the location. Check GPS/location services and try again.")
            elif code == 3:
                st.warning("Location request timed out. Please try again.")
            else:
                st.warning(f"Location unavailable: {message}")

    if submitted and city_input.strip():
        # City searches are resolved through OpenWeather's Geocoding API first.
        # We then request current weather by the returned coordinates so the
        # current conditions, forecast and AQI all use exactly the same point.
        with st.spinner("Resolving city and loading weather..."):
            data, error = get_weather_data_by_search(city_input.strip(), API_KEY)
        if data:
            st.session_state["weather_data"] = data
            st.session_state["selected_city"] = data.get("name", city_input.strip())
            st.session_state["location_accuracy"] = None
            st.session_state["location_source"] = "search"
            st.session_state["last_location_key"] = None
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

        accuracy = st.session_state.get("location_accuracy")
        location_source = st.session_state.get("location_source")
        if location_source == "browser":
            if accuracy:
                accuracy = float(accuracy)
                if accuracy <= 5000:
                    st.caption(f"📍 Location detected from your device • accuracy about {accuracy:.0f} m")
                else:
                    st.caption("📍 Location detected • your browser returned a low-precision location, so weather is based on the nearest resolved coordinates.")
        elif location_source == "search":
            search_location = data.get("_search_location", {})
            search_name = search_location.get("name") or city
            search_state = search_location.get("state")
            search_country = search_location.get("country")
            location_label = ", ".join(
                part for part in [search_name, search_state, search_country] if part
            )
            st.caption(
                f"🔎 City search resolved by OpenWeather Geocoding • {location_label} • "
                f"coordinates {lat:.5f}, {lon:.5f}"
            )

        with st.spinner("Updating forecast and air quality..."):
            forecast_data, forecast_error = get_forecast_data(lat, lon, API_KEY)
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
            Made with ❤️ using Streamlit by AP Bhattacharya
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    if "weather_data" not in st.session_state:
        st.session_state["weather_data"] = None
    if "location_source" not in st.session_state:
        st.session_state["location_source"] = None
    if "location_accuracy" not in st.session_state:
        st.session_state["location_accuracy"] = None
    if "last_location_key" not in st.session_state:
        st.session_state["last_location_key"] = None
    app()
