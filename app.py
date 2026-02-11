"""
Flask Backend for AI Automation Agent
Connects frontend to Gemini API securely
"""
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize Gemini client
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main endpoint - receives prompt, calls Gemini, returns response"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400

        prompt = data['prompt']

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({"text": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Load saved task history"""
    try:
        if os.path.exists('agent_history.json'):
            with open('agent_history.json', 'r') as f:
                history = json.load(f)
            return jsonify({"history": history})
        return jsonify({"history": []})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['POST'])
def save_history():
    """Save task history to file"""
    try:
        data = request.get_json()
        history = data.get('history', [])
        with open('agent_history.json', 'w') as f:
            json.dump(history, f, indent=2)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 AI Automation Agent Server Starting...")
    print("📡 Connected to Gemini 2.5 Flash")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

