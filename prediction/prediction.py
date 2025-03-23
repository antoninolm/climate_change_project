import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# 1. Load Data
# Load the dataset, treating the first row as headers
df = pd.read_csv("../raw_data/Q_13_previous-1950-2023_RR-T-Vent.csv.gz", compression="gzip", delimiter=";")

#Data Preprocessing

# Convert AAAAMMJJ to datetime format
df['date'] = pd.to_datetime(df['AAAAMMJJ'].astype(str), format='%Y%m%d')

# Set the datetime column as the index
df = df.set_index('date')

# Filter data for a specific location (change 'Location_A' to your desired location)
selected_location = "AIX-PUYRICARD"  # Change this to your desired location
df = df[df["NOM_USUEL"] == selected_location]

# Drop columns that are completely NaN (entire column is empty)
df = df.dropna(axis=1, how='all')

# Ensure dataset is sorted
df = df.sort_index()

# Ensure the datetime index has a frequency
df = df.asfreq('D')  # 'D' = Daily frequency

# Feature Engineering: Create lag features (previous day's temperature)
for lag in range(1, 8):  # Create 7 lag days
    df[f'temp_lag_{lag}'] = df['TNTXM'].shift(lag)

# Create time-based features
df['dayofyear'] = df.index.dayofyear
df['month'] = df.index.month
df['year'] = df.index.year

# Drop rows with NaN values (due to lagging)
df = df.dropna()

# Drop specified columns
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

# Ensure data is sorted by date
df = df.sort_index()

# Fix: Reindex to ensure continuous dates
df = df.asfreq('D')  # Set to daily frequency
# Convert object columns to their appropriate types
df = df.infer_objects(copy=False)

# Interpolate only numeric columns
df[df.select_dtypes(include=['number']).columns] = df.select_dtypes(include=['number']).interpolate()

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

# Fit SARIMA model with baseline parameters (simple model)
sarima_model = SARIMAX(train[target],
                       order=(2, 1, 2),         # ARIMA component (p, d, q)
                       seasonal_order=(2, 1, 2, 12),  # Seasonal (P, D, Q, S)
                       enforce_stationarity=False,
                       enforce_invertibility=False,
                       simple_differencing=True)  # Faster training

# Train the model
sarima_result = sarima_model.fit(method='powell', maxiter=200, disp=True)

# Make predictions on the test set
predictions = sarima_result.predict(start=len(train), end=len(df)-1, dynamic=False)

print(predictions.iloc[-7])
