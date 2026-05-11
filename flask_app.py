"""
Flask Web Interface for Email Verification Tool
Alternative lightweight HTTP API + HTML interface
"""

from flask import Flask, render_template, request, jsonify
from email_verifier import verify_email
import json

app = Flask(__name__)

# Enable CORS if needed
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response

app.after_request(after_request)


@app.route('/')
def index():
    """Serve the main HTML interface."""
    return render_template('index.html')


@app.route('/api/verify', methods=['POST'])
def api_verify():
    """API endpoint for email verification."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        check_web_presence = data.get('check_web_presence', True)
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        result = verify_email(email, check_web_presence)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    print("🚀 Starting Flask Email Verification Server...")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
