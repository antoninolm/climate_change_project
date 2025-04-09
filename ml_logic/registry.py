"""
All the loading / saving model
"""
import os
import pickle

os.makedirs('models', exist_ok=True)

def sanitize(name):
    """
    Ensure name won't break pickle dumping / loading
    """
    return name.replace('/', '_').replace(' ', '_').replace('\\', '_')

def save_model(model, city_name):
    """
    Saves a model to a pickle
    """
    safe_city_name = sanitize(city_name)

    with open(f"models/{safe_city_name}_prophet.pkl", "wb") as f:
        pickle.dump(model, f)

def load_model(city_name: str):
    """
    Loads the model from the exported pickle
    """
    safe_city_name = sanitize(city_name)
    
    with open(f'models/{safe_city_name}_prophet.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

        return model
