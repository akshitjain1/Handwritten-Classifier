def classify_text(text):
    if "Professor" in text or "Teaching" in text:
        return "Academic Document"
    elif "Engineer" in text or "Developer" in text:
        return "Technical Resume"
    else:
        return "General Handwritten Note"
