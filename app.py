from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import pytz
import asyncio
from scraper import get_live_vfl_fixtures  # <-- new smart scraper function

app = Flask(__name__)

lagos_tz = pytz.timezone("Africa/Lagos")

@app.route("/")
def home():
    now = datetime.now(lagos_tz)
    next_round = now + timedelta(minutes=2)
    try:
        fixtures = asyncio.run(get_live_vfl_fixtures())
        over_15 = fixtures.get("over_15", [])
        under_25 = fixtures.get("under_25", [])
    except Exception as e:
        print("Error fetching SportyBet data:", e)
        over_15, under_25 = [], []

    return render_template(
        "index.html",
        over_15=over_15,
        under_25=under_25,
        now=now.strftime("%Y-%m-%d %H:%M:%S"),
        next_round=next_round.strftime("%Y-%m-%d %H:%M:%S"),
    )

@app.route("/scrape")
def scrape():
    try:
        asyncio.run(get_live_vfl_fixtures())
        return jsonify({"message": "Scraper started.", "status": "success"})
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
