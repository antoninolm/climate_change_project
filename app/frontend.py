"""
Frontend logic
"""
import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import datetime, timedelta

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

# Format parameters to match dataset
# Keep this commented out for now
# params = {"date": selected_date.strftime("%Y%m%d")}  # Convert date to YYYYMMDD format

# Use the calculated days difference as the 'steps' parameter
params = {"steps": days_difference}

# Button to trigger prediction
if st.sidebar.button("🔍 Predict Temperature"):
    with st.spinner("Fetching temperature prediction..."):
        try:
            response = requests.get(URL, params=params, timeout=3000)
            response.raise_for_status()  # Ensures an exception is raised for HTTP errors (4xx, 5xx)
            response_json = response.json()
            print(response_json)
            predicted_temp = response_json.get("prediction", "N/A")

            # Display result
            st.success(f"🌡 **Predicted Temperature the step / day n°{days_difference} after the last day of training data (31/12/2023): {round(predicted_temp, 2)}°C**")
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
