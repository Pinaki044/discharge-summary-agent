from tools.pdf_reader import extract_pdf_text
from tools.ocr import extract_text_with_ocr

from agents.planner import PlanningAgent


def main():

    pdf_path = "data/patient.pdf"

    print("\nAttempting standard PDF extraction...\n")

    extracted_text = extract_pdf_text(pdf_path)

    first_page_text = extracted_text[0]["text"].strip()

    # OCR fallback
    if not first_page_text:

        print("No embedded text detected.")
        print("Triggering OCR fallback...\n")

        extracted_text = extract_text_with_ocr(pdf_path)

    else:

        print("Embedded text successfully extracted.\n")

    agent = PlanningAgent()

    agent.run(extracted_text)

    print("\nFIRST PAGE TEXT SAMPLE:\n")

    print(extracted_text[0]["text"][:3000])


if __name__ == "__main__":

    main()