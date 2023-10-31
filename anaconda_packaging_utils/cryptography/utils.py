"""
File:           utils.py
Description:    Library that provides cryptography and hashing-related utility functions.
"""
import string


def is_valid_hex(s: str) -> bool:
    """
    Checks if a string is a valid hex string
    :param s:   String to validate
    :return: True if the string is a valid hex string. False otherwise.
    """
    return all(c in string.hexdigits for c in s)


def is_valid_md5(s: str) -> bool:
    """
    Checks if a string is a valid MD5 hash
    :param s:   String to validate
    :return: True if the string is a valid MD5 hash. False otherwise.
    """
    return len(s) == 32 and is_valid_hex(s)


def is_valid_sha256(s: str) -> bool:
    """
    Checks if a string is a valid SHA-256 hash
    :param s:   String to validate
    :return: True if the string is a valid SHA-256 hash. False otherwise.
    """
    return len(s) == 64 and is_valid_hex(s)


def is_valid_sha1(s: str) -> bool:
    """
    Checks if a string is a valid SHA-1 hash. This is used by git/GitHub.
    :param s:   String to validate
    :return: True if the string is a valid SHA-1 hash. False otherwise.
    """
    return len(s) == 40 and is_valid_hex(s)


def cast_hex_str_to_int(s: str) -> int:
    """
    Converts a hex string to an integer
    :param s:   String to convert. This must be a valid hex-string.
    :return: Integer equivalent of a hex string.
    """
    return int(s, 16)
