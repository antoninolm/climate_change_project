"""
Frontend logic
"""
import os
from dotenv import load_dotenv
import streamlit as st
import requests

st.set_page_config(
  page_title="Demo",
  page_icon="👀",
)

load_dotenv()

endpoint = "http://0.0.0.0:8000" #os.getenv("GCLOUD_RUN_URL") or "http://0.0.0.0:8000"


def load_cities():
    """
    fetch cities
    """
    response = requests.get(f"{endpoint}/cities", timeout=30000)
    response.raise_for_status()  # Ensures an exception is raised for HTTP errors (4xx, 5xx)
    return response.json()['cities']

def get_prediction(params):
    """
    fetch prediction
    """
    response = requests.get(f"{endpoint}/predict", params=params, timeout=3000)
    response.raise_for_status()  # Ensures an exception is raised for HTTP errors (4xx, 5xx)
    response_json = response.json()

    return response_json[0]


# FastAPI Endpoint URL (Replace with actual API URL)
# if local dev -> 0.0.0.0:8000
print(f"Using endpoint: {endpoint}")
URL = f"{endpoint}/predict"

# Get cities list
cities = load_cities()

st.title("🌍 Future Average Temperature Predictor")

# Select a city
chosen_city = st.selectbox("Select a City:", sorted(cities))

# Select how many years into the future
years_into_future = st.slider('Years into the future:', 1, 50, 1)

# Select a month
chosen_month = st.selectbox("Select Month:", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

month_number = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}[chosen_month]


# Prepare parameters for the API request
params = {
  "city": chosen_city,
  "years": years_into_future,
  "month": month_number,
}

prediction = get_prediction(params)


st.success(f"""
              **🌡️ Predicted Avg Temperature (°C) for {chosen_city} in {chosen_month} {2025 + years_into_future}:**
              # **{prediction:.2f}°C**
              """)


# Add the temperature image (daily temperature graph)
st.write("📈 Daily Temperature Chart")
image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'image-Tem-Paris-20250403-min.png')
st.image(image_path, caption="Daily Temperature in Aix-en-Provence")
# The image is for Paris, just for presentation purpose we show "Aix-en-Provence" in the caption
