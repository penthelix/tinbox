def is_valid_youtube_url(url: str) -> bool:
    return url.startswith("https://www.youtube.com/feeds/videos.xml?channel_id=")


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


def sanitized_filename(s: str) -> str:
    """
    Return a sanitized string by retaining only alphanumeric characters, parentheses,
    hyphens, and underscores.
    """
    keep_chars = {"(", ")", "-", "_"}  # The order of chars is from string.whitespace
    return "".join(c for c in s if c.isalpha() or c.isdigit() or c in keep_chars)
