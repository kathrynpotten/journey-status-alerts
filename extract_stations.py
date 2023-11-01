""" Script to extract stations for each tube line """

import requests
import bs4
import re


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


station_dict = {}
branches_dict = {}
branched = []


def split_text(type):
    if type == "tube":
        return " Underground Station"
    elif type == "tram":
        return " Tram Stop"
    elif type == "dlr":
        return " DLR Station"
    else:
        return " Rail Station"


def extract_stations(type, soup):
    stops = soup.select(".stop-link")
    split = split_text(type)
    return [station.text.replace("\n", "").split(split)[0] for station in stops]


for type, lines in lines.items():
    for line in lines:
        res = requests.get(f"https://tfl.gov.uk/{type}/route/{line}/")
        soup = bs4.BeautifulSoup(res.text, "lxml")
        routes = soup.select(".orderedRoutesDropDown")
        branches = (
            [branch.text for branch in routes][0].replace(" ", "").split("\n")[:-2]
        )
        if len(branches) > 1:
            branched.append(line)
            branches_dict[line] = branches
        station_dict[line] = extract_stations(type, soup)


for line in branched:
    stations = station_dict[line]
    for branch in branches_dict[line]:
        branch_start, branch_end = branch.split("↔")[0], branch.split("↔")[1]
        branch_start, branch_end = re.sub(
            r"(\w)([A-Z])|(\d)", r"\1 \2\3", branch_start
        ), re.sub(r"(\w)([A-Z])|(\d)", r"\1 \2\3", branch_end)
        start_idx, end_idx = stations.index(branch_start), stations.index(branch_end)

        branches_stations = stations[start_idx : end_idx + 1]


# with open("stations.txt", "w+", encoding="utf-8") as file:
#    file.write(json.dumps(station_dict))

# print(station_dict.keys())
