"""
Handles loading the data
"""
import pandas as pd

def get_data() -> pd.DataFrame:
    """
    Creates a DataFrame from our data .csv file
    """
    df = pd.read_csv(
        "raw_data/Q_13_previous-1950-2023_RR-T-Vent.csv.gz",
        compression="gzip",
        delimiter=";"
    )

    return df
