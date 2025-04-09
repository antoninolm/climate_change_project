"""
All Stations Map Section
"""

import streamlit as st
import seaborn as sns
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(
  page_title="Map",
  page_icon="🌍",
)

def load_station_data():
    """
    load data
    """
    df = pd.read_csv("app/stations_with_regions.csv")
    return df.dropna(subset=["LAT", "LON", "REGION", "DEP"])


df_top = load_station_data()
st.title("📍 All Weather Stations Map")

# Radio to choose color mode
color_mode = st.radio("Choose how to color stations:", ["By Region", "By Department"])

if color_mode == "By Region":
    unique_vals = df_top["REGION"].unique()
    palette = sns.color_palette("hsv", len(unique_vals)).as_hex()
    color_map = dict(zip(unique_vals, palette))
    color_col = "REGION"
    title = "🗺️ Stations Colored by Region"
else:
    unique_vals = df_top["DEP"].unique()
    palette = sns.color_palette("tab20", len(unique_vals)).as_hex()
    color_map = dict(zip(unique_vals, palette))
    color_col = "DEP"
    title = "🗺️ Stations Colored by Department"

st.subheader(title)

# Center map around average coordinates
map_center = [df_top["LAT"].mean(), df_top["LON"].mean()]
station_map = folium.Map(location=map_center, zoom_start=6)

# Add each station as a pin
for _, row in df_top.iterrows():
    key = row[color_col]
    folium.CircleMarker(
        location=[row["LAT"], row["LON"]],
        radius=5,
        color=color_map.get(key, "gray"),
        fill=True,
        fill_opacity=0.9,
        popup=f"{row['NOM_USUEL']} ({color_col}: {key})"
    ).add_to(station_map)

st.markdown('<div id="leafletmap">')


# Display the interactive map
st_folium(station_map, width=800, height=600)
