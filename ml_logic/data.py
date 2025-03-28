"""
Handles loading the data
"""
import pandas as pd

def get_data() -> pd.DataFrame:
    """
    Creates a DataFrame from our data .csv file
    """
    # Define the absolute path inside the container
    data_path = "raw_data/Q_13_previous-1950-2023_RR-T-Vent.csv.gz"

    # Load the dataset
    df = pd.read_csv(data_path, compression="gzip", delimiter=";")

    return df
