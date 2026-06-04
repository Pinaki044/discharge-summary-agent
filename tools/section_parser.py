import re


SECTION_HEADERS = [
    "DIAGNOSIS",
    "HISTORY",
    "PAST HISTORY",
    "PHYSICAL EXAMINATION",
    "INVESTIGATIONS",
    "COURSE IN THE HOSPITAL",
    "MEDICATIONS",
    "ALLERGIES",
    "FOLLOW UP",
    "DISCHARGE CONDITION"
]


def split_into_sections(text):

    sections = {}

    current_section = "UNKNOWN"

    sections[current_section] = []

    # Create dynamic regex pattern
    headers_pattern = "|".join(
        [re.escape(header) for header in SECTION_HEADERS]
    )

    pattern = rf"({headers_pattern}):?"

    parts = re.split(pattern, text, flags=re.IGNORECASE)

    i = 0

    while i < len(parts):

        part = parts[i].strip()

        upper_part = part.upper()

        if upper_part in SECTION_HEADERS:

            current_section = upper_part

            if current_section not in sections:
                sections[current_section] = []

            if i + 1 < len(parts):

                content = parts[i + 1].strip()

                sections[current_section].append(content)

                i += 2

            else:
                i += 1

        else:

            sections[current_section].append(part)

            i += 1

    # Convert lists into strings
    for key in sections:

        sections[key] = "\n".join(
            sections[key]
        ).strip()

    return sections
