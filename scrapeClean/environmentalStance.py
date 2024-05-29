import csv
import json
from collections import defaultdict

input_csv = 'data/environmentalStance.csv'
states_data = defaultdict(lambda: {"districts": defaultdict(dict), "score": {"pro_avg": 0, "anti_avg": 0}})

# processing
with open(input_csv, mode='r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        state = row["District"].split("-")[0]
        district = row["District"]

        pro_votes = sum(1 for v in row.values() if v == '+')
        anti_votes = sum(1 for v in row.values() if v == '-')
        total_votes = sum(1 for v in row.values() if v in ['+', '-', '?', 'n/a'])

        pro_percentage = (pro_votes / total_votes) * 100 if total_votes > 0 else 0
        anti_percentage = (anti_votes / total_votes) * 100 if total_votes > 0 else 0

        states_data[state]["districts"][district] = {
            "pro": pro_percentage,
            "anti": anti_percentage
        }

# state avg
for state, data in states_data.items():
    pro_sum = sum(d["pro"] for d in data["districts"].values())
    anti_sum = sum(d["anti"] for d in data["districts"].values())
    num_districts = len(data["districts"])

    state_pro_avg = pro_sum / num_districts if num_districts > 0 else 0
    state_anti_avg = anti_sum / num_districts if num_districts > 0 else 0

    data["score"]["pro_avg"] = state_pro_avg
    data["score"]["anti_avg"] = state_anti_avg

output_json = 'data/environmentalStance.json'

with open(output_json, mode='w') as file:
    json.dump(states_data, file, indent=4)

print(f"JSON data has been written to {output_json}")
