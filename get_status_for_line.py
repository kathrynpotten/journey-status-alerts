""" Script to find delay status of a route on London Underground, given a tube line, 
departure and destination stations. 

Requires function get_status from get_delay_status module. """

import get_delay_status
import ast
import sys


def get_status_for_line_section(line, departure, destination):
    with open("stations.txt", "r", encoding="utf-8") as file:
        line_stations = ast.literal_eval(file.read().split("\n")[0])[line]

    for branch_stations in line_stations.values():
        try:
            idx1, idx2 = branch_stations.index(departure), branch_stations.index(
                destination
            )
            stations = branch_stations[min(idx1, idx2) : max(idx1, idx2) + 1]

        except ValueError:
            continue

    return f"{get_delay_status.get_status(line, stations)}"


if __name__ == "__main__":
    # get line and stations for preferred route
    line = sys.argv[1]
    departure = sys.argv[2]
    destination = sys.argv[3]

    print(get_status_for_line_section(line, departure, destination))
