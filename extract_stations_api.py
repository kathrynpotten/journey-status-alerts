""" Script to extract stations for each tube line using TfL API"""

import json
import requests


# for line in tube_lines:
#    res = requests.get("https://api.tfl.gov.uk/line/piccadilly/route/sequence/outbound")
#
#    x = res.json()
#
#    for route in x["orderedLineRoutes"]:


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
branhces_dict = {}

"""
for line in tube_lines:

    res = requests.get(f"https://api.tfl.gov.uk/line/{line}/route/sequence/outbound")

    x = res.json()

    for route in x["orderedLineRoutes"]:
        branhces_dict[route["name"]] = route["naptanIds"]
"""

res = requests.get(f"https://api.tfl.gov.uk/line/piccadilly/route/sequence/outbound")

x = res.json()

for route in x["orderedLineRoutes"]:
    name = route["name"].replace("&harr;", "↔")
    branhces_dict[name] = route["naptanIds"]

print(branhces_dict)
