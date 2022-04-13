import hashlib


def better_hash(string: str) -> int:
    """
    Stable hash function for strings. Is needed so that the same string gives
    the same hash every time.

    Args:
        string (str): the string to hash
    Returns:
        int: the hash of the string
    """
    return int(hashlib.sha256(string.encode()).hexdigest(), 16)
