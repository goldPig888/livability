import json
from collections import defaultdict


input_file_path = 'data/disasterDeclarationsSummaries.json'

with open(input_file_path, 'r') as file:
    data = json.load(file)

# I only want the state, placeCode, incidentType, and declarationDate
# and restructure by state then by zipcode
reorganized_data = defaultdict(lambda: defaultdict(list))

for entry in data["DisasterDeclarationsSummaries"]:
    state = entry["state"]
    place_code = entry["placeCode"]
    incident_type = entry["incidentType"]
    declaration_date = entry["declarationDate"]
    
    reorganized_data[state][place_code].append([incident_type, declaration_date])

reorganized_data = {state: dict(place_codes) for state, place_codes in reorganized_data.items()}

with open(input_file_path, 'w') as file:
    json.dump(reorganized_data, file, indent=4)

