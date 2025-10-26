from flask import Flask, render_template, jsonify
from datetime import datetime
import pytz
import random

app = Flask(__name__)

# --- Mock demo data (replace with live SportyBet data later) ---
def generate_demo_predictions():
    teams = [
        ("Chelsea", "Liverpool"),
        ("Arsenal", "Man City"),
        ("Man United", "Tottenham"),
        ("Brighton", "Everton"),
        ("Newcastle", "Aston Villa"),
        ("Leeds", "Brentford")
    ]
    random.shuffle(teams)
    demo_data = {
        "over_15": random.sample(teams, 3),
        "under_25": random.sample(teams, 2)
    }
    return demo_data


@app.route("/")
def home():
    tz = pytz.timezone("Africa/Lagos")
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    demo_data = generate_demo_predictions()
    return render_template("index.html", fixtures=demo_data, now=current_time)


@app.route("/api/fixtures")
def api_fixtures():
    return jsonify(generate_demo_predictions())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
