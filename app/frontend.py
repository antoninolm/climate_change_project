"""
Frontend logic
"""
from datetime import date

import streamlit as st
import requests

# FastAPI Endpoint URL (Replace with actual API URL)
URL = 'http://0.0.0.0:8000/predict' # "https://climatechangeinfrance-877376155256.europe-west1.run.app/predict"

# Streamlit App Title
st.title("🌡 Temperature Prediction")

# Sidebar controls for user input
st.sidebar.header("📅 Select Date")

# Date selection (between 1965-2030)
selected_date = st.sidebar.date_input(
    "Select a Date",
    min_value=date(1965, 1, 1),
    max_value=date(2030, 12, 31),
    value=date.today()
)

# Format parameters to match dataset
params = {"date": selected_date.strftime("%Y%m%d")}  # Convert date to YYYYMMDD format

# Button to trigger prediction
if st.sidebar.button("🔍 Predict Temperature"):
    with st.spinner("Fetching temperature prediction..."):
        try:
            response = requests.get(URL, params=params, timeout=10)
            response.raise_for_status()  # Ensures an exception is raised for HTTP errors (4xx, 5xx)
            predicted_temp = response.json().get("predicted_temperature", "N/A")

            # Display result
            st.success(f"🌡 **Predicted Temperature on {selected_date}: {predicted_temp}°C**")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to fetch prediction. Error: {e}")



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
