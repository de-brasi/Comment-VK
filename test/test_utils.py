import sys


def custom_assert(actual_value, expected_value, hint: str) -> None:
    if actual_value != expected_value:
        sys.stderr.write(f"Assertion error: expected {expected_value} but received {actual_value}; {hint}\n")
