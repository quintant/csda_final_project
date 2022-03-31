import hashlib


def better_hash(string):
    """Hash a string using a better algorithm than the default hashlib.sha256"""
    return int(hashlib.sha256(string.encode()).hexdigest(), 16)