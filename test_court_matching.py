import pytest
from unittest.mock import MagicMock, patch
from test_2 import NetworkError, load_people_data, filter_courts_by_type, retrieve_nearest_court_of_type

ENDPOINT_URL = "https://example.com/api"
COURT_DATA_1 = [
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": "null",
        "cci_code": "null",
        "magistrate_code": "null",
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
        "displayed": True,
        "hide_aols": False,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
]

COURT_DATA_2 = [
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": "null",
        "cci_code": "null",
        "magistrate_code": "null",
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
        "displayed": True,
        "hide_aols": False,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    {
        "name": "Random County Court",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": "null",
        "cci_code": "null",
        "magistrate_code": "null",
        "slug": "central-london-employment-tribunal",
        "types": [
            "County Court"
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
        "displayed": True,
        "hide_aols": False,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    }
]


def test_load_people_data_as_list():
    assert isinstance(load_people_data('people.csv'), list) == True


def test_load_people_data_as_list_of_dict():
    assert isinstance(load_people_data('people.csv')[0], dict) == True


def test_no_court_of_type_available():
    assert filter_courts_by_type(COURT_DATA_1, "County Court") == {
        'error': 'No court of desired type available.'}


def test_finds_court_of_type():
    assert filter_courts_by_type(
        COURT_DATA_2, "County Court") == COURT_DATA_2[1]


@patch("test_2.requests")
def test_failed_court_data_retrieval_500(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_request.get.return_value = mock_response

    with pytest.raises(Exception):
        retrieve_nearest_court_of_type("postcode", "desired_type")


@patch("test_2.requests")
def test_failed_court_data_retrieval_400(mock_request):
    mock_response = MagicMock()

    mock_response.status_code = 400
    mock_request.get.return_value = mock_response

    with pytest.raises(Exception):
        retrieve_nearest_court_of_type('WC2B 6EX', 'Tribunal')


@patch("test_2.requests")
@patch("test_2.filter_courts_by_type")
def test_retrieve_nearest_court_of_type_success(mock_filtered_court, mock_request):
    mock_response = MagicMock()

    mock_response.status_code = 200
    mock_request.get.return_value = mock_response
    mock_response.json.return_value = COURT_DATA_2

    mock_filtered_court.return_value = COURT_DATA_2[0]

    assert retrieve_nearest_court_of_type(
        'WC2B 6EX', 'Tribunal') == COURT_DATA_2[0]
