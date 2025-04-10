from gcp_data_loader import load_climate_dataset_from_gcs

df = load_climate_dataset_from_gcs()

print(df.head())
