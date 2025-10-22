from flask import Flask, render_template, jsonify
from database import get_all_data, store_fixture, init_db
import threading
import scraper
import time

app = Flask(__name__)

# ✅ Make sure the database table exists before anything starts
init_db()

@app.route('/')
def home():
    records = get_all_data()
    return render_template('index.html', records=records)

@app.route('/api/data')
def api_data():
    data = get_all_data()
    return jsonify(data)

# 🔁 Background scraper that runs every 2 minutes
def background_scraper():
    while True:
        try:
            fixtures = scraper.scrape_current_fixtures()
            for fixture in fixtures:
                store_fixture(fixture)
            print(f"✅ Scraped {len(fixtures)} fixtures successfully.")
        except Exception as e:
            print(f"⚠️ Scraper error: {e}")
        time.sleep(120)  # repeat every 2 minutes

# Start background scraper thread
scraper_thread = threading.Thread(target=background_scraper, daemon=True)
scraper_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
