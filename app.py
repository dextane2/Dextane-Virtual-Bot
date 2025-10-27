from flask import Flask, render_template, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

# --------------------------------------
# DEMO DATA (replace later with real scrape)
# --------------------------------------
fixtures = {
    "over15": [
        "Manchester Utd vs Chelsea",
        "Arsenal vs Liverpool",
        "Man City vs Tottenham"
    ],
    "under25": [
        "Everton vs Crystal Palace",
        "Leeds vs Aston Villa"
    ]
}

# --------------------------------------
# LAGOS TIME (WAT)
# --------------------------------------
def get_lagos_time():
    lagos_tz = pytz.timezone("Africa/Lagos")
    return datetime.now(lagos_tz)

# --------------------------------------
# HOME PAGE
# --------------------------------------
@app.route("/")
def home():
    try:
        lagos_time = get_lagos_time().strftime("%I:%M %p")  # 12-hour format
        return render_template("index.html", fixtures=fixtures, now=lagos_time)
    except Exception as e:
        print(f"Error loading home page: {e}")
        return "Error loading home page", 500

# --------------------------------------
# SCRAPE ENDPOINT (future live data)
# --------------------------------------
@app.route("/scrape")
def scrape():
    try:
        # For now, just return the demo fixtures
        return jsonify({"status": "success", "fixtures": fixtures})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --------------------------------------
# START SERVER
# --------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
