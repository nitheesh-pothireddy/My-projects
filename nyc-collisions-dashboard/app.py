"""Streamlit dashboard for analyzing NYC motor vehicle collisions."""

import numpy as np
import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st

DATA_URL = "Motor_Vehicle_Collisions_-_Crashes.csv"
NROWS = 100_000


@st.cache_data(persist=True)
def load_data(nrows: int) -> pd.DataFrame:
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH_DATE", "CRASH_TIME"]])
    data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    data.rename(columns=str.lower, inplace=True)
    data.rename(columns={"crash_date_crash_time": "date/time"}, inplace=True)
    return data


st.title("Motor Vehicle Collisions in New York City")
st.markdown(
    "This application is a Streamlit dashboard that can be used to "
    "analyze motor vehicle collisions in NYC 🗽💥🚗"
)

data = load_data(NROWS)

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(
    data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any")
)

st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at", 0, 23)
hourly = data[data["date/time"].dt.hour == hour]

st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(hourly["latitude"]), np.average(hourly["longitude"]))
st.write(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=hourly[["date/time", "latitude", "longitude"]],
                get_position=["longitude", "latitude"],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            )
        ],
    )
)

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
hist = np.histogram(hourly["date/time"].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})
st.write(px.bar(chart_data, x="minute", y="crashes", hover_data=["minute", "crashes"], height=400))

st.header("Top 5 dangerous streets by affected type")
select = st.selectbox("Affected type of people", ["Pedestrians", "Cyclists", "Motorists"])
injury_col = {
    "Pedestrians": "injured_pedestrians",
    "Cyclists": "injured_cyclists",
    "Motorists": "injured_motorists",
}[select]
st.write(
    data.query(f"{injury_col} >= 1")[["on_street_name", injury_col]]
    .sort_values(by=injury_col, ascending=False)
    .dropna(how="any")[:5]
)

if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)
