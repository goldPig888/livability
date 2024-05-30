import json


state_abbreviations = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}


with open('data/usDistricts.json', 'r') as f:
    city_district_data = json.load(f)


with open('data/environmentalStance.json', 'r') as f:
    district_data = json.load(f)

# Initialize the combined data structure
combined_data = {}

# Process each state in the city-district mapping data
for full_state_name, cities in city_district_data.items():
    if full_state_name not in state_abbreviations:
        print(f"State name {full_state_name} not found in the abbreviations list.")
        continue

    state_acronym = state_abbreviations[full_state_name]
    combined_data[state_acronym] = {}
    
    for city_info in cities:
        city_name = city_info['city']
        combined_data[state_acronym][city_name] = {}
        
        for district in city_info['districts']:
            if district in district_data[state_acronym]['districts']:
                combined_data[state_acronym][city_name][district] = district_data[state_acronym]['districts'][district]

with open('data/environmentalStance.json', 'w') as f:
    json.dump(combined_data, f, indent=4)

print("done")
