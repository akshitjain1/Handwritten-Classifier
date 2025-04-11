from utils.ocr import extract_text_tesseract

if __name__ == "__main__":
    image_path = "data/sample_images/testing1.jpg"
    text = extract_text_tesseract(image_path)
    print("Extracted Text:\n", text)
