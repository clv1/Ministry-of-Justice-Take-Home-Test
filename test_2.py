# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type (provided in miles)

import csv
import json
import pandas as pd
import requests

ENDPOINT_URL = 'https://www.find-court-tribunal.service.gov.uk/search/results.json'


class NetworkError(Exception):
    "Class for network-related errors"


def load_people_data(csv_data: csv) -> list[dict]:
    """Loads the csv data and returns it as a list of dictionaries."""
    with open(csv_data, 'r', encoding='utf-8') as file:
        people_df = pd.read_csv(file)
    return people_df.to_dict(orient='records')


def filter_courts_by_type(court_data: list[dict], desired_court_type: str) -> dict:
    """
    Takes in a list of courts, already ordered by distance.
    Returns the first court of the desired type.
    """
    for court in court_data:
        court_type = court.get('types')
        if desired_court_type in court_type:
            return court
    return {'error': 'no court of desired type available.'}


def retrieve_nearest_court_of_type(postcode: str, desired_court_type: str) -> dict:
    """Uses the API to retrieve the nearest court from a person's postcode."""
    postcode_query = f"?postcode={postcode}"

    response = requests.get(ENDPOINT_URL+postcode_query, timeout=10)
    court_data = response.json()

    if response.status_code >= 500:
        raise NetworkError("Server error.")
    if response.status_code >= 400:
        raise NetworkError(
            "Court data not found.")

    nearest_court_of_type = filter_courts_by_type(
        court_data, desired_court_type)
    return nearest_court_of_type


def match_person_to_court(person: dict) -> dict:
    """Returns a dict containing the details of each person and their nearest court."""
    matched_details = {}

    # person details
    matched_details['name'] = person.get('person_name')
    matched_details['desired_court_type'] = person.get(
        'looking_for_court_type')
    matched_details['home_postcode'] = person.get('home_postcode')

    # court details
    matched_court = retrieve_nearest_court_of_type(
        person.get('home_postcode'),  person.get('looking_for_court_type'))
    matched_details['nearest_court_of_type'] = matched_court
    matched_details['court_dx_number'] = matched_court.get('dx_number')
    matched_details['distance_to_court'] = f"{matched_court.get('distance')} miles"

    return matched_details


def match_people_to_courts(people_data: list[list]) -> list[dict]:
    """
    Matches a list of people to courts.
    Returns the details of matches as a JSON array.
    """
    return [match_person_to_court(
        person) for person in people_data]


def generate_json_output(matches_list: list[dict]) -> json:
    """Writes details of matches to file as a json object."""
    with open('test_2_matched_output.json', 'w', encoding='utf-8') as file:
        json.dump(matches_list, file, indent=4)


if __name__ == "__main__":
    people = load_people_data('people.csv')
    matches = match_people_to_courts(people)
    generate_json_output(matches)
