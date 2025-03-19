from fastapi import FastAPI

app = FastAPI()

# This allows us to make sure our server is running
@app.get('/')
def index():
    return { 'ok': True }

# Main route get the prediction for the day after the last one in the dataset
@app.get('/predict')
def predict():
    # Here we need to call the prediction function
    # then return its result
    return { 'prediction': '' }
