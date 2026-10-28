from tinbox.helper import is_hex_code


def test_is_hex_code():
    sample_cases = [
        ("#CD5C5C", True),
        ("#EAECEE", True),
        ("#eaecee", True),
        ("#000000", True),
        ("#CD5C58C", False),
        ("#CD5C5Z", False),
        ("#CD5C&C", False),
        ("EFCD12", False),
    ]
    for input_str, expected_output in sample_cases:
        assert is_hex_code(input_str) == expected_output
