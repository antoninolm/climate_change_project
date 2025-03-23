from fastapi import FastAPI

app = FastAPI()

# This allows us to make sure our server is running
@app.get('/')
def index():
    return { 'ok': True }

# Main route get the prediction for the day after the last one in the dataset
@app.get('/predict')
def predict():
    # Load the pre-trained model (assuming it's stored as arima_model.pkl)
    with open('arima_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)  # Load the SARIMA model

    # Call the make_predictions function to predict the next day's temperature
    forecast_values, conf_int = make_predictions(model, steps=1)  # Predict for 1 day ahead

    # Return the forecasted values (temperature)
    return { 'prediction': forecast_values.tolist(), 'confidence_interval': conf_int.tolist() }