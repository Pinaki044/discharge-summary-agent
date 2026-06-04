import re


def is_garbage_text(text):

    text = text.strip()

    if len(text) < 5:
        return True

    strange_chars = re.findall(r"[^a-zA-Z0-9\s\-\.,:/()]", text)

    if len(strange_chars) > 5:
        return True

    words = text.split()

    if len(words) <= 2:
        return True

    return False