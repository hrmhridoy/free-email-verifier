from flask import Flask, request, jsonify
from email_verifier import verify_email

app = Flask(__name__)


@app.route('/', methods=['POST'])
def verify():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    email = data.get('email', '').strip()
    check_web_presence = data.get('check_web_presence', True)

    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = verify_email(email, check_web_presence)
    return jsonify(result), 200
