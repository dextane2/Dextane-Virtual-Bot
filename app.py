from flask import Flask, render_template, jsonify
from database import get_all_data, save_fixture, init_db
import threading
import scraper
import time

app = Flask(__name__)

# ✅ Ensure the database table exists before anything runs
init_db()

# Home route — show latest scraped records
@app.route('/')
def home():
    records = get_all_data()
    return render_template('index.html', records=records)

# API route — returns live data as JSON
@app.route('/api/data')
def api_data():
    data = get_all_data()
    return jsonify(data)

# Background auto-scraper loop (runs every 2 minutes)
def background_scraper():
    while True:
        try:
            fixtures = scraper.scrape_current_fixtures()
            for fixture in fixtures:
                save_fixture(fixture)
            print(f"✅ Scraped {len(fixtures)} fixtures successfully.")
        except Exception as e:
            print(f"⚠️ Scraper error: {e}")
        time.sleep(120)  # run every 2 minutes

# Start the scraper in a background thread
scraper_thread = threading.Thread(target=background_scraper, daemon=True)
scraper_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
