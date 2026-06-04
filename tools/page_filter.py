import re


IMPORTANT_KEYWORDS = [
    "DIAGNOSIS",
    "HISTORY",
    "INVESTIGATION",
    "COURSE",
    "DISCHARGE",
    "MEDICATION",
    "ALLERG",
    "FOLLOW UP",
    "HOSPITAL"
]


def is_meaningful_page(text):

    if len(text.strip()) < 100:
        return False

    keyword_matches = 0

    for keyword in IMPORTANT_KEYWORDS:

        if keyword.lower() in text.lower():
            keyword_matches += 1

    english_word_count = len(
        re.findall(r"\b[a-zA-Z]{3,}\b", text)
    )

    if keyword_matches >= 1 and english_word_count > 30:
        return True

    return False


def filter_meaningful_pages(pages):

    filtered_pages = []

    for page in pages:

        if is_meaningful_page(page["text"]):

            filtered_pages.append(page)

    return filtered_pages