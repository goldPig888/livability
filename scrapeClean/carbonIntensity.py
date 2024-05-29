import requests
from pprint import pprint
import json
import os

# endpoints
zones_url = 'https://api.electricitymap.org/v3/zones'
ci_url = 'https://api.electricitymap.org/v3/carbon-intensity/latest'

api_key = 'wt5BXxQvcNUSR'

# get all zones
def get_zones():
    response = requests.get(zones_url)
    response.raise_for_status()
    return response.json()

# get carbon intensity for a specific zone
def get_ci(zone):
    headers = {'auth-token': api_key}
    params = {'zone': zone}
    response = requests.get(ci_url, headers=headers, params=params)
    response.raise_for_status()  
    return response.json()

ci_results = {}

try:
    # getting the zones...
    zones = get_zones()
    
    # populating the dict...
    for zone in zones.keys():
        try:
            ci_results[zone] = get_ci(zone)
        except requests.exceptions.RequestException as e:
            ci_results[zone] = {'error': str(e)}
except requests.exceptions.RequestException as e:
    print(f"Failed to get available zones: {e}")

# pretty print 🎀
pprint(ci_results)

os.makedirs('data', exist_ok=True)

# write to file
with open('data/carbonIntensityData.json', 'w') as json_file:
    json.dump(ci_results, json_file, indent=4)

issues_count = len([zone for zone in ci_results if 'error' in ci_results[zone]])
no_issues_count = len(ci_results) - issues_count

print(f"zones with issues: {issues_count}")
print(f"zones without issues: {no_issues_count}")
