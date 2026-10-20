def is_hex_code(s: str) -> bool:
    """
    Returns True if the string is a valid hex code with a leading hash, False otherwise.
    """
    if len(s) != 7 or not s.startswith("#"):
        return False
    for char in s[1:]:
        if not (char.isdigit() or char.lower() in "abcdef"):
            return False
    return True
