
import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import datetime
from urllib.parse import quote
from streamlit_autorefresh import st_autorefresh

# PAGE SETTINGS
st.set_page_config(
    page_title="Live Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# AUTO REFRESH EVERY 10 MINUTES
st_autorefresh(interval=600000, key="weather_refresh")

# DESIGN
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eaf4ff, #f8fbff);
}
h1 {
    color: #17365D;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0 3px 12px #d5e1ee;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("🌤️ Live Weather & Air Quality")
st.caption("Real-time Weather Dashboard | Powered by Open-Meteo API")

# CITY INPUT
if "city" not in st.session_state:
    st.session_state.city = "Lahore"

with st.form("city_form"):
    city_input = st.text_input(
        "Enter City Name",
        value=st.session_state.city,
        placeholder="Example: Lahore, Karachi, London"
    )
    search = st.form_submit_button("🔍 Get Weather")

if search and city_input.strip():
    st.session_state.city = city_input.strip()

city = st.session_state.city

# GET CITY COORDINATES
try:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=20
    )

    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        st.error("City not found. Please enter another city.")
        st.stop()

    place = geo_data["results"][0]

    latitude = place["latitude"]
    longitude = place["longitude"]
    city_name = place["name"]
    country = place.get("country", "")

    # GET CURRENT WEATHER AND FORECAST
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "is_day",
                "precipitation",
                "weather_code",
                "wind_speed_10m"
            ],
            "hourly": [
                "temperature_2m",
                "precipitation_probability"
            ],
            "forecast_days": 1,
            "timezone": "auto"
        },
        timeout=20
    )

    weather_response.raise_for_status()
    weather_data = weather_response.json()
    current = weather_data["current"]

    # GET AIR QUALITY
    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    air_response = requests.get(
        air_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "pm10",
                "pm2_5",
                "carbon_monoxide",
                "nitrogen_dioxide",
                "sulphur_dioxide",
                "ozone"
            ],
            "timezone": "auto"
        },
        timeout=20
    )

    air_response.raise_for_status()
    air_data = air_response.json()
    air = air_data["current"]

    # WEATHER DESCRIPTION
    weather_codes = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫️",
        48: "Rime Fog 🌫️",
        51: "Light Drizzle 🌦️",
        53: "Drizzle 🌦️",
        55: "Heavy Drizzle 🌧️",
        61: "Light Rain 🌧️",
        63: "Moderate Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Light Snow ❄️",
        73: "Snow ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Showers 🌦️",
        81: "Rain Showers 🌧️",
        82: "Heavy Rain Showers ⛈️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with Hail ⛈️",
        99: "Heavy Thunderstorm ⛈️"
    }

    description = weather_codes.get(
        current["weather_code"],
        "Weather information available"
    )

    # LOCAL DATE AND TIME
    local_time = datetime.fromisoformat(current["time"])

    st.divider()

    st.subheader(f"📍 {city_name}, {country}")
    st.write(
        f"🕒 Local Date & Time: **{local_time.strftime('%d %B %Y | %I:%M %p')}**"
    )
    st.write(f"🌤️ Current Condition: **{description}**")

    # WEATHER METRICS
    st.header("🌡️ Current Weather")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Temperature",
        f"{current['temperature_2m']} °C"
    )

    c2.metric(
        "Feels Like",
        f"{current['apparent_temperature']} °C"
    )

    c3.metric(
        "Humidity",
        f"{current['relative_humidity_2m']} %"
    )

    c4.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']} km/h"
    )

    c5, c6 = st.columns(2)

    c5.metric(
        "Precipitation",
        f"{current['precipitation']} mm"
    )

    c6.metric(
        "PM2.5",
        f"{air.get('pm2_5', 'N/A')} µg/m³"
    )

    # AIR QUALITY
    st.divider()
    st.header("🌫️ Current Air Quality")

    a1, a2, a3 = st.columns(3)

    a1.metric("PM10", f"{air.get('pm10', 'N/A')} µg/m³")
    a2.metric("Carbon Monoxide", f"{air.get('carbon_monoxide', 'N/A')}")
    a3.metric("Nitrogen Dioxide", f"{air.get('nitrogen_dioxide', 'N/A')}")

    a4, a5, a6 = st.columns(3)

    a4.metric("Sulphur Dioxide", f"{air.get('sulphur_dioxide', 'N/A')}")
    a5.metric("Ozone", f"{air.get('ozone', 'N/A')}")
    a6.metric("PM2.5", f"{air.get('pm2_5', 'N/A')} µg/m³")

    # HOURLY FORECAST
    st.divider()
    st.header("📈 Today's Weather Forecast")

    hourly = weather_data["hourly"]

    forecast_df = pd.DataFrame({
        "Time": pd.to_datetime(hourly["time"]),
        "Temperature": hourly["temperature_2m"],
        "Rain Probability": hourly["precipitation_probability"]
    })

    forecast_df = forecast_df[
        forecast_df["Time"] >= local_time
    ].head(24)

    fig = px.line(
        forecast_df,
        x="Time",
        y="Temperature",
        markers=True,
        title="Hourly Temperature Forecast",
        template="plotly_white"
    )

    st.plotly_chart(fig, width="stretch")

    fig2 = px.bar(
        forecast_df,
        x="Time",
        y="Rain Probability",
        title="Hourly Rain Probability (%)",
        template="plotly_white"
    )

    st.plotly_chart(fig2, width="stretch")

    # API SOURCE LINKS
    st.divider()
    st.header("🌐 Data Sources & API Information")

    # WEATHER API LINK
    weather_api_link = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,"
        f"apparent_temperature,wind_speed_10m,precipitation,weather_code"
        f"&timezone=auto"
    )

    # AIR QUALITY API LINK
    air_api_link = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=pm10,pm2_5,carbon_monoxide,"
        f"nitrogen_dioxide,sulphur_dioxide,ozone"
        f"&timezone=auto"
    )

    # GEOCODING API LINK
    geo_api_link = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={quote(city)}&count=1&language=en&format=json"
    )

    st.markdown("### 🌤️ Weather Data")
    st.markdown(
        f"[Open Weather API JSON ↗]({weather_api_link})"
    )

    st.markdown("### 🌫️ Air Quality Data")
    st.markdown(
        f"[Open Air Quality API JSON ↗]({air_api_link})"
    )

    st.markdown("### 📍 City Location Data")
    st.markdown(
        f"[Open Geocoding API JSON ↗]({geo_api_link})"
    )

    st.markdown("### 📚 Official Documentation")

    st.markdown(
        "[Weather API Documentation ↗](https://open-meteo.com/en/docs)"
    )

    st.markdown(
        "[Air Quality API Documentation ↗](https://open-meteo.com/en/docs/air-quality-api)"
    )

    st.markdown(
        "[Geocoding API Documentation ↗](https://open-meteo.com/en/docs/geocoding-api)"
    )

    st.caption(
        "Data Source: Open-Meteo APIs. "
        "Weather and air-quality values are model-based estimates, "
        "not direct physical sensor measurements."
    )

    st.success("Weather data fetched successfully!")

except requests.RequestException as error:
    st.error(f"API connection error: {error}")

except (KeyError, ValueError, TypeError) as error:
    st.error(f"Data processing error: {error}")
