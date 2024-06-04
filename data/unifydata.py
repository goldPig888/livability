import json as js
import csv

abrvs = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "American Samoa": "AS",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Federated States of Micronesia": "FM",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Marshall Islands": "MH",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Palau": "PW",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia":"VA",
    "Virgin Islands": "VI",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}
fnames = open('livability/data/usDistricts.json') # Done
names = js.load(fnames) # Done
faq = open('livability/data/airQuality.json') # should be good awaiting testing
aq = js.load(faq) # should be good
fcarbon = open('livability/data/carbonIntensityData.json')
carbons = js.load(fcarbon)
fstance = open('livability/data/environmentalStance.json') # Done
stances = js.load(fstance) # Done
fweather = open('livability/data/weather.json')
weather = js.load(fweather)

def main():
    cities = extractNamesAndStances(names)
    extractAirQuality(cities)
    extractCarbonIntensity(cities)
    extractWeather(cities)
    write(cities)

def extractNamesAndStances(n: dict):
    cities = {}
    for state in n: # access list of cities
        for city in n[state]: # access individual cities
            temp = n[state][n[state].index(city)]
            temp['state'] = state
            stance = 0
            num = 0
            if stances[abrvs[state]].get(temp['city'], None):
                for district in stances[abrvs[state]][temp['city']]:
                    stance += stances[abrvs[state]][temp['city']][district]['pro']
                    num += 1
            stance = stance / num if num > 0 else 0
            temp['Environmental Stance'] = stance
            
            cities[city['city']] = temp
    return cities
    # should return dict w keys of city names of dictionaries with key names: stance, state, districts

# if the name of the location has the name of an existing location in the dict in it, set aqi in the dict
            
def extractAirQuality(cities: dict):
    for code in aq:
        if aq[code].get('status') and aq[code]['status'] != "ok":
            pass
        else:
            if aq[code].get('data'):
                data = aq[code]['data']
                name = data['city']['name']
                if any([key in name for key in cities]) and any([k in name for k in abrvs]):
                    
                    k = [key if key in name else None for key in cities]
                    k = [a for a in k if a]
                    k = k[0]
                    
                    if not cities.get(k):
                        cities[k]['aqi'] = data['aqi']
                        cities[k]['idx'] = data['idx']
                        if data['city'].get('geo'):
                            cities[k]['Latitude'] = data['city']['geo'][0]
                            cities[k]['Longitude'] = data['city']['geo'][1]


def standardizeRisks():
    weights = {
        "Relatively Low": 0.0166666668,
        "Very Low": 0.0027777778,
        "Relatively Moderate": .027777778,
        "Relatively High": .0388888892,
        "Very High": 0.05277782
    }
def extractCarbonIntensity(cities: dict):
    pass

def extractWeather(cities):
    for city in weather:
        if city['location']['country'] == "United States of America" and cities.get(city['location']['name'], None):
            for attr in city['current']:
                if not "_c" in attr and attr not in ["last_updated_epoch", "last_updated", "condition"]:
                    cities[city['location']['name']][attr] = city['current'][attr]
        else:
            weather.remove(city)
            
def write(cities):
    name = "livability/data/unified.csv"
    with open(name, 'w', newline='') as file:
        keys = [] + list(cities['Houston'].keys())
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for key, value in cities.items():
            row = {'city': key}
            row.update(value)
            writer.writerow(row)


if __name__ == "__main__":
    main()