import hashlib


def better_hash(string):
    """
    Stable hash function for strings. Is needed so that the same string gives the same hash
    every time.
    """
    return int(hashlib.sha256(string.encode()).hexdigest(), 16)
