import json as js
import csv
from math import radians, sin, cos, sqrt, atan2
import pprint as urcute

# !! TODO: city -> county mapping and deciphering codes in carbon intensity
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
fnames = open('data/usDistricts.json') # Done
names = js.load(fnames) # Done
faq = open('data/airQuality.json') # Done
aq = js.load(faq) # should be good
fcarbon = open('data/carbonIntensityCity.json') # Done
carbons = js.load(fcarbon)
fstance = open('data/environmentalStance.json') # Done
stances = js.load(fstance) # Done
fweather = open('data/weather.json')
weather = js.load(fweather)

fcoords = open('data/cityCoords.json') # coordinates data
coords = js.load(fcoords) # coordinates data


def main():
    cities = extractNamesAndStances(names)
    #print(cities['New York'])
    extractAirQuality(cities)
    extractCarbonIntensity(cities)
    extractWeather(cities)
    write(cities)
    urcute.pprint(cities['Albany'])


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
            
            
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # this is earth radius in km
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def extractAirQuality(cities: dict):
    #count = 0
    #this is coordsmaxxing the missing ones
    for city in cities:
        if 'Latitude' not in cities[city] or 'Longitude' not in cities[city]:
            coord_entry = next((item for item in coords if item['city'] == city), None)
            if coord_entry:
                cities[city]['Latitude'] = coord_entry['latitude']
                cities[city]['Longitude'] = coord_entry['longitude']
            else:
                #print(f"{count} no coords found for city: {city}")
                #count+=1
                continue
            
        city_lat, city_lon = float(cities[city]['Latitude']), float(cities[city]['Longitude'])
        closest_aqi = None
        min_distance = float('inf')
        for code in aq:
            if aq[code].get('status') != "ok":
                continue
            if 'data' in aq[code] and isinstance(aq[code]['data'], dict):
                data = aq[code]['data']
                if 'geo' in data['city'] and isinstance(data['city']['geo'], list):
                    lat, lon = data['city']['geo']
                    distance = haversine(city_lat, city_lon, lat, lon)
                    if distance < min_distance:
                        min_distance = distance
                        closest_aqi = data
        if closest_aqi:
            cities[city]["aqi"] = closest_aqi['aqi']
            cities[city]["idx"] = closest_aqi['idx']
            cities[city]['Latitude'] = closest_aqi['city']['geo'][0]
            cities[city]['Longitude'] = closest_aqi['city']['geo'][1]
            
            
def standardizeRisks():
    weights = {
        "Relatively Low": 0.0166666668,
        "Very Low": 0.0027777778,
        "Relatively Moderate": .027777778,
        "Relatively High": .0388888892,
        "Very High": 0.05277782
    }
    
    
def extractCarbonIntensity(cities: dict):
    for city, intensity in carbons.items():
        if city in cities:
            cities[city]['carbon_intensity'] = intensity


def extractWeather(cities):
    for city in cities:

        for w in weather:
            if w['location']['name'] == cities[city]['city']:
                for attr in w['current']:
                    if not "_c" in attr and attr not in ["last_updated_epoch", "last_updated", "condition", "wind_dir", "pressure_mb", "precip_mm", "vis_km", "gust_kph", "wind_kph"]:
                        cities[w['location']['name']][attr] = w['current'][attr]


def outputModeling(cities, prefs):
    for city in cities:
        for pref in prefs:
            k = 1
            max = 1
            try:
                str = int(cities[city].get(pref))
                max -= k * ((str - int(prefs[pref])) ** 2) / (int(prefs[pref]) * 100)
            except:
                pass
        max *= 100
        print("Livability: ", max)
        cities[city]["Livability"] = max
        
            
        


def write(cities):
    name = "data/unified.csv"
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