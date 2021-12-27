import random
import string


def generate_pin_number() -> str:
    return "".join(random.sample(string.digits, 4))
