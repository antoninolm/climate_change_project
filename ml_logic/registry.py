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

def load_models():
    """
    Loads the models from the exported pickle
    """
    model_folder = 'models'
    city_models = {}

    for filename in os.listdir(model_folder):
        if filename.endswith('_prophet.pkl'):
            city_name = filename.replace('_prophet.pkl', '')

            display_name = city_name.replace('_', ' ')  # Nice display

            with open(os.path.join(model_folder, filename), 'rb') as f:
                city_models[display_name] = pickle.load(f)

    return city_models
