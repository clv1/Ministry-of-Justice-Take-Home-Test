import pytest
from test_3 import sum_current_time


def test_invalid_hour():
    with pytest.raises(ValueError):
        sum_current_time("24:02:30")


def test_invalid_negative_hour():
    with pytest.raises(ValueError):
        sum_current_time("21:72:30")


def test_invalid_data_type():
    with pytest.raises(TypeError):
        sum_current_time("aa:02:30")


def test_invalid_data_type_decimal():
    with pytest.raises(TypeError):
        sum_current_time("2.:02:30")


def test_successful_sum_two_digits():
    assert sum_current_time("21:22:30") == 73


def test_successful_sum_single_digits():
    assert sum_current_time("04:03:12") == 19


def test_successful_sum_zeroes():
    assert sum_current_time("23:00:00") == 23
