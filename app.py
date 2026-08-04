from flask import Flask, jsonify, request
import os

# Load .env when available, but don't crash if python-dotenv is not installed or no .env exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # In production Render provides environment variables via the dashboard — it's fine if dotenv is missing
    pass

app = Flask(__name__)
# Ensure SECRET_KEY comes from env in production
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')

@app.route("/")
def index():
    return jsonify(message="Bienvenido a Pakazita Tienda!")

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
