import streamlit as st
import requests
from datetime import date

# FastAPI Endpoint URL (Replace with actual API URL)
URL = "http://.....api-url/predict"

# Streamlit App Title
st.title("🌡 Temperature Prediction")

# Sidebar controls for user input
st.sidebar.header("📍 Enter Location & Date")

# User input for Latitude & Longitude
lat = st.sidebar.number_input("Enter Latitude", min_value=41.0, max_value=51.0, value=48.8566, format="%.6f")
lon = st.sidebar.number_input("Enter Longitude", min_value=-5.0, max_value=10.0, value=2.3522, format="%.6f")

# Date selection (between 1950-2050)
selected_date = st.sidebar.date_input("Select a Date", min_value=date(1950, 1, 1), max_value=date(2050, 12, 31), value=date.today())

# Format parameters to match dataset
params = {
    "AAAAMMJJ": selected_date.strftime("%Y%m%d"),  # Convert date to YYYYMMDD format
    "LAT": lat,
    "LON": lon
}

# Button to trigger prediction
if st.sidebar.button("🔍 Predict Temperature"):
    with st.spinner("Fetching temperature prediction..."):
        response = requests.get(URL, params=params)

    # Handle API response
    if response.status_code == 200:
        predicted_temp = response.json().get("predicted_temperature", "N/A")
        st.success(f"🌡 **Predicted Temperature on {selected_date}: {predicted_temp}°C**")
    else:
        st.error("❌ Failed to fetch prediction. Check API connection.")



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
