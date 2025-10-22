from flask import Flask, jsonify, request
from database import get_all_data, store_fixture, init_db
import os

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 Dextane Virtual Bot is running successfully on Render!",
        "status": "online"
    })

# Endpoint to get all stored data
@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        data = get_all_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to store new fixture (data)
@app.route("/api/store", methods=["POST"])
def store_data():
    try:
        content = request.get_json()
        if not content:
            return jsonify({"error": "No JSON data provided"}), 400
        store_fixture(content)
        return jsonify({"message": "Data stored successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check (used by Render)
@app.route("/health")
def health_check():
    return "OK", 200

# Initialize the database on startup
def init_db():
    """Initialize the database (create tables if not exist)."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base

    engine = create_engine("sqlite:///data.db")
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully")

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(host="0.0.0.0", port=port)
