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

    cities = df_preprocessed['location'].unique()

    for city in cities:
        city_df = df_preprocessed[df_preprocessed['location'] == city]

        model = create_model(city_df)

        save_model(model, city)


    print('Successfully created model and pickle files!')

setup_data_and_model()
