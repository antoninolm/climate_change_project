from statsmodels.tsa.statespace.sarimax import SARIMAX

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
