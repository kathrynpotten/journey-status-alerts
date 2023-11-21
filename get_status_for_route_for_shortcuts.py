""" Script to get delay status for a route on the Lonodn Underground given only departure and destination stations.

Uses the TfL API to find suggested route. 

This module is the same as get_status_for_route, but writes to a file for use with Apple Shortcuts. """

import get_status_for_line
import ast
import sys
import requests

f = open("status.txt", "w+")

departure = sys.argv[1]
destination = sys.argv[2]

with open("stations.txt", "r", encoding="utf-8") as file:
    input = file.read().split("\n\n")

ics_codes = ast.literal_eval(input[1])

code_from, code_to = (
    ics_codes[departure],
    ics_codes[destination],
)

res = requests.get(
    f"https://api.tfl.gov.uk/journey/journeyresults/{code_from}/to/{code_to}"
)

x = res.json()

status = ""

for leg in x["journeys"][0]["legs"]:
    leg_line = leg["instruction"]["summary"].split(" line")[0].lower()
    leg_departure = leg["departurePoint"]["commonName"].split(" Underground Station")[0]
    leg_destination = leg["arrivalPoint"]["commonName"].split(" Underground Station")[0]
    f.write(
        f"Take the {leg_line.capitalize()} line from {leg_departure} to {leg_destination}"
    )
    leg_status = get_status_for_line.get_status_for_line_section(
        leg_line, leg_departure, leg_destination
    )
    status += "\n" + leg_status

f.write(status)
f.close()
