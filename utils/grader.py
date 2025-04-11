import requests
import json

API_KEY = "AIzaSyALffFp3Uh_s1sOoMDU-xBGK-aX_CbIcFo"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def rubric_grade(text):
    prompt = (
        "You are an evaluator for handwritten assignments. Analyze the text based on this rubric:\n"
        "- Grammar (score out of 10): Check sentence structure, spelling, punctuation\n"
        "- Content Relevance (score out of 10): How well it covers the intended topic, clarity\n"
        "- Structure (score out of 10): Logical flow, paragraphing, coherence\n\n"
        "Then, provide:\n"
        "1. A score out of 10 for each section\n"
        "2. A total average score\n"
        "3. A grade (A: 9-10, B: 7-8.9, C: 5-6.9, D: below 5)\n"
        "4. Feedback on each section\n\n"
        f"Assignment:\n{text}"
    )

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
        result = response.json()
        output = result['candidates'][0]['content']['parts'][0]['text'].strip()

        return output
    except Exception as e:
        return f"Error grading with rubric: {e}"
