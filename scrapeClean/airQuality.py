import requests
import json
import time
import os
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = 'https://api.waqi.info'
endpoint = '/feed/{city}/?token={token}'
api_key = '88770fd5c1d6a5af839b5f03b04bb958489e0344'

# load city data
city_data = []
with open('data/world-cities.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        city_data.append(row)

def get_air_quality(city, api_key):
    url = base_url + endpoint.format(city=city, token=api_key)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return city, response.json()
    except requests.exceptions.RequestException as e:
        return city, {'error': str(e)}

air_quality_data = {}
max_requests = 1000

# Function to process cities in parallel
def process_cities_in_parallel(city_data, api_key, max_requests):
    with ThreadPoolExecutor(max_workers=max_requests) as executor:
        futures = {executor.submit(get_air_quality, city['name'], api_key): city for city in city_data}

        for future in as_completed(futures):
            city = futures[future]
            city_id = city['geonameid']
            try:
                city_name, data = future.result()
                air_quality_data[city_id] = data
                print(f"Processed {city_name} ({city_id})")
            except Exception as e:
                print(f"Error processing {city['name']} ({city_id}): {e}")

# Process cities in batches of max_requests
for i in range(0, len(city_data), max_requests):
    batch = city_data[i:i + max_requests]
    process_cities_in_parallel(batch, api_key, max_requests)
    time.sleep(1)  # To avoid hitting rate limits

# Save air quality data to file
os.makedirs('data', exist_ok=True)
with open('data/airQuality.json', 'w') as f:
    json.dump(air_quality_data, f, indent=4)

print("Air quality data has been saved to data/airQuality.json")
