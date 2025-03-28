"""
All the modeling logic/code
"""
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from ml_logic.preprocessing import get_target

def create_model(df: pd.DataFrame):
    """
    Instantiate the model, trains it and returns it
    """
    # Define the train-test split ratio
    train_ratio = 0.8  # 80% training, 20% testing
    train_size = int(len(df) * train_ratio)

    # Ensure datetime index BEFORE splitting
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    # Split dataset into training and testing sets
    df_train = df.iloc[:train_size]  # Training data
    # test = df.iloc[train_size:]   # Testing data

    target = get_target()

    # FINAL CHECK
    assert df_train[target].notna().all(), "Training data contains NaNs in target"

    # Fit SARIMA model with baseline parameters (simple model)
    sarima_model = SARIMAX(df_train[target],
                        order=(2, 1, 2),         # ARIMA component (p, d, q)
                        seasonal_order=(2, 1, 2, 12),  # Seasonal (P, D, Q, S)
                        enforce_stationarity=False,
                        enforce_invertibility=False,
                        simple_differencing=True)  # Faster training
    # Train the model
    sarima_model = sarima_model.fit(method='powell', maxiter=200, disp=True)

    # We should later on only return the model, for SARIMA we need df and df_train
    return sarima_model
