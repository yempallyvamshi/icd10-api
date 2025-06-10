from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528:free"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    prompt = f"""
You are a certified medical coder with expertise in ICD-10-CM. Interpret user input and respond accordingly:
- If the input is a diagnosis (e.g., "Asthma"), return the correct ICD-10-CM code and description.
- If the input is an ICD-10-CM code (e.g., "J45.909"), return the associated diagnosis.
- Be accurate, brief, and strictly use ICD-10-CM standards.

User Input: {user_input}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-blog-url",  # replace with your Blogger URL
        "X-Title": "ICD10Chatbot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful ICD-10-CM medical coding assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        return jsonify({"response": message})
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"HTTP error: {e.response.text}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "ICD-10 API is live."

if __name__ == "__main__":
    app.run(debug=True)
