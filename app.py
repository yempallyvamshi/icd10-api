from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528:free"  # You can also try: mistralai/mistral-7b-instruct, openai/gpt-4, etc.

# Serve the frontend
@app.route("/", methods=["GET"])
def index():
    return send_file("frontend.html")

# Main chat endpoint
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
        "HTTP-Referer": "http://localhost:5000",   # Required by OpenRouter (can be your app URL)
        "X-Title": "ICD10Chatbot"                  # Required (name of your app)
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

if __name__ == "__main__":
    app.run(debug=True)
