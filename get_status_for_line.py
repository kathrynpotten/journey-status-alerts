import get_delay_status
import ast
import sys


# get line and stations for preferred route
line = sys.argv[1]

with open("stations.txt", "r", encoding="utf-8") as file:
    line_stations = ast.literal_eval(file.read())[line]

idx1, idx2 = line_stations.index(sys.argv[2]), line_stations.index(sys.argv[3])
stations = line_stations[min(idx1, idx2) : max(idx1, idx2) + 1]
route_delay_status = f"{get_delay_status.get_status(line, stations)}"

print(route_delay_status)
