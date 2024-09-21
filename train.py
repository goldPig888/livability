import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

# Step 1: Load the dataset
df = pd.read_csv('data/unified_with_livability.csv')

# Step 2: Select features and target (livability score)
# Drop non-numerical or irrelevant columns
features = df.drop(columns=['city', 'districts', 'state', 'livability'])
target = df['livability']

# Step 3: Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Step 4: Scale the features (normalization)
scaler_x = MinMaxScaler()
x_train_scaled = scaler_x.fit_transform(x_train)
x_test_scaled = scaler_x.transform(x_test)

# Target normalization (optional: if you want to normalize livability between 0 and 1)
scaler_y = MinMaxScaler(feature_range=(0, 100))
y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()
y_test_scaled = scaler_y.transform(y_test.values.reshape(-1, 1)).flatten()

# Step 5: Build the Neural Network model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(x_train_scaled.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))  # Predicting a continuous value (livability score)

# Step 6: Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mse'])

# Step 7: Train the model
model.fit(x_train_scaled, y_train_scaled, epochs=50, batch_size=32, validation_data=(x_test_scaled, y_test_scaled))

# Step 8: Save the model and the scalers
model.save('models/livability_nn_model.h5')  # Save the trained model
joblib.dump(scaler_x, 'models/scaler_x.pkl')  # Save the feature scaler
joblib.dump(scaler_y, 'models/scaler_y.pkl')  # Save the target scaler

# Step 9: Evaluate the model
loss, mse = model.evaluate(x_test_scaled, y_test_scaled)
print(f"Test Mean Squared Error: {mse}")

# Predictions for test data (optional)
predictions = model.predict(x_test_scaled)
predictions_unscaled = scaler_y.inverse_transform(predictions)
print(f"Sample Predictions (Unscaled): {predictions_unscaled[:5].flatten()}")
