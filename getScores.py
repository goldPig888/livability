import pandas as pd
from calculator import *

# Load the dataset
df = pd.read_csv('data/unified.csv')

# Ensure required columns are numeric, coercing errors
numeric_columns = ['aqi', 'carbon_intensity', 'heatindex_f', 'wind_mph', 'Environmental Stance', 'livability']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Iterate through each city and calculate the livability score
def process_city(row):
    deviations = {}
    for key in ideal_values:
        deviations[key] = row[key]

    # Set environmental stance
    user_stance = row['Environmental Stance']

    # Calculate and return the livability score
    return calculate_livability(deviations, user_stance)

# Apply the function to each row in the DataFrame to compute livability
df['livability'] = df.apply(process_city, axis=1)

# Calculate percentile rank for livability score
df['livability_percentile'] = df['livability'].rank(pct=True) * 100

# Save the updated DataFrame with livability scores and percentiles
df.to_csv('data/unified.csv', index=False)

print("Livability scores and percentiles calculated and saved to 'data/unified.csv'.")
