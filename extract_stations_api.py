""" Script to extract stations for each tube line using TfL API"""

import json
import requests


lines = {
    "tube": [
        "bakerloo",
        "district",
        "metropolitan",
        "victoria",
        "central",
        "hammersmith-city",
        "northern",
        "waterloo-city",
        "circle",
        "jubilee",
        "piccadilly",
    ],
    "elizabeth-line": "elizabeth",
    "dlr": "dlr",
    "tram": "tram",
    "overground": "london-overground",
}

tube_lines = [
    "bakerloo",
    "district",
    "metropolitan",
    "victoria",
    "central",
    "hammersmith-city",
    "northern",
    "waterloo-city",
    "circle",
    "jubilee",
    "piccadilly",
]

station_dict = {}
station_codes = {}


for line in tube_lines:
    branches_dict = {}

    res = requests.get(f"https://api.tfl.gov.uk/line/{line}/route/sequence/outbound")

    x = res.json()

    for route in x["orderedLineRoutes"]:
        name = route["name"].replace("&harr;", "↔")
        branches_dict[name] = route["naptanIds"]

    for station in x["stations"]:
        if station["stopType"] == "NaptanMetroStation":
            name = station["name"].split(" Underground Station")[0]
            station_codes[station["stationId"]] = name

    for branch, stations in branches_dict.items():
        for station in stations:
            index = stations.index(station)
            if station in station_codes.keys():
                stations[index] = station_codes[station]

    station_dict[line] = branches_dict


with open("stations.txt", "w+", encoding="utf-8") as file:
    file.write(json.dumps(station_dict))
