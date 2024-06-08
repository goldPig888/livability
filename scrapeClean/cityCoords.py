import requests
import json

weather_api_key = "e89f7c64ac17d854de5cdc27af1a00b1"
carbon_api_key = "wt5BXxQvcNUSR"
carbon_url_template = "https://api.electricitymap.org/v3/carbon-intensity/history?lat={lat}&lon={lon}&auth-token={api_key}"

def fetch_carbon_intensity(latitude, longitude):
    url = carbon_url_template.format(lat=latitude, lon=longitude, api_key=carbon_api_key)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        if 'history' in results and results['history']:
            return results['history'][-1]['carbonIntensity']
    return None

with open('/Users/mayespinola/Documents/GitHub/livability/data/cityCoords.json', 'r') as f:
    city_coords = json.load(f)

carbon_intensity_data = {}

for city_info in city_coords:
    city = city_info['city']
    latitude = city_info['latitude']
    longitude = city_info['longitude']
    carbon_intensity = fetch_carbon_intensity(latitude, longitude)
    if carbon_intensity is not None:
        carbon_intensity_data[city] = carbon_intensity
        print(f"City: {city}, Carbon Intensity: {carbon_intensity}")

with open('/Users/mayespinola/Documents/GitHub/livability/data/carbonIntensityCity.json', 'w') as f:
    json.dump(carbon_intensity_data, f, indent=4)

print("done")
