"""
Handles loading the data
"""
import pandas as pd

def get_data() -> pd.DataFrame:
    """
    Creates a DataFrame from our data .csv file
    """
    # Define the absolute path inside the container
    data_path = "raw_data/all_clean_weather_1984_2024_filtered.csv"

    # Load the dataset
    df = pd.read_csv(data_path, parse_dates=['DATE'])

    return df
