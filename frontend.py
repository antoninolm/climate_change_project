import streamlit as st
import requests
from datetime import date

# API Endpoint
URL = "http://localhost:8000/predict"

st.title("🌡 Temperature Prediction")

# Date selection
selected_date = st.sidebar.date_input("📅 Pick a date", date.today(), date(1950, 1, 1), date(2025, 3, 20))
params = {"date": selected_date.strftime("%Y%m%d")}

# Predict button
if st.sidebar.button("🔍 Predict Temperature"):
    response = requests.get(URL, params=params).json()
    st.success(f"🌡 **Predicted Temperature: {response.get('predicted_temperature', 'N/A')}°C**")




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
