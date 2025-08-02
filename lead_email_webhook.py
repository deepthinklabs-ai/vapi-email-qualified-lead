from flask import Flask, request, jsonify
from send_lead_email import send_lead_email
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/send-lead-email", methods=["POST"])
def handle_lead():
    try:
        data = request.json

        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        bamboo_type = data.get("bamboo_type")
        volume = data.get("volume")
        summary = data.get("call_summary")

        if not all([name, phone, email, bamboo_type, volume, summary]):
            return jsonify({"error": "Missing one or more required fields."}), 400

        send_lead_email(name, phone, email, bamboo_type, volume, summary)
        return jsonify({"status": "Email sent"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8080)
