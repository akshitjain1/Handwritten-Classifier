import requests
import json

API_KEY = "AIzaSyALffFp3Uh_s1sOoMDU-xBGK-aX_CbIcFo"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def grammarly_correct(text):
    prompt = f"Correct the following text grammatically:\n\n{text}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
    result = response.json()
    try:
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error parsing Gemini response: {e}"
