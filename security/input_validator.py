import re

def reject_suspicious_input(value: str):
    if len(value) > 128 or re.search(r"[\x00-\x1f<>]", value):
        raise ValueError("Input contains unsupported characters or length")
    return value
