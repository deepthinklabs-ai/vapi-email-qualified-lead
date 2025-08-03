from flask import Flask, request, jsonify
from send_lead_email import send_lead_email
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def ping():
    """Simple health-check endpoint."""
    return "pong", 200


@app.route("/send-lead-email", methods=["POST"])
def handle_lead():
    """
    Validate JSON payload, trigger SendGrid email.
    Returns 400 on missing fields, 500 on SendGrid failure.
    """
    data = request.get_json(force=True)

    required = [
        "name",
        "phone",
        "email",
        "bamboo_type",
        "volume",
        "call_summary",
    ]
    if not all(k in data and data[k] for k in required):
        return jsonify({"error": "Missing one or more required fields."}), 400

    try:
        send_lead_email(
            data["name"],
            data["phone"],
            data["email"],
            data["bamboo_type"],
            data["volume"],
            data["call_summary"],
        )
        return jsonify({"status": "Email sent"}), 200

    except Exception as e:
        # Log the exception; Flask will still return JSON to the caller.
        app.logger.error("SendGrid error: %s", e, exc_info=True)
        return jsonify({"error": "Failed to send email"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


