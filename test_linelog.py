import pytest
from test_1 import is_log_line, get_dict


def test_log_line_incomplete_timestamp_error():
    assert is_log_line(
        "03/11/21 INFO    :....mailbox_register: mailbox allocated for rsvp") == None


def test_log_line_no_timestamp_error():
    assert is_log_line(
        "INFO    :....mailbox_register: mailbox allocated for rsvp") == None


def test_log_line_error_error_type_no():
    assert is_log_line(
        "03/11/21 10:55:22    :....mailbox_register: mailbox allocated for rsvp") == None


def test_log_line_no_message_error():
    assert is_log_line(
        "03/11/21 10:55:22  INFO") == None


def test_get_dict_on_invalid_line():
    assert get_dict("03/11/21 10:55:22  INFO") == None


def test_get_dict_has_timestamp():
    assert get_dict(
        "04/11/21 10:55:21 INFO    :....mailbox_register: mailbox allocated for rsvp-udp").get('timestamp') == "04/11/21 10:55:21"


def test_get_dict_has_log_level():
    assert get_dict(
        "04/11/21 10:55:21 INFO    :....mailbox_register: mailbox allocated for rsvp-udp").get('log_level') == "INFO"


def test_get_dict_has_message():
    assert get_dict(
        "04/11/21 10:55:21 INFO    :....mailbox_register: mailbox allocated for rsvp-udp").get('message') == ":....mailbox_register: mailbox allocated for rsvp-udp"
