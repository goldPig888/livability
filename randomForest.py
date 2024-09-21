import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load your dataset
df = pd.read_csv('data/unified.csv')

# Select features and target
features = df[['aqi', 'carbon_intensity', 'heatindex_f', 'wind_mph']]  # Add more features
target = df['livability']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model (e.g., RandomForest)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the trained model
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
