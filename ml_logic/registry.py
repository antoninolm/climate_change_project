"""
All the loading / saving model
"""
import pickle

def save_model(model,file_name):
    """
    Saves a model to a pickle
    """
    with open(f"models/{file_name}.pkl", "wb") as f:
        pickle.dump(model, f)

def load_model(file_name: str):
    """
    Loads the model from the exported pickle
    """
    with open(f'models/{file_name}.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

        return model
