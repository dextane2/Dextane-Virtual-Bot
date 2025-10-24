from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random

app = Flask(__name__)

# ---------------------------
# Generate random demo data
# ---------------------------
def generate_predictions():
    teams = [
        ("Arsenal", "Chelsea"), ("Liverpool", "Man City"), ("Man Utd", "Tottenham"),
        ("Leicester", "Everton"), ("Brighton", "Newcastle"), ("Aston Villa", "Wolves"),
        ("Crystal Palace", "West Ham"), ("Fulham", "Brentford"), ("Leeds", "Burnley"),
        ("Norwich", "Watford")
    ]
    random.shuffle(teams)
    
    # Simulate Over 1.5 (3 best predictions)
    over_15 = [
        {
            "home": t1,
            "away": t2,
            "confidence": f"{random.randint(85, 96)}%"
        }
        for t1, t2 in teams[:3]
    ]
    
    # Simulate Under 2.5 (2 best predictions)
    under_25 = [
        {
            "home": t1,
            "away": t2,
            "confidence": f"{random.randint(83, 94)}%"
        }
        for t1, t2 in teams[3:5]
    ]

    return over_15, under_25


@app.route("/")
def home():
    try:
        lagos_time = datetime.now(ZoneInfo("Africa/Lagos"))
        next_round_time = lagos_time + timedelta(minutes=2)
        over_15, under_25 = generate_predictions()
        return render_template(
            "index.html",
            now=lagos_time.strftime("%Y-%m-%d %H:%M:%S"),
            next_round=next_round_time.strftime("%Y-%m-%d %H:%M:%S"),
            over15=over_15,
            under25=under_25
        )
    except Exception as e:
        print("Error loading home page:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/scrape")
def scrape_now():
    # Placeholder for your real scraper logic
    return jsonify({
        "message": "Scraper started.",
        "status": "success"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
