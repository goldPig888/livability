from flask import Flask, render_template, request, session, jsonify
import pandas as pd
import pickle

app = Flask(__name__)
app.config["SECRET_KEY"] = "sahus is a pretty princess <3"

# Load the trained AI model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load city data from the CSV and clean city names for consistency
city_data = pd.read_csv('data/unified.csv')
city_data['city_cleaned'] = city_data['city'].str.strip().str.lower()

# Function to encode environmental stance (Pro = 0, Neutral = 1, Anti = 2)
def encode_environmental_stance(stance):
    mapping = {"Pro": 0, "Neutral": 1, "Anti": 2}
    return mapping.get(stance, 1)  # Default to "Neutral" if stance is not recognized

# Fetch data for a specific city
def get_city_data(city_name):
    city_name_cleaned = city_name.strip().lower()
    city_row = city_data[city_data['city_cleaned'] == city_name_cleaned]
    if city_row.empty:
        raise ValueError(f"City '{city_name}' not found in the dataset.")
    return city_row.iloc[0].to_dict()

# Render the homepage
@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')

# Store user preferences in session
@app.route('/preferences', methods=['POST', 'GET'])
def set_preferences():
    if request.method == "POST":
        data = request.get_json()
        session.permanent = True
        session['preferences'] = data
        return jsonify(success=True)
    elif request.method == "GET":
        if 'preferences' in session:
            preferences = session['preferences']
            return jsonify(success=True, preferences=preferences)
        else:
            return jsonify(success=False, message="No preferences found.")

# Calculate and return the livability score based on preferences and city data using the AI model
@app.route('/livability', methods=['GET', 'POST'])
def get_score():
    preferences = session.get('preferences', {})
    if not preferences:
        return jsonify(success=False, message="Preferences not set."), 400

    # Get city name from preferences
    city = preferences.get('city', 'Unknown')
    try:
        city_real_data = get_city_data(city)
    except ValueError as e:
        return jsonify(success=False, message=str(e)), 400

    # Prepare the data for prediction (e.g., AQI, carbon intensity, etc.)
    input_data = [
        city_real_data['aqi'],
        city_real_data['carbon_intensity'],
        city_real_data['heatindex_f'],
        city_real_data['wind_mph']
    ]

    # Predict livability using the AI model
    livability_score = model.predict([input_data])[0]

    # Calculate percentile
    city_data['livability'] = city_data.apply(lambda row: model.predict([[row['aqi'], row['carbon_intensity'], row['heatindex_f'], row['wind_mph']]])[0], axis=1)
    livability_percentile = (city_data['livability'] > livability_score).mean() * 100

    # Return the result
    return jsonify(success=True, score=livability_score, percentile=livability_percentile)

if __name__ == "__main__":
    app.run(debug=True)
