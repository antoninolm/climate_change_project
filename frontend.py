import streamlit as st
import requests

# FastAPI Endpoint URL
URL = "http://      /predict"  # Update with actual FastAPI URL

# Sidebar Interaction for Predictions
st.sidebar.header("📅 Customize Prediction")
year_selected = st.sidebar.slider("Select a Year (2025-2050)", 2025, 2050, 2030)

# Call FastAPI to get prediction
params = {"year": year_selected}
response = requests.get(URL, params=params)

# Handle API Response
if response.status_code == 200:
    predicted_temp = response.json()["predicted_temperature"]
    st.sidebar.write(f"🌡 **Predicted Temperature in {year_selected}: {predicted_temp:.2f}°C**")
else:
    st.sidebar.error("❌ Failed to fetch prediction. Check API connection.")


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
