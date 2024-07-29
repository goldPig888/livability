from flask import Flask, render_template, request, session, jsonify
import pandas as pd
import numpy as np
import random
import math
import matplotlib
matplotlib.use('Agg')
from model import Model

app = Flask(__name__)
app.config["SECRET_KEY"] = "sahus is a pretty princess <3"

# encode environmental stance
def encode_environmental_stance(stance):
    mapping = {"Pro": 0, "Neutral": 1, "Anti": 2}
    return mapping[stance]

# Mock data generation function with uniform distributions
def generate_mock_data(num_entries):
    
    ranges = {
        "aqi": (0, 500),
        "air_quality": (1, 5),
        "carbon_intensity": (0, 500),
        "environmental_stance": (0, 2),
        "heat_index_temp": (-30, 120),
        "wind_speed_tolerance": (0, 100)
    }
    
    data = []
    for i in range(num_entries):
        entry = {
            "environmental_stance": random.choice([0, 1, 2]),
            "aqi": random.uniform(*ranges["aqi"]),
            "air_quality": random.uniform(*ranges["air_quality"]),
            "carbon_intensity": random.uniform(*ranges["carbon_intensity"]),
            "heat_index_temp": random.uniform(*ranges["heat_index_temp"]),
            "wind_speed_tolerance": random.uniform(*ranges["wind_speed_tolerance"]),
        }
        data.append(entry)
    df = pd.DataFrame(data)
    df['livability'] = calculate_livability(df)
    return df

def calculate_livability(df):
    ideal_values = {
        "aqi": 0,
        "air_quality": 0,
        "carbon_intensity": 50,
        "environmental_stance": 1,
        "heat_index_temp": 62.2,
        "wind_speed_tolerance": 10
    }
    weights = {
        "aqi": 0.35,
        "air_quality": 0.05,
        "carbon_intensity": 0.05,
        "environmental_stance": 0.05,
        "heat_index_temp": 0.3,
        "wind_speed_tolerance": 0.2
    }
    max_deviations = {
        "aqi": 500,  # 500 - 0
        "air_quality": 5,  # 5 - 0
        "carbon_intensity": 450,  # 500 - 50
        "environmental_stance": 1,  # Max deviation (0 to 2)
        "heat_index_temp": 98,  # Max deviation (-30 to 68, 120 - 68)
        "wind_speed_tolerance": 100  # 100 - 0
    }
    
    scores = []
    for _, row in df.iterrows():
        normalized_score = len(max_deviations)
        for key in ideal_values:
            deviation = abs(row[key] - ideal_values[key])
            normalized_deviation = deviation / max_deviations[key]
            print(weights[key] * normalized_deviation * 100)
        
            penalty = sigmoid(weights[key] * normalized_deviation) / 6
            normalized_score -= penalty
        normalized_score = max(0, min(normalized_score * 100 / 6, 100)) 
        scores.append(normalized_score)
    return scores

def sigmoid(x):
    return (1 / 1 + math.exp(-x))


mock_data = generate_mock_data(1000)
features = mock_data.drop(columns=['livability'])
target = mock_data['livability']
model = Model(pd.concat([features, target], axis=1), 'livability')
model.fit()
model.save_model('model.pkl')

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route('/preferences', methods=['POST', 'GET'])
def setPreferences():
    if request.method == "POST":
        data = request.get_json()
        session['preferences'] = data
        return jsonify(success=True)
    
    elif request.method == "GET":
        if 'preferences' in session:
            preferences = session['preferences']
            return jsonify(success=True, preferences=preferences)
        else:
            return jsonify(success=False, message="No preferences found.")

@app.route('/livability', methods=['GET', 'POST'])
def getScore():
    if not session.get('preferences'):
        return "Preferences not set. Please set your preferences first.", 400
    
    preferences = session['preferences']
    preferences_df = pd.DataFrame([preferences])
    
    preferences_df = preferences_df.rename(columns={
        "Environmental Stance": "environmental_stance",
        "AQI": "aqi",
        "Air Quality": "air_quality",
        "Carbon Intensity": "carbon_intensity",
        "Heat Index": "heat_index_temp",
        "Wind Speed Tolerance": "wind_speed_tolerance"
    })
    
    if "environmental_stance" in preferences_df.columns:
        preferences_df["environmental_stance"] = preferences_df["environmental_stance"].apply(encode_environmental_stance)
    
    model = Model(None, 'livability')
    model.load_model('model.pkl')

    for feature in model.feature_names:
        if feature not in preferences_df.columns:
            preferences_df[feature] = 0
            
            
    preferences_df = preferences_df[model.feature_names]
    
    pred_score = model.predict(preferences_df)[0]
    # obtain the conditions of the city, put it in a dataframe, then predict the city OR find what our score for the city was and comp w pred_score
    if request.method == 'POST':
        return jsonify(success=True, score=pred_score)
    else:
        return f"Your livability score is: {pred_score}"

if __name__ == "__main__":
    app.run(debug=True)
