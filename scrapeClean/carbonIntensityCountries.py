import requests
import json
import os
from pprint import pprint

def get_zones():
    response = requests.get('https://api.electricitymap.org/v3/zones')
    response.raise_for_status()
    return response.json()

def get_ci(zone, api_key):
    headers = {'auth-token': api_key}
    params = {'zone': zone}
    response = requests.get('https://api.electricitymap.org/v3/carbon-intensity/latest', headers=headers, params=params)
    response.raise_for_status()  
    return response.json()

def load_country_zones(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

api_key = 'wt5BXxQvcNUSR'

try:
    zones = get_zones()
    ci_results = {}
    for zone in zones.keys():
        try:
            ci_results[zone] = get_ci(zone, api_key)
        except requests.exceptions.RequestException as e:
            ci_results[zone] = {'error': str(e)}
    
    # Load country zones
    country_zones = load_country_zones('/Users/mayespinola/Documents/GitHub/livability/data/countryZones.json')

    combined_results = {}
    for zone, ci_data in ci_results.items():
        country_name = country_zones.get(zone, {}).get('zoneName', 'Unknown')
        if 'error' not in ci_data:
            combined_results[country_name] = ci_data.get('carbonIntensity')
        else:
            combined_results[country_name] = ','

    pprint(combined_results)
    os.makedirs('data', exist_ok=True)
    with open('data/carbonIntensityData.json', 'w') as json_file:
        json.dump(combined_results, json_file, indent=4)

except requests.exceptions.RequestException as e:
    print(f"Failed to process data: {e}")
