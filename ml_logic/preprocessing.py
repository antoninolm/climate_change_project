"""
All the preprocessing logic/code
"""
import pandas as pd

def get_target() -> str:
    """
    Returns a constant
    """
    return 'TNTXM'

def preprocess(df: pd.DataFrame):
    """
    Handles preprocessing the data
    """
    # Rename columns
    df.rename(columns={
        'TX': 'max_temperature',
        'TM': 'avg_temperature',
        'TN': 'min_temperature',
        'NOM_USUEL': 'location',
        'LAT': 'lat',
        'LON': 'lon',
        'DATE': 'DATE',
        'RR': 'amount_precipitation',
        'Co2 Mole fraction (ppm)': 'co2',
        'Methane ppm': 'ch4'
    }, inplace=True)

    # First replace ',' by '.' then convert to float
    df['co2'] = df['co2'].str.replace(',', '.').astype(float)
    df['ch4'] = df['ch4'].str.replace(',', '.').astype(float)

    # Extract year and month
    df['year'] = df['DATE'].dt.year
    df['month'] = df['DATE'].dt.month

    return df
