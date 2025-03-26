"""
API logic
"""
from fastapi import FastAPI
from ml_logic.registry import load_model, load_train_and_df

app = FastAPI()

# This allows us to make sure our server is running
@app.get('/')
def index():
    """
    Healthcheck route
    """
    return { 'ok': True }

# Main route get the prediction for the day after the last one in the dataset
@app.get('/predict')
def predict():
    """
    Loads the model and gets a prediction
    """
    # Load the pre-trained model (assuming it's stored as arima_model.pkl)
    model = load_model('sarima')

    (train, df) = load_train_and_df()

    def make_predictions(model, steps=1):
        """
        Given a trained SARIMA model, this function will forecast the temperature
        for the next `steps` days.
        It returns both the predicted values and the confidence intervals.
        """
        # Get the forecast for the next `steps` days
        forecast_obj = model.get_forecast(steps=1)

        # Extract the predicted values
        forecast_values = forecast_obj.predicted_mean

        # Extract the confidence intervals (optional)
        conf_int = forecast_obj.conf_int()

        # Return both the forecasted values and the confidence intervals
        return forecast_values, conf_int

    # Call the make_predictions function to predict the next day's temperature
    forecast_values, conf_int = make_predictions(model, steps=1)  # Predict for 1 day ahead

    # Return the forecasted values (temperature)
    return { 'prediction': forecast_values.tolist(), 'confidence_interval': conf_int.values.tolist() }
