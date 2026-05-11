from flask import Flask, request, jsonify
from email_verifier import verify_email
import traceback

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.exception('API error')
    message = str(error) or 'Unknown server error'
    return jsonify({
        'error': 'Server error',
        'message': message
    }), 500


@app.route('/api/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        return jsonify({
            'status': 'ready',
            'message': 'Email verification API is available.'
        }), 200

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    email = data.get('email', '').strip()
    check_web_presence = data.get('check_web_presence', True)

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    result = verify_email(email, check_web_presence)
    return jsonify(result), 200
