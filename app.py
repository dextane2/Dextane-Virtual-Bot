from flask import Flask, jsonify, request
from database import get_all_data, store_fixture
import sqlite3, os

app = Flask(__name__)

# ✅ Initialize DB if missing
def init_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team TEXT,
            away_team TEXT,
            odd_home REAL,
            odd_draw REAL,
            odd_away REAL,
            under_2_5 REAL,
            over_1_5 REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "🚀 Dextane Virtual Bot is running successfully on Render!",
        "status": "online"
    })

# Get all data
@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        data = get_all_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Store new fixture
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

# Health check
@app.route("/health")
def health_check():
    return "OK", 200

# Start server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # <-- creates the fixtures table if missing
    app.run(host="0.0.0.0", port=port)
