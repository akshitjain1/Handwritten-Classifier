import pytesseract
from PIL import Image

def extract_text_tesseract(image_path):
    image = Image.open(image_path).convert("L")  # grayscale
    text = pytesseract.image_to_string(image)
    return text.strip()
