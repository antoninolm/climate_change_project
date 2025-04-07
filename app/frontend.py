"""
Frontend logic
"""
import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
import seaborn as sns  # Needed for color palettes

load_dotenv()

# FastAPI Endpoint URL (Replace with actual API URL)
# if local dev -> 0.0.0.0:8000
endpoint = os.getenv("GCLOUD_RUN_URL") or "http://0.0.0.0:8000"
print(f"Using endpoint: {endpoint}")
URL = f"{endpoint}/predict"

# Streamlit App Title
st.title("🌡 Temperature Prediction")

# Sidebar controls for user input
st.sidebar.header("🦶 Select Step")

# Define the known last date of data (31/12/2023)
last_date = datetime(2023, 12, 31)

# Define the earliest valid date (1st January 2024)
earliest_valid_date = datetime(2024, 1, 1)

# Define the latest valid date (7th January 2024)
latest_valid_date = datetime(2024, 1, 7)

# Date selection (limit between 1st Jan 2024 and 7th Jan 2024)
selected_date = st.sidebar.date_input(
    "Select a date",
    min_value=earliest_valid_date.date(),  # Limit to Jan 1, 2024
    max_value=latest_valid_date.date(),    # Limit to Jan 7, 2024
    value=earliest_valid_date.date()       # Default to the first date
)

# Calculate the difference in days between the selected date and the last known date (31/12/2023)
days_difference = (selected_date - last_date.date()).days

# Display the selected date and the difference
st.sidebar.write(f"Selected date: {selected_date}")
st.sidebar.write(f"Days from 31/12/2023: {days_difference} days")

# Load station metadata from CSV
@st.cache_data
def load_station_data():
    df = pd.read_csv("app/stations_with_regions.csv")
    return df.dropna(subset=["LAT", "LON", "REGION", "DEP"])

df_top = load_station_data()
station_names = df_top["NOM_USUEL"].sort_values().unique()

# Dropdown to select one of the available stations
selected_station = st.sidebar.selectbox("📍 Select Station", station_names)

# Format parameters to match dataset
# Keep this commented out for now
# params = {"date": selected_date.strftime("%Y%m%d")}  # Convert date to YYYYMMDD format

# Prepare parameters for the API request
params = {
    "steps": days_difference,
    "station": selected_station
}

# Create a placeholder for the prediction result using st.session_state
# This ensures the prediction stays visible even after Streamlit rerenders the page
if "prediction_msg" not in st.session_state:
    st.session_state.prediction_msg = ""

# Add the temperature image (daily temperature graph)
st.subheader("📈 Daily Temperature Chart")
image_path = os.path.join(os.path.dirname(__file__), 'images', 'image-Tem-Paris-20250403-min.png')
st.image(image_path, caption="Daily Temperature in Aix-en-Provence")
# The image is for Paris, just for presentation purpose we show "Aix-en-Provence" in the caption

# Button to trigger prediction
if st.sidebar.button("🔍 Predict Temperature"):
    with st.spinner("Fetching temperature prediction..."):
        try:
            response = requests.get(URL, params=params, timeout=3000)
            response.raise_for_status()  # Ensures an exception is raised for HTTP errors (4xx, 5xx)
            response_json = response.json()
            print(response_json)
            predicted_temp = response_json.get("prediction", "N/A")

            # When the prediction is fetched, we update the session_state with the result.
            # This ensures the result stays visible even when other components (like the map) rerender.
            st.session_state.prediction_msg = (
                f"🌡 **Predicted Temperature for {selected_station} on {selected_date}: {round(predicted_temp, 2)}°C**"
            )

        except requests.exceptions.RequestException as e:
            st.session_state.prediction_msg = f"❌ Failed to fetch prediction. Error: {e}"

# Display the prediction result
if st.session_state.prediction_msg:
    if "❌" in st.session_state.prediction_msg:
        st.error(st.session_state.prediction_msg)
    else:
        st.success(st.session_state.prediction_msg)

# -------------------------------
# All Stations Map Section
# -------------------------------

st.subheader("📍 All Weather Stations Map")

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

# Display the interactive map
st_folium(station_map, width=800, height=600)

###
# Pushing Frontend Files to GitHub
# 1. Navigate to the project folder:
#    cd package_folder
#
# 2. Initialize a Git repository:
#    git init
#
# 3. Create a new GitHub repository (follow instructions from the GitHub CLI or web interface).
#
# 4. Add and commit your files:
#    git add .
#    git commit -m "Initial commit"
#
# 5. Add the remote repository:
#    git remote add origin <SSH_URL>
#    # Replace <SSH_URL> with your actual GitHub SSH URL.
#
# 6. Verify the remote URL:
#    git remote -v
#
# 7. Push your code to GitHub:
#    git push -u origin main
###
