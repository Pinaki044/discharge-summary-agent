import re
from tools.safety_checks import is_garbage_text

from schemas.discharge_schema import (
    DischargeSummary,
    PendingResult,
    MedicationChange
)


INVALID_DIAGNOSIS_PATTERNS = [
    "doctor",
    "signature",
    "drug chart",
    "weight",
    "route",
    "dose",
    "freq",
    "admission record",
    "case record",
    "regular prescription",
    "drug & dosage"
]


def is_valid_diagnosis(text):

    clean_text = text.lower().strip()

    # Too short
    if len(clean_text) < 8:
        return False

    # Reject excessive symbols/numbers
    symbol_count = len(
        re.findall(r"[^a-zA-Z\s]", clean_text)
    )

    if symbol_count > 5:
        return False

    # Reject noisy patterns
    for pattern in INVALID_DIAGNOSIS_PATTERNS:

        if pattern in clean_text:
            return False

    words = clean_text.split()

    # Must contain at least 2 meaningful words
    if len(words) < 2:
        return False

    # Reject too many tiny words
    meaningful_words = [
        word for word in words
        if len(word) >= 3
    ]

    if len(meaningful_words) < 2:
        return False

    # Reject random uppercase-like OCR fragments
    vowel_count = len(
        re.findall(r"[aeiou]", clean_text)
    )

    if vowel_count < 2:
        return False

    return True

def diagnosis_confidence(text):

    score = 0

    clean_text = text.lower()

    # Longer phrases are more likely real diagnoses
    if len(clean_text) > 15:
        score += 2

    # Multiple meaningful words
    words = clean_text.split()

    if len(words) >= 2:
        score += 2

    # Medical-like words
    medical_keywords = [
        "infection",
        "disease",
        "syndrome",
        "failure",
        "injury",
        "dehydration",
        "gastro",
        "fever",
        "diabetes",
        "hypertension",
        "uti",
        "colitis"
    ]

    for keyword in medical_keywords:

        if keyword in clean_text:
            score += 3
            break

    # Penalize excessive symbols
    symbol_count = len(
        re.findall(r"[^a-zA-Z\s]", clean_text)
    )

    if symbol_count > 3:
        score -= 2

    # Penalize weird OCR fragments
    vowel_count = len(
        re.findall(r"[aeiou]", clean_text)
    )

    if vowel_count < 2:
        score -= 2

    return score

def extract_diagnoses(sections, summary: DischargeSummary):

    diagnosis_text = sections.get("DIAGNOSIS", "")

    if not diagnosis_text:

        summary.clinician_review_flags.append(
            "Diagnosis section missing."
        )

        return summary

    diagnoses = []

    lines = diagnosis_text.split("\n")

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        clean_line = re.sub(
            r"^\d+[\).\-\s]*",
            "",
            clean_line
        )

        if is_valid_diagnosis(clean_line):

            confidence = diagnosis_confidence(clean_line)

            if confidence >= 4:

                if not is_garbage_text(clean_line):

                    diagnoses.append(clean_line)

                else:

                    summary.clinician_review_flags.append(
                        f"OCR-noisy diagnosis ignored: {clean_line}"
                    )
            else:
                summary.clinician_review_flags.append(
                    f"Low-confidence diagnosis candidate: {clean_line}"
                )

    # Remove duplicates
    diagnoses = list(dict.fromkeys(diagnoses))

    if diagnoses:

        summary.principal_diagnosis = diagnoses[0]

        if len(diagnoses) > 1:

            summary.secondary_diagnoses = diagnoses[1:]

    else:

        summary.clinician_review_flags.append(
            "Unable to confidently extract diagnoses."
        )

    return summary

def extract_hospital_course(sections, summary):

    course_text = sections.get(
        "COURSE IN THE HOSPITAL",
        ""
    )

    if not course_text:

        summary.clinician_review_flags.append(
            "Hospital course section missing."
        )

        return summary

    # Clean excessive whitespace
    course_text = " ".join(
        course_text.split()
    )

    summary.hospital_course = course_text

    return summary

def extract_pending_results(sections, summary):

    combined_text = " ".join(
        sections.values()
    ).lower()

    pending_keywords = [
        "awaited",
        "pending",
        "yet to come",
        "report awaited"
    ]

    findings = []

    sentences = combined_text.split(".")

    for sentence in sentences:

        for keyword in pending_keywords:

            if keyword in sentence:

                clean_sentence = sentence.strip()

                if clean_sentence:

                    findings.append(clean_sentence)

    # Remove duplicates
    findings = list(dict.fromkeys(findings))

    if findings:

        structured_pending = []

        for item in findings:

            structured_pending.append(
                PendingResult(
                   test_name=item,
                   status="PENDING"
                )
            )

        summary.pending_results = structured_pending

    return summary

def extract_discharge_medications(sections, summary):

    medication_keywords = [
        "tablet",
        "tab",
        "capsule",
        "cap",
        "injection",
        "syrup",
        "mg",
        "ml"
    ]

    medications = []

    combined_text = " ".join(
        sections.values()
    )

    lines = combined_text.split("\n")

    for line in lines:

        clean_line = line.strip()

        lower_line = clean_line.lower()

        for keyword in medication_keywords:

            if keyword in lower_line:

                bad_keywords = [
                    "blood sugar",
                    "creatinine",
                    "doctor",
                    "witnessing",
                    "capillary",
                    "temperature",
                    "mlc",
                    "reports enclosed",
                    "hemodynamically",
                    "mmhg"
                ]

                is_bad = False

                for bad in bad_keywords:

                    if bad in lower_line:

                        is_bad = True
                        break

                if len(clean_line) > 5 and not is_bad:

                    if not is_garbage_text(clean_line):

                        medications.append(clean_line)

                    else:

                        summary.clinician_review_flags.append(
                            f"Suspicious medication OCR ignored: {clean_line}"
                        )

    # Remove duplicates
    medications = list(dict.fromkeys(medications))

    summary.discharge_medications = medications

    return summary

def reconcile_medications(summary):

    for med in summary.discharge_medications:

        summary.medication_changes.append(

            MedicationChange(
                medication_name=med,
                change_type="ADDED",
                reason=None,
                needs_review=True
            )
        )

    return summary

