from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    # Simulated response – Replace with real logic or AI call
    icd10_lookup = {
        "Asthma": "J45.909",
        "Diabetes": "E11.9",
        "Hypertension": "I10",
        "Fracture of femur": "S72.001A"
    }

    code = icd10_lookup.get(message, "ICD-10 code not found.")
    return jsonify({"response": f"ICD-10 code for '{message}' is: {code}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
