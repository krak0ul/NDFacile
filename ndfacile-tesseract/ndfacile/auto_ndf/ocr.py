import pytesseract
from PIL import ImageFile


class Océaire():
    @staticmethod
    def extract_text(img: ImageFile) -> str:
        """
        Extracts text from image using Tesseract
        Returns a string of raw extracted text
        """
        try:
            # TODO: make lang a global var
            return pytesseract.image_to_string(img, lang='fra', timeout=2)
        
        except RuntimeError as timeout:
            raise timeout(f"OCR timed out (2s)")