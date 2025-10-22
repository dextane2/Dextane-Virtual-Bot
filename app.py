from flask import Flask, render_template, jsonify
from database import get_all_data, store_fixture
from scraper import scrape_sportybet
import threading
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    records = get_all_data()
    return render_template("index.html", records=records, now=datetime.datetime.now())

@app.route("/scrape", methods=["GET"])
def trigger_scrape():
    """Endpoint to trigger scraping manually or by cron-job"""
    try:
        threading.Thread(target=scrape_sportybet, daemon=True).start()
        return jsonify({"status": "success", "message": "Scraper started."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
