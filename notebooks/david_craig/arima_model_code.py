import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import time

# 1. From Load Data
# Load the dataset, treating the first row as headers
df = pd.read_csv("/Users/davidcraig/code/antoninolm/climate_change_project/climate_change_project/raw_data/Q_13_previous-1950-2023_RR-T-Vent.csv.gz", compression="gzip", delimiter=";")

# 2. From Data Cleaning Section
# Convert AAAAMMJJ to datetime format
df['date'] = pd.to_datetime(df['AAAAMMJJ'].astype(str), format='%Y%m%d', errors='coerce')

# Set the datetime column as the index
df = df.set_index('date')

# Filter data for a specific location (change 'Location_A' to your desired location)
selected_location = "MARSEILLE"  # Change this to your desired location
df = df[df["NOM_USUEL"] == selected_location]

# Drop columns that are completely NaN (entire column is empty)
df = df.dropna(axis=1, how='all')

# Ensure dataset is sorted
df = df.sort_index()

# Ensure the datetime index has a frequency
df = df.asfreq('D')  # 'D' = Daily frequency


# 3. From notebook section on TIME SERIES ANALYSIS
# Feature Engineering: Create lag features (previous day's temperature)
for lag in range(1, 8):  # Create 7 lag days
    df[f'temp_lag_{lag}'] = df['TNTXM'].shift(lag)

# Create time-based features
df['dayofyear'] = df.index.dayofyear
df['month'] = df.index.month
df['year'] = df.index.year

# Drop specified columns- PLACE AND POST NUMBER
df = df.drop(columns=['NUM_POSTE', 'NUM_USUEL'], errors='ignore')

# Reorder columns: Move 'dayofyear', 'month', and 'year' to positions 3, 4, and 5
cols = list(df.columns)
cols.remove('dayofyear')
cols.remove('month')
cols.remove('year')
cols.insert(3, 'dayofyear')
cols.insert(4, 'month')
cols.insert(5, 'year')
df = df[cols]

# Generate full date range based on min and max in your data
full_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

# Find missing dates
missing_dates = full_range.difference(df.index)

#4. INTERPOLATION SECTION
# Ensure data is sorted by date
df = df.sort_index()

# Fix: Reindex to ensure continuous dates
df = df.asfreq('D')  # Set to daily frequency
# Convert object columns to their appropriate types
df = df.infer_objects(copy=False)

# Interpolate only numeric columns
df[df.select_dtypes(include=['number']).columns] = df.select_dtypes(include=['number']).interpolate()


#5. CHECK FOR STATIONARITY-not required for model predict.


# Perform the ADF test on TNTXM (temperature column)
#adf_result = adfuller(df['TNTXM'].dropna())

# Print results
#print(f"ADF Statistic: {adf_result[0]}")
#print(f"P-value: {adf_result[1]}")

# Interpretation
#if adf_result[1] < 0.05:
    #print("The data is stationary (p < 0.05), SARIMA can be used directly.")
#else:
    #print("The data is non-stationary (p >= 0.05), differencing may be needed before using ARIMA.")

#6. TRAIN-TEST SPLIT
# Set target variable
target = 'TNTXM'  # Assign TNTXM as the target

# Columns to keep but NOT use in the model
exclude_columns = ['M_USUEL', 'LAT', 'LON', 'dayofyear', 'month', 'year', 'ALTI', 'AAAAMMJJ']

# Define features (Exclude the target variable and excluded columns)
features = [col for col in df.columns if col not in exclude_columns + [target, 'NOM_USUEL']]

# Define the train-test split ratio
train_ratio = 0.8  # 80% training, 20% testing
train_size = int(len(df) * train_ratio)

# Split dataset into training and testing sets
train = df.iloc[:train_size]  # Training data
test = df.iloc[train_size:]   # Testing data

# 7. ARIMA MODEL FITTING

#Fit ARIMA model
from statsmodels.tsa.arima.model import ARIMA

arima_model = ARIMA(train[target], order=(2, 1, 2))
arima_result = arima_model.fit()

# Predict on the test set
predictions = arima_result.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
