from flask import Flask, jsonify, render_template
import pytz
from datetime import datetime
import random

app = Flask(__name__)

# Demo fixture generator (simulating new VFL rounds)
def generate_demo_fixtures():
    teams = [
        "Chelsea", "Arsenal", "Liverpool", "Man City", "Tottenham",
        "Man United", "Newcastle", "Leeds", "Everton", "Aston Villa"
    ]
    predictions = ["Over 1.5 Goals", "Under 2.5 Goals", "BTTS", "Home Win", "Away Win"]
    fixtures = []
    for _ in range(2):
        home, away = random.sample(teams, 2)
        fixtures.append({
            "home": home,
            "away": away,
            "prediction": random.choice(predictions),
            "kickoff": random.choice(["14:30", "14:45", "15:00", "15:15"])
        })
    return fixtures

# Store fixtures globally for demo mode
fixtures = generate_demo_fixtures()

@app.route("/")
def home():
    lagos_tz = pytz.timezone("Africa/Lagos")
    lagos_time = datetime.now(lagos_tz)
    return render_template("index.html",
                           now=lagos_time.strftime("%Y-%m-%d %H:%M:%S"),
                           fixtures=fixtures)

@app.route("/scrape")
def scrape():
    """
    Trigger a simulated scrape.
    Later this will be replaced with real SportyBet data scraping.
    """
    global fixtures
    try:
        fixtures = generate_demo_fixtures()
        print("✅ Simulated scrape triggered. Fixtures updated.")
        return jsonify({
            "status": "success",
            "message": "Fixtures refreshed successfully.",
            "fixtures": fixtures
        })
    except Exception as e:
        print("❌ Error scraping:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
