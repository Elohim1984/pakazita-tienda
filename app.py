from flask import Flask, jsonify, request
import os
import logging

# Load .env when available, but don't crash if python-dotenv is not installed or no .env exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # In production Render provides environment variables via the dashboard — it's fine if dotenv is missing
    pass

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
# Ensure SECRET_KEY comes from env in production
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')
# Database config: SQLAlchemy reads SQLALCHEMY_DATABASE_URI from env variable DATABASE_URL or SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create extension objects without binding to app yet. We'll bind only if a DB URL is provided.
db = SQLAlchemy()
migrate = Migrate()

# Try to configure the database from env vars; do NOT crash if it's missing so the app can still run (health checks etc.)
db_url = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    migrate.init_app(app, db)
else:
    logging.warning("No DATABASE_URL/SQLALCHEMY_DATABASE_URI found — database features are disabled until you set DATABASE_URL.")

# Simple models placed here for ease of demo — in larger apps move to a separate module
class User(db.Model if db else object):
    __tablename__ = 'users'
    if db:
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model if db else object):
    __tablename__ = 'products'
    if db:
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        description = db.Column(db.Text, nullable=True)
        price = db.Column(db.Numeric(10,2), nullable=False, default=0.00)
        stock = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
