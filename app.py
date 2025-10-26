from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import pytz
import random

app = Flask(__name__, static_folder="static", template_folder="templates")

LAGOS = pytz.timezone("Africa/Lagos")
COUNTDOWN_SECONDS = 120  # 2 minutes

# Demo data (you can replace this with real scraper later)
DEMO_OVER = [
    "BOU vs EVE - Over 1.5",
    "FUL vs BRE - Over 1.5",
    "LEI vs LEE - Over 1.5"
]

DEMO_UNDER = [
    "MCI vs WOL - Under 2.5",
    "TOT vs NEW - Under 2.5"
]


def build_demo_predictions():
    # Shuffle to give appearance of change
    over = random.sample(DEMO_OVER, 3)
    under = random.sample(DEMO_UNDER, 2)
    return over, under


@app.route("/")
def index():
    now = datetime.now(LAGOS)
    next_round = now + timedelta(seconds=COUNTDOWN_SECONDS)
    over, under = build_demo_predictions()
    return render_template(
        "index.html",
        now=now.strftime("%Y-%m-%d %H:%M:%S"),
        next_round=next_round.strftime("%Y-%m-%d %H:%M:%S"),
        over=over,
        under=under,
        countdown=COUNTDOWN_SECONDS
    )


@app.route("/api/predictions")
def api_predictions():
    """Return JSON with demo predictions and timestamp (for AJAX refresh)."""
    now = datetime.now(LAGOS)
    over, under = build_demo_predictions()
    return jsonify({
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "over": over,
        "under": under,
        "countdown": COUNTDOWN_SECONDS
    })


@app.route("/scrape")
def scrape_now():
    """Manual scrape endpoint — currently regenerates demo predictions."""
    now = datetime.now(LAGOS)
    over, under = build_demo_predictions()
    return jsonify({
        "status": "success",
        "message": "Demo predictions refreshed.",
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "over": over,
        "under": under,
        "countdown": COUNTDOWN_SECONDS
    })


if __name__ == "__main__":
    # For local testing; Render will use gunicorn in production
    app.run(host="0.0.0.0", port=10000)
