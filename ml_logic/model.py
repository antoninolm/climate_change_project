"""
All the modeling logic/code
"""
import pandas as pd
from prophet import Prophet

def create_model(df: pd.DataFrame):
    """
    Instantiate the model, trains it and returns it
    """
    monthly_avg = df.groupby(['year', 'month']).agg({
        'avg_temperature': 'mean',
        'co2': 'mean',
        'ch4': 'mean',
        'amount_precipitation': 'mean'
    }).reset_index()

    # Prepare Prophet dataframe
    monthly_avg['ds'] = pd.to_datetime(monthly_avg['year'].astype(str) + '-' + monthly_avg['month'].astype(str) + '-01')
    monthly_avg['y'] = monthly_avg['avg_temperature']
    prophet_df = monthly_avg[['ds', 'y', 'co2', 'ch4', 'amount_precipitation']]

    # Train Prophet
    model = Prophet(
        yearly_seasonality=True,
        daily_seasonality=False,
        weekly_seasonality=False,
        seasonality_mode='multiplicative',
    )
    model.add_regressor('co2', prior_scale=2.0)
    model.add_regressor('ch4', prior_scale=1.0)
    model.add_regressor('amount_precipitation', prior_scale=1.0)

    model.fit(prophet_df)
    
    return model
