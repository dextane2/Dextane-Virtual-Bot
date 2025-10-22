from flask import Flask, render_template, jsonify
from threading import Thread
from database import get_all_data
from scraper import run_scraper
import time

app = Flask(__name__)

@app.route("/")
def home():
    try:
        # Fetch all stored fixtures from database
        records = get_all_data()

        # Render the dashboard with current timestamp
        return render_template(
            "index.html",
            records=records,
            now=time.strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        print(f"Error loading home page: {e}")
        return f"An error occurred while loading the dashboard: {e}", 500


@app.route("/scrape")
def scrape():
    try:
        # Run the scraper in a background thread to avoid freezing the UI
        thread = Thread(target=run_scraper)
        thread.start()

        return jsonify({
            "message": "Scraper started successfully.",
            "status": "success",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        print(f"Scraper error: {e}")
        return jsonify({
            "message": f"Scraper failed: {e}",
            "status": "error"
        })


if __name__ == "__main__":
    # Run app locally (Render uses gunicorn in production)
    app.run(host="0.0.0.0", port=5000, debug=False)
