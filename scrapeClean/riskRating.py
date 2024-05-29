import csv
import json
import os

# full name mapping cuz nobody is gonna read what horrid prefixes were in that original one
hazard_mapping = {
    "AVLN": "Avalanche",
    "CFLD": "Coastal Flooding",
    "CWAV": "Cold Wave",
    "DRGT": "Drought",
    "ERQK": "Earthquake",
    "HAIL": "Hail",
    "HWAV": "Heat Wave",
    "HRCN": "Hurricane",
    "ISTM": "Ice Storm",
    "LNDS": "Landslide",
    "LTNG": "Lightning",
    "RFLD": "Riverine Flooding",
    "SWND": "Strong Wind",
    "TRND": "Tornado",
    "TSUN": "Tsunami",
    "VLCN": "Volcanic Activity",
    "WFIR": "Wildfire",
    "WNTW": "Winter Weather"
}

csv_file_path = 'data/riskRating.csv'
output_json_path = 'data/riskRating.json'

data_by_state = {}

with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        state = row['STATE']
        county_name = row['COUNTY']
        county_code = row['COUNTYFIPS']
        buildvalue = row['BUILDVALUE']
        agrivalue = row['AGRIVALUE']
        risk_rating = row['RISK_RATNG']

        if state not in data_by_state:
            data_by_state[state] = {}
        
        if county_name not in data_by_state[state]:
            data_by_state[state][county_name] = {
                "county_code": county_code,
                "buildvalue": buildvalue,
                "agrivalue": agrivalue,
                "risk_rating": risk_rating,
                "hazards": {}
            }
        
        for prefix, full_name in hazard_mapping.items():
            hazard_key = f"{prefix}_RISKR"
            if hazard_key in row and row[hazard_key]:
                rating = row[hazard_key]
                if isinstance(rating, str) and any(word in rating.lower() for word in ["low", "moderate", "high", "very"]):
                    data_by_state[state][county_name]["hazards"][full_name] = rating

os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
with open(output_json_path, 'w') as json_file:
    json.dump(data_by_state, json_file, indent=4)

print(f"Processed data has been saved to {output_json_path}")
