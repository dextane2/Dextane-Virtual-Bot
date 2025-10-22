from flask import Flask, jsonify, render_template
from scraper import run_scraper
from database import get_all_data  # ✅ matches your current database.py
import threading
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    fixtures = get_all_data()
    last_updated = fixtures[0]["timestamp"] if fixtures else None
    return render_template('index.html', fixtures=fixtures, last_updated=last_updated)

@app.route('/scrape')
def scrape():
    threading.Thread(target=run_scraper).start()
    return jsonify({"message": "Scraper started.", "status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
