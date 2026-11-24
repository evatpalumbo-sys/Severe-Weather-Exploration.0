# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)

import requests
import streamlit as st
import pandas as pd

st.title("Weather Forecast Exploration")

st.write("Explore upcoming weather forecasts for several cities.")

# User Input #1
cities = {
    "Atlanta": (33.7490, -84.3880),
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Miami": (25.7617, -80.1918)
}

city = st.selectbox("Select a city", list(cities.keys()))

# User Input #2
days = st.slider(
    "Number of forecast days",
    min_value=1,
    max_value=7,
    value=5
)

latitude, longitude = cities[city]

url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}"
    f"&longitude={longitude}"
    f"&daily=temperature_2m_max,precipitation_sum"
    f"&forecast_days={days}"
    f"&timezone=auto"
)

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    df = pd.DataFrame({
        "Date": data["daily"]["time"],
        "Max Temperature": data["daily"]["temperature_2m_max"],
        "Precipitation": data["daily"]["precipitation_sum"]
    })

    st.subheader(f"Forecast for {city}")

    st.dataframe(df)

    # Dynamic Visual #1
    st.subheader("Maximum Temperature Forecast")

    st.line_chart(
        df.set_index("Date")["Max Temperature"]
    )

    # Dynamic Visual #2
    st.subheader("Daily Precipitation Forecast")

    st.bar_chart(
        df.set_index("Date")["Precipitation"]
    )

else:
    st.error("Unable to retrieve weather data.")