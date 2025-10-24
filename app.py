from flask import Flask, render_template
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# Lagos timezone
lagos_tz = pytz.timezone("Africa/Lagos")

@app.route("/")
def home():
    now = datetime.now(lagos_tz)
    next_round = now + timedelta(minutes=2)

    # Demo data (Over 1.5 and Under 2.5 predictions)
    over_15 = [
        {"home": "Chelsea", "away": "Arsenal", "prediction": "Over 1.5"},
        {"home": "Barcelona", "away": "Real Madrid", "prediction": "Over 1.5"},
        {"home": "PSG", "away": "Marseille", "prediction": "Over 1.5"},
    ]

    under_25 = [
        {"home": "Juventus", "away": "Inter Milan", "prediction": "Under 2.5"},
        {"home": "Atletico", "away": "Sevilla", "prediction": "Under 2.5"},
    ]

    return render_template(
        "index.html",
        over_15=over_15,
        under_25=under_25,
        now=now.strftime("%Y-%m-%d %H:%M:%S"),
        next_round=next_round.strftime("%Y-%m-%d %H:%M:%S"),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
