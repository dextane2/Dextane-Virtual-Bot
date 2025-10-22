from flask import Flask, jsonify, render_template
from scraper import run_scraper   # ✅ Updated to match the new scraper function
from database import get_fixtures
import threading
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    fixtures = get_fixtures()
    last_updated = fixtures[0]["timestamp"] if fixtures else None
    return render_template('index.html', fixtures=fixtures, last_updated=last_updated)

@app.route('/scrape')
def scrape():
    # Run the scraper in a background thread so it doesn’t block the web app
    threading.Thread(target=run_scraper).start()
    return jsonify({"message": "Scraper started.", "status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
