# yanyan_Weather

AI-powered weather app built with Streamlit and OpenAI.

## Features

- Real-time weather data for any city worldwide (via [wttr.in](https://wttr.in))
- AI-generated weather summaries using OpenAI GPT-4o-mini
- Dark/light mode toggle (top-right corner)
- Displays temperature, humidity, wind, UV index, pressure, and visibility

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run yanyan_Weather.py
   ```

3. **Enter your OpenAI API key** in the sidebar (never stored)

## Requirements

- Python 3.10+
- OpenAI API key

## Dependencies

| Package | Version |
|---------|---------|
| streamlit | >=1.32.0 |
| openai | >=1.0.0 |
| requests | >=2.31.0 |
