from flask import Flask, render_template, jsonify
from threading import Thread
from database import get_all_data
import time
import scraper  # Import the module, not a function from it

app = Flask(__name__)

@app.route("/")
def home():
    try:
        records = get_all_data()
        return render_template(
            "index.html",
            records=records,
            now=time.strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        print(f"Error loading home page: {e}")
        return f"An error occurred while loading the dashboard: {e}", 500


@app.route("/scrape")
def start_scraper():
    try:
        thread = Thread(target=scraper.run_scraper)
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
    app.run(host="0.0.0.0", port=5000)
