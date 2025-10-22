from flask import Flask, jsonify, render_template
from scraper import run_scraper
from database import get_all_data  # ✅ works with your existing database.py
import threading
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    try:
        fixtures = get_all_data() or []
        # Handle both list of tuples and list of dicts
        if fixtures and isinstance(fixtures[0], tuple):
            fixtures = [
                {
                    "home_team": row[0],
                    "away_team": row[1],
                    "over_1_5": row[2],
                    "under_2_5": row[3],
                    "timestamp": row[4],
                }
                for row in fixtures
            ]
        last_updated = fixtures[0]["timestamp"] if fixtures else "No records yet"
        return render_template("index.html", fixtures=fixtures, last_updated=last_updated)
    except Exception as e:
        # Log and show an error message safely
        print("Error loading home page:", e)
        return f"Error loading data: {e}", 500

@app.route('/scrape')
def scrape():
    threading.Thread(target=run_scraper).start()
    return jsonify({"message": "Scraper started.", "status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
