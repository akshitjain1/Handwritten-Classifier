import streamlit as st
import requests
import re
from utils.ocr import extract_text_tesseract

# ========== CONFIG ==========
API_KEY = "AIzaSyD4l-SRP9XW4XnzGgGnDkZ3e1kvEX9UPkc"
GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={API_KEY}"

# ========== FUNCTIONS ==========
def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEN_URL, headers=headers, json=data)
    return response.json()['candidates'][0]['content']['parts'][0]['text']

def correction_prompt(text):
    return f"""
Correct the grammar and sentence structure of the following text. Maintain the original meaning:

Original Text:
{text}

Return the corrected text only.
"""

def rubric_prompt(text):
    return f"""
You are an evaluator. Evaluate the following text using a detailed rubric.

Text:
{text}

Rubric:
- Grammar (out of 10): Score the grammar, punctuation, spelling, and sentence construction.
- Content Relevance (out of 10): Score how relevant and accurate the content is.
- Structure (out of 10): Evaluate the organization, flow, and coherence.

Then provide the Average Score and an overall Grade (A/B/C/D).

Respond ONLY in this format:
1. Scores:
- Grammar (out of 10): [value]
- Content Relevance (out of 10): [value]
- Structure (out of 10): [value]

2. Average Score: [value]
3. Grade: [value]
4. Feedback:
[Detailed explanation for each category.]
"""

def classification_prompt(text):
    return f"""
Classify the following text into one of the categories:
[Essay, Report, Letter, Application, Summary, Article, Story, Unknown]

Text:
{text}

Respond with only the category name.
"""

def extract_rubric_parts(text):
    try:
        grammar = int(re.search(r"Grammar.*?[:\-\u2013\u2014]?\s*(\d{1,2})", text, re.IGNORECASE).group(1))
        content = int(re.search(r"Content Relevance.*?[:\-\u2013\u2014]?\s*(\d{1,2})", text, re.IGNORECASE).group(1))
        structure = int(re.search(r"Structure.*?[:\-\u2013\u2014]?\s*(\d{1,2})", text, re.IGNORECASE).group(1))

        avg_score = round((grammar + content + structure) / 3, 2)
        if avg_score >= 9:
            grade = "A"
        elif avg_score >= 7:
            grade = "B"
        elif avg_score >= 5:
            grade = "C"
        else:
            grade = "D"

        return {
            "grammar": grammar,
            "content": content,
            "structure": structure,
            "avg_score": avg_score,
            "grade": grade
        }

    except Exception:
        return {
            "grammar": "N/A",
            "content": "N/A",
            "structure": "N/A",
            "avg_score": "N/A",
            "grade": "N/A"
        }

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="Handwritten Grader", layout="centered")

st.title("📝 Handwritten Assignment Grader")
st.caption("OCR + Gemini-based evaluation system")

uploaded_file = st.file_uploader("📤 Upload a handwritten image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with open("temp_image.png", "wb") as f:
        f.write(uploaded_file.getvalue())

    st.image(uploaded_file, caption="🖼 Uploaded Image", use_column_width=True)

    extracted_text = extract_text_tesseract("temp_image.png")
    st.info("✅ Text Extracted from Image")
    st.code(extracted_text, language="text")

    with st.spinner("✨ Correcting grammar..."):
        corrected_text = call_gemini(correction_prompt(extracted_text))

    st.success("✅ Grammar corrected")
    st.text_area("✏️ Corrected Text", corrected_text, height=150)

    # ======= Classification ========
    with st.spinner("🧠 Classifying assignment type..."):
        classification = call_gemini(classification_prompt(corrected_text))

    st.success(f"🏷️ **Predicted Type:** `{classification.strip()}`")

    # ======= Evaluation ========
    with st.spinner("📊 Evaluating the text..."):
        rubric_response = call_gemini(rubric_prompt(corrected_text))

    scores = extract_rubric_parts(rubric_response)

    st.subheader("📝 Detailed Evaluation Report")
    st.markdown(rubric_response)
