"""
Generate codes for use throughout the API (activation codes, forgot password codes, etc.)
Author: Andrew Jarombek
Date: 7/4/2019
"""

import secrets
import string


def generate_code(length: int = 8) -> str:
    """
    Generate a random code of a given length.
    :param length: Integer length of the secret code.
    :return: String representing a code.
    """
    return "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
