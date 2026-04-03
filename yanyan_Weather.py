import streamlit as st
import requests
import json
from openai import OpenAI

st.set_page_config(page_title="yanyan_Weather", page_icon="🌤️", layout="centered")

st.title("🌤️ yanyan_Weather")
st.caption("AI-powered weather insights using OpenAI")

# Sidebar for API key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.caption("Your key is never stored.")

if "input_key" not in st.session_state:
    st.session_state["input_key"] = 0

city = st.text_input("Enter a city name", placeholder="e.g. Tokyo, New York, Paris", key=f"city_input_{st.session_state['input_key']}")

def fetch_weather(city: str) -> dict | None:
    """Fetch weather data from wttr.in (no API key required)."""
    try:
        url = f"https://wttr.in/{requests.utils.quote(city)}?format=j1"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Could not fetch weather data: {e}")
        return None

def parse_weather(data: dict) -> dict:
    """Extract relevant fields from wttr.in JSON."""
    current = data["current_condition"][0]
    area = data["nearest_area"][0]
    area_name = area["areaName"][0]["value"]
    country = area["country"][0]["value"]

    return {
        "location": f"{area_name}, {country}",
        "temp_c": current["temp_C"],
        "temp_f": current["temp_F"],
        "feels_like_c": current["FeelsLikeC"],
        "feels_like_f": current["FeelsLikeF"],
        "humidity": current["humidity"],
        "description": current["weatherDesc"][0]["value"],
        "wind_kmph": current["windspeedKmph"],
        "wind_dir": current["winddir16Point"],
        "visibility_km": current["visibility"],
        "uv_index": current["uvIndex"],
        "pressure_mb": current["pressure"],
        "cloud_cover": current["cloudcover"],
    }

def get_ai_summary(weather: dict, client: OpenAI) -> str:
    """Use OpenAI to generate a friendly weather summary."""
    prompt = f"""
You are a friendly weather presenter. Based on the following weather data, write a short,
engaging 2-3 sentence summary suitable for a weather app. Include practical advice
(e.g. bring an umbrella, wear sunscreen, dress warmly). Be warm and conversational.

Weather data:
{json.dumps(weather, indent=2)}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

col_btn1, col_btn2 = st.columns([1, 1], gap="small")

with col_btn1:
    get_weather_clicked = st.button("Get Weather", type="primary", disabled=not city, use_container_width=True)

with col_btn2:
    refresh_clicked = st.button("Refresh", use_container_width=True)

if refresh_clicked:
    st.session_state["input_key"] += 1
    st.rerun()

if get_weather_clicked:
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar.")
    elif not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather data..."):
            raw = fetch_weather(city.strip())

        if raw:
            weather = parse_weather(raw)

            # Weather metrics
            st.subheader(f"📍 {weather['location']}")
            st.markdown(f"**Condition:** {weather['description']}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{weather['temp_c']}°C / {weather['temp_f']}°F",
                        f"Feels like {weather['feels_like_c']}°C")
            col2.metric("Humidity", f"{weather['humidity']}%")
            col3.metric("Wind", f"{weather['wind_kmph']} km/h {weather['wind_dir']}")

            col4, col5, col6 = st.columns(3)
            col4.metric("Visibility", f"{weather['visibility_km']} km")
            col5.metric("UV Index", weather['uv_index'])
            col6.metric("Pressure", f"{weather['pressure_mb']} mb")

            st.divider()

            # AI summary
            with st.spinner("Generating AI weather summary..."):
                try:
                    client = OpenAI(api_key=api_key)
                    summary = get_ai_summary(weather, client)
                    st.subheader("🤖 AI Weather Summary")
                    st.info(summary)
                except Exception as e:
                    st.error(f"OpenAI error: {e}")
