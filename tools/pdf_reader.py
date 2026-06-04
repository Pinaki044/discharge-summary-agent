import fitz  # PyMuPDF

from PIL import Image

import pytesseract

import io


# Tesseract installation path (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_pdf(pdf_path):

    pages_text = []

    try:

        print("\nAttempting standard PDF extraction...\n")

        doc = fitz.open(pdf_path)

        for page in doc:

            text = page.get_text()

            pages_text.append(text)

        doc.close()

        combined_text = "".join(pages_text).strip()

        # If normal extraction fails → OCR fallback
        if len(combined_text) < 100:

            print("No embedded text detected.")
            print("Triggering OCR fallback...\n")

            pages_text = ocr_pdf(pdf_path)

        return pages_text

    except Exception as e:

        print(f"PDF extraction failed: {e}")

        return []


def ocr_pdf(pdf_path):

    extracted_pages = []

    try:

        doc = fitz.open(pdf_path)

        for page_number in range(len(doc)):

            page = doc.load_page(page_number)

            pix = page.get_pixmap()

            image_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(image_bytes))

            text = pytesseract.image_to_string(image)

            extracted_pages.append(text)

        doc.close()

        return extracted_pages

    except Exception as e:

        print(f"OCR extraction failed: {e}")

        return []