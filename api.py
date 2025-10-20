from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from webull_adapter import save_credentials

app = Flask(__name__)
# Allow requests from your Next.js development server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/credentials', methods=['POST'])
def update_credentials():
    """
    API endpoint to receive and save Webull credentials.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400

    save_credentials(email, password)
    
    return jsonify({"status": "success", "message": "Credentials saved successfully"})

if __name__ == '__main__':
    app.run(port=5001, debug=True)