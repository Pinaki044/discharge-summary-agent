from tools.pdf_reader import extract_pdf_text
from tools.ocr import extract_text_with_ocr
from tools.section_parser import split_into_sections

from schemas.discharge_schema import DischargeSummary

from agents.extractors import (
    extract_diagnoses,
    extract_hospital_course,
    extract_pending_results,
    extract_discharge_medications,
    reconcile_medications
)


pdf_path = "data/patient.pdf"

pages = extract_pdf_text(pdf_path)

if not pages[0]["text"].strip():

    pages = extract_text_with_ocr(pdf_path)

full_text = "\n".join(
    [page["text"] for page in pages]
)

sections = split_into_sections(full_text)

summary = DischargeSummary()

summary = extract_diagnoses(sections, summary)
summary = extract_hospital_course(
    sections,
    summary
)
summary = extract_pending_results(
    sections,
    summary
)

summary = extract_discharge_medications(
    sections,
    summary
)

summary = reconcile_medications(
    summary
)

print("\nEXTRACTED SUMMARY:\n")

print(summary.model_dump())