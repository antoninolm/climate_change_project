"""
Setup project data and model
"""
from ml_logic.data import get_data
from ml_logic.preprocessing import preprocess
from ml_logic.model import create_model
from ml_logic.registry import save_model

def setup_data_and_model():
    """
    Get the data and instantiate the model
    """
    df = get_data()
    df_preprocessed = preprocess(df)

    model = create_model(df_preprocessed)

    # Save modelas a pickle
    save_model(model, 'sarima')

    print('Successfully created model and pickle files!')

setup_data_and_model()
