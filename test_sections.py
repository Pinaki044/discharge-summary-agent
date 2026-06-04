from tools.pdf_reader import extract_pdf_text
from tools.ocr import extract_text_with_ocr
from tools.section_parser import split_into_sections


pdf_path = "data/patient.pdf"

pages = extract_pdf_text(pdf_path)

if not pages[0]["text"].strip():

    pages = extract_text_with_ocr(pdf_path)

full_text = "\n".join(
    [page["text"] for page in pages]
)

sections = split_into_sections(full_text)

for section_name, content in sections.items():

    print("\n====================")

    print(section_name)

    print("====================\n")

    print(content[:1000])