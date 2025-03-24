"""
Setup project data and model
"""
from ml_logic.data import get_data
from ml_logic.preprocessing import preprocess
from ml_logic.model import create_model
from ml_logic.registry import save_model, save_train_and_df

def setup_data_and_model():
    """
    Get the data and instantiate the model
    """
    df = get_data()
    df_preprocessed = preprocess(df)

    print(len(df_preprocessed))

    (model, df_final, df_train) = create_model(df_preprocessed)

    # Save modelas a pickle
    save_model(model, 'sarima')
    # Save data as a pickle
    # TODO: remove when we change of models from SARIMA to RNN
    save_train_and_df(df_train, df)

    print('Successfully created model and pickle files!')

setup_data_and_model()
