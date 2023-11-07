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

"""
for line in tube_lines:
    print(line)
    branches_dict = {}

    res = requests.get(f"https://api.tfl.gov.uk/line/{line}/route/sequence/outbound")
    x = res.json()

    code_res = requests.get(f"https://api.tfl.gov.uk/line/{line}/stoppoints")
    y = code_res.json()


    for route in x["orderedLineRoutes"]:
        name = route["name"].replace("&harr;", "↔")
        branches_dict[name] = route["naptanIds"]

    for station in x["stations"]:
        name = station["name"].split(" Underground Station")[0]
        if station["stopType"] == "NaptanMetroStation":
            station_codes[station["stationId"]] = name
        else:
            for i in range(len(y)):
                if y[i]["commonName] == name+ " Underground Station"
                station_codes[y[i]["id"]] = name

    for branch, stations in branches_dict.items():
        for station in stations:
            index = stations.index(station)
            if station in station_codes.keys():
                stations[index] = station_codes[station]

    station_dict[line] = branches_dict

"""
# with open("stations.txt", "w+", encoding="utf-8") as file:
#    file.write(json.dumps(station_dict))


code_res = requests.get(f"https://api.tfl.gov.uk/line/bakerloo/stoppoints")
y = code_res.json()

name = "Baker Street"
for i in range(len(y)):
    print(y[i]["commonName"])
    if y[i]["commonName"] == name + " Underground Station":
        print(i, y[i]["id"])
