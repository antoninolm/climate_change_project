from fastapi import FastAPI
import pickle
from ml_logic.registry import load_model, load_train_and_df
from ml_logic.data import get_data

app = FastAPI()

# Check if the server is running
@app.get('/')
def index():
    return {'ok': True}

@app.get('/predict')
def predict():
    # Load the model and get data
    model = load_model('sarima')
    (train, df) = load_train_and_df()

    def make_predictions(model, steps=1):
        forecast_obj = model.get_forecast(steps=steps)
        forecast_values = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int()
        return forecast_values, conf_int

    # Make predictions
    forecast_values, conf_int = make_predictions(model, steps=1)

    return {'prediction': forecast_values.tolist(), 'confidence_interval': conf_int.values.tolist()}
