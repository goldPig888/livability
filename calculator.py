import pandas as pd
import math

# Sigmoid function for scaling penalties
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Define ideal values for each metric
ideal_values = {
    "aqi": 0,
    "carbon_intensity": 50,
    "heatindex_f": 62.2,  # Ideal temperature (Fahrenheit)
    "wind_mph": 10,       # Ideal wind speed (mph)
    "Environmental Stance": 1  # Ideal environmental stance (Neutral)
}

# Adjust weights for each metric
weights = {
    "aqi": 0.55,  # Increased importance of AQI
    "carbon_intensity": 0.15,  # Increased importance of carbon intensity
    "heatindex_f": 0.35,  # Increased importance of temperature
    "wind_mph": 0.10,  # Keep lower weight for wind
    "Environmental Stance": 0.05  # Reduce environmental stance impact
}

# Adjust max deviations allowed for each metric
max_deviations = {
    "aqi": 200,  # Reduced deviation range for AQI
    "carbon_intensity": 150,  # Reduced deviation range for carbon intensity
    "heatindex_f": 30,  # Reduced deviation range for temperature
    "wind_mph": 50,  # Keep the wind speed deviation
    "Environmental Stance": 2  # Keep environmental stance as is
}

# Function to calculate the livability score for each city
def calculate_livability(deviations, user_stance):
    normalized_score = len(max_deviations)  # Start with the maximum score
    
    for key in ideal_values:
        if pd.isna(deviations.get(key)):
            continue
        
        # Calculate deviation from ideal value
        deviation = abs(deviations[key] - ideal_values[key])
        normalized_deviation = deviation / max_deviations[key]
        
        # Apply sigmoid with increased multiplier for stronger penalties
        penalty = sigmoid(weights[key] * normalized_deviation * 20) / 6  # Increased multiplier to 20
        normalized_score -= penalty
    
    # Final livability score, scaled between 0 and 100
    return max(0, min(normalized_score * 100 / 6, 100))
