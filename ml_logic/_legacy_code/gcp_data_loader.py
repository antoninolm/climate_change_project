from google.cloud import storage
import pandas as pd


def load_climate_dataset_from_gcs(
    bucket_name: str = "arima-models-bucket",
    blob_path: str = "data/Q_13_previous-1950-2023_RR-T-Vent.csv.gz",
    local_filename: str = "Q_13_previous-1950-2023_RR-T-Vent.csv.gz"
) -> pd.DataFrame:
    """
    Download the compressed climate dataset from Google Cloud Storage and return it as a pandas DataFrame.

    Args:
        bucket_name (str): Name of the GCS bucket.
        blob_path (str): Path to the blob (file) in the bucket.
        local_filename (str): Local filename to save the downloaded file.

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    print(f"Downloading {blob_path} from bucket {bucket_name}...")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    blob.download_to_filename(local_filename)
    print(f"Downloaded to {local_filename}")

    df = pd.read_csv(local_filename, compression='gzip')
    print(f"Loaded dataset with shape: {df.shape}")

    return df
