import fitz
import pytesseract
from PIL import Image
import io


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_with_ocr(pdf_path):

    extracted_pages = []

    try:

        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):

            page = doc.load_page(page_num)

            pix = page.get_pixmap()

            img_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(img_bytes))

            text = pytesseract.image_to_string(image)

            extracted_pages.append({
                "page": page_num + 1,
                "text": text
            })

        return extracted_pages

    except Exception as e:

        print(f"OCR Error: {e}")

        return []