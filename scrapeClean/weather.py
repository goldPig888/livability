import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

def fetch_weather(city, api_key):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {'key': api_key, 'q': city.strip()}
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            # Log the error and the problematic city
            print(f"API Error for {city}: {response.status_code} {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # Log request errors
        print(f"Request Error for {city}: {e}")
        return None

def process_cities_concurrently(file_path, api_key, output_file):
    cities = pd.read_csv(file_path)
    
    futures = []
    weather_data = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        
        for city in cities['name']:
            futures.append(executor.submit(fetch_weather, city, api_key))
        
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)
                weather_data.append(result)

    with open(output_file, 'w') as f:
        json.dump(weather_data, f, indent=4)

api_key = '0a4cd908ca72401188f195846230203'
csv_file_path = 'data/world-cities.csv'
output_json_file = 'data/weather.json'
process_cities_concurrently(csv_file_path, api_key, output_json_file)
