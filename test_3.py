"""Test 3"""
# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.

HOURS = 24
MINUTES = 60
SECONDS = 60


def sum_current_time(time_str: str) -> int:
    """
    Expects a string of data in the format HH:MM:SS as input.
    The time divisions HH, MM, SS are extracted and validated.
    Returns the sum of the time divisions.
    """
    list_of_nums = time_str.split(":")

    try:
        hour, minute, second = int(list_of_nums[0]), int(
            list_of_nums[1]), int(list_of_nums[2])
    except Exception as err:
        raise TypeError("Time division data of invalid type.") from err

    if hour not in range(HOURS) or minute not in range(MINUTES) or second not in range(SECONDS):
        raise ValueError("Time division out of acceptable bounds.")

    return hour + minute + second


if __name__ == "__main__":
    print(sum_current_time("21:31:01"))
