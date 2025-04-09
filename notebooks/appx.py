# ======================
# 1. STREAMLIT APP SETUP
# ======================
import streamlit as st
import pandas as pd
import pickle
import os
import datetime

# ======================
# 2. LOAD ALL CITY MODELS
# ======================

model_folder = 'prophet_models'
city_models = {}

for filename in os.listdir(model_folder):
    if filename.endswith('_prophet.pkl'):
        safe_city_name = filename.replace('_prophet.pkl', '')
        display_name = safe_city_name.replace('_', ' ')  # Nice display
        with open(os.path.join(model_folder, filename), 'rb') as f:
            city_models[display_name] = pickle.load(f)

# ======================
# 3. STREAMLIT USER INTERFACE
# ======================

st.title("🌍 Future Average Temperature Predictor")

# Select a city
chosen_city = st.selectbox("Select a City:", sorted(city_models.keys()))

# Select how many years into the future
years_into_future = st.slider('Years into the future:', 1, 50, 20)

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

# ======================
# 4. PREDICT THE TEMPERATURE
# ======================
# 1. Select model
model = city_models[chosen_city]

# 2. Build future dataframe
future = model.make_future_dataframe(periods=years_into_future*12, freq='MS')
future['year'] = future['ds'].dt.year
future['month'] = future['ds'].dt.month

# 3. Set future constant features
last_co2 = model.history['co2'].iloc[-1]
last_ch4 = model.history['ch4'].iloc[-1]
last_rainfall = model.history['amount_precipitation'].iloc[-1]

future['co2'] = last_co2
future['ch4'] = last_ch4
future['amount_precipitation'] = last_rainfall

# 4. Predict future
forecast = model.predict(future)

# 5. Add year/month columns into forecast (optional, for easier navigation)
forecast['year'] = forecast['ds'].dt.year
forecast['month'] = forecast['ds'].dt.month

# 6. Build target date
now = datetime.datetime.now()
target_year = now.year + years_into_future
target_month = month_number

target_date = datetime.date(target_year, target_month, 1)

# 7. Find closest prediction
forecast['target_distance'] = abs(forecast['ds'].dt.date - target_date)
target_row = forecast.sort_values('target_distance').iloc[0]

# 8. Display prediction
predicted_temp = target_row['yhat']
target_ds = target_row['ds'].date()

st.subheader(f"🌡️ Predicted Avg Temperature for {chosen_city} in {chosen_month} {target_year}:")
st.metric(label="Temperature (°C)", value=f"{predicted_temp:.2f}")
