"""
All the loading / saving model
"""
import pickle
import pandas as pd
import os

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

def save_train_and_df(train: pd.DataFrame, df: pd.DataFrame):
    os.makedirs("data/sarima", exist_ok=True)
    """
    Temporary function, to remove after we stop using SARIMAX
    """
    with open("data/sarima/train.pkl", "wb") as f:
        pickle.dump(train, f)

    with open("data/sarima/df.pkl", "wb") as f:
        pickle.dump(df, f)

def load_train_and_df():
    """
    Temporary function, to remove after we stop using SARIMAX
    """
    with open("data/sarima/train.pkl", 'rb') as train_file:
        train = pickle.load(train_file)  # Load the SARIMA model
    with open("data/sarima/df.pkl", 'rb') as df_file:
            df = pickle.load(df_file)  # Load the SARIMA model
     # ✅ Ensure datetime index
    for frame in [train, df]:
        if not isinstance(frame.index, pd.DatetimeIndex):
            frame.index = pd.to_datetime(frame.index)

    return (train, df)
