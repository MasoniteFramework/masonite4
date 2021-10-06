"""String generators and helpers"""
import random
import string


def random_string(length=4):
    """Generate a random string based on the given length.

    Keyword Arguments:
        length {int} -- The amount of the characters to generate (default: {4})

    Returns:
        string
    """
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
