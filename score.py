import pandas as pd
#import numpy as np
from io import StringIO

csv_data = """
city,Environmental Stance,aqi,temp_f,humidity
New York,100.0,16,75.9,45
Buffalo,97.2,19,66.0,59
"""

df = pd.read_csv(StringIO(csv_data))


# user preferences & weights
user_prefs = {
    'Environmental Stance': (90, 5),
    'aqi': (50, 4),
    'temp_f': (70, 5),
    'humidity': (50, 3)
}


# rng for normalize
ranges = {
    'Environmental Stance': 100, 
    'aqi': 100,                  
    'temp_f': 100,               
    'humidity': 100              
}


# normalize differences
def normalize_difference(user_value, city_value, range_value):
    return abs(city_value - user_value) / range_value


def calculate_livability(df, user_prefs, ranges):
    scores = {}
    for i, r in df.iterrows():
        total_diff = 0
        total_weight = 0
        for factor, (user_value, weight) in user_prefs.items():
            city_value = r[factor]
            range_value = ranges[factor]
            norm_diff = normalize_difference(user_value, city_value, range_value)
            weighted_diff = norm_diff * weight
            total_diff += weighted_diff
            total_weight += weight
        livability_score = (1 - total_diff / total_weight) * 100
        scores[r['city']] = livability_score
    return scores



livability_scores = calculate_livability(df, user_prefs, ranges)
print(livability_scores)