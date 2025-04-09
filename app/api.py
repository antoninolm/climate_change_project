"""
API logic
"""
import datetime
from fastapi import FastAPI
from ml_logic.registry import load_models


app = FastAPI()

city_models = load_models()

# Check if the server is running
@app.get('/')
def index():
    """
    Healthcheck route
    """
    return {'ok': True}

@app.get('/predict')
def predict(city: str, years: int, month: int):
    """
    Loads the model and gets a prediction
    """

    # Get the model
    model = city_models[city]

    # Build future dataframe
    future = model.make_future_dataframe(periods=(years + 1)*12, freq='MS')  # +1 pour s'assurer d'avoir assez de données

    # Set future constant features
    last_co2 = model.history['co2'].iloc[-1]
    last_ch4 = model.history['ch4'].iloc[-1]
    last_rainfall = model.history['amount_precipitation'].iloc[-1]

    future['co2'] = last_co2
    future['ch4'] = last_ch4
    future['amount_precipitation'] = last_rainfall
    future['year'] = future['ds'].dt.year
    future['month'] = future['ds'].dt.month

    # Predict future
    forecast = model.predict(future)

    # Add year/month columns into forecast (optional, for easier navigation)
    forecast['year'] = forecast['ds'].dt.year
    forecast['month'] = forecast['ds'].dt.month

    # Build target date
    now = datetime.datetime.now()
    target_year = now.year + years
    target_month = month

    # Find prediction for the specific month and year
    target_row = forecast[
        (forecast['year'] == target_year) & 
        (forecast['month'] == target_month)
    ].iloc[0]

    # Get prediction
    predicted_temp = target_row['yhat']

    return { predicted_temp, target_year }
