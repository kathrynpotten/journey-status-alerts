""" Script to find delay status of given route on the London Underground (tube line and stations on route). 

Status is scraped from TfL website and parsed for ease of understanding. """

import requests
import bs4
import re


def line_service_status(soup, line):
    line_info = soup.select(f".rainbow-list-item.{line}")
    status = []
    for item in line_info:
        status.append(item.text.replace("\n", " "))

    return status[0].split("Replan your journey")[0]


def update_status(status, line, stations, delay):
    if any(station in status for station in stations):
        status = status.split(" GOOD SERVICE")[0]
        status = (
            f"{line.capitalize()} line has {delay.lower()}"
            + status.split(f"{delay}")[-1]
        )
    elif "GOOD SERVICE" in status:
        status = f"{delay} on parts of {line.capitalize()} line. Your route has good service."
    else:
        status = f"{delay} on parts of {line.capitalize()} line. Your route is not mentioned but may be affected."
    return status


def update_status_suspended(status, line, stations, delay):
    status = status.split(f"{line.capitalize()} Line:")[1]
    if any(station in status for station in stations):
        status = re.split(" (MINOR|SEVERE) DELAYS", status)[0]
        status = (
            f"{line.capitalize()} line is part suspended. "
            + status.split(f"{delay}")[-1].strip()
            + f" {delay} on rest of line."
        )
    else:
        status = f"{line.capitalize()} line is part suspended. {delay} on rest of line. Your route is not mentioned but may be affected."
    return status


def update_status_closure(status, line, stations, delay):
    if any(station in status for station in stations):
        status = re.split("No service", status)[1]
        status = (
            f"{line.capitalize()} line is part closed. "
            + status.split("Use")[0].strip()
        )
    else:
        status = f"{line.capitalize()} line is part closed. Your route is not mentioned but may be affected."
    return status


def parse_status(status, line, stations):
    if "Closed" in status:
        parsed_status = f"{line.capitalize()} closed. Please find alternative route."
    elif "Suspended" in status:
        parsed_status = (
            f"{line.capitalize()} suspended. Please find an alternative route."
        )
    elif "Part suspended" in status:
        if "GOOD SERVICE" in status:
            delay = "Good service"
            parsed_status = update_status_suspended(status, line, stations, delay)
        elif "MINOR DELAYS" in status:
            delay = "Minor delays"
            parsed_status = update_status_suspended(status, line, stations, delay)
        elif "SEVERE DELAYS" in status:
            delay = "Severe delays"
            parsed_status = update_status_suspended(status, line, stations, delay)
    elif "Part closure" in status:
        delay = "Part closure"
        parsed_status = update_status_closure(status, line, stations, delay)
    elif "Severe delays" in status:
        delay = "Severe delays"
        parsed_status = update_status(status, line, stations, delay)
    elif "Reduced service" in status:
        delay = "Reduced service"
        parsed_status = update_status(status, line, stations, delay)
    elif "Minor delays" in status:
        delay = "Minor delays"
        parsed_status = update_status(status, line, stations, delay)
    elif "Good service" in status:
        parsed_status = f"Good service on whole {line.capitalize()} line."
    else:
        parsed_status = (
            "Status not recognised. Please visit the TfL website for more information."
        )

    return parsed_status


def get_status(line, stations):
    res = requests.get("https://tfl.gov.uk/tube-dlr-overground/status/")
    soup = bs4.BeautifulSoup(res.text, "lxml")
    status = line_service_status(soup, line)
    parsed_status = parse_status(status, line, stations)
    return parsed_status


def get_status_commute(line, stations, soup):
    status = line_service_status(soup, line)
    parsed_status = parse_status(status, line, stations)
    return parsed_status


def commute(**kwargs):
    res = requests.get("https://tfl.gov.uk/tube-dlr-overground/status/")
    soup = bs4.BeautifulSoup(res.text, "lxml")
    status_list = []
    for stations, line in kwargs.items():
        status_list.append(get_status_commute(line, stations, soup))
    updated_status_list = [
        status for status in status_list if "Good service on whole" not in status
    ]
    if not updated_status_list:
        route_delay_status = "Good service on all lines."
    else:
        route_delay_status = "\n".join(updated_status_list)

        if len(updated_status_list) != len(status_list):
            route_delay_status += "\nGood service on all other lines"
    return route_delay_status
