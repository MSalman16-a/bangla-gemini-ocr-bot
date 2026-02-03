import google.generativeai as genai
from PIL import Image
import json

def run_gemini(api_key, images, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    responses = []

    for img in images:
        res = model.generate_content([img, prompt])
        responses.append(res.text)

    # Gemini sometimes splits JSON — merge safely
    joined = "\n".join(responses)

    try:
        return json.loads(joined)
    except:
        # fallback: try to extract JSON
        start = joined.find("[")
        end = joined.rfind("]") + 1
        return json.loads(joined[start:end])
