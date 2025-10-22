# app.py
from flask import Flask, render_template, g
import sqlite3, os

DB_PATH = "matches.db"
app = Flask(__name__)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    # ensure DB file exists
    if not os.path.exists(DB_PATH):
        return "<p>No data yet. The scraper worker will populate matches.db in a couple of minutes.</p>"
    cur = get_db().cursor()
    cur.execute("SELECT id, timestamp, home_team, away_team, over_1_5_odds, under_2_5_odds, prediction FROM matches ORDER BY id DESC LIMIT 200")
    rows = cur.fetchall()
    html = "<h1>Dextane Virtual Bot — Recent Predictions</h1>"
    html += "<table border='1' cellpadding='6' cellspacing='0'><tr><th>#</th><th>Time (UTC)</th><th>Home</th><th>Away</th><th>Over 1.5</th><th>Under 2.5</th><th>Prediction</th></tr>"
    for r in rows:
        html += f"<tr><td>{r['id']}</td><td>{r['timestamp']}</td><td>{r['home_team']}</td><td>{r['away_team']}</td><td>{r['over_1_5_odds']}</td><td>{r['under_2_5_odds']}</td><td>{r['prediction']}</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    # simple dev server; Render will use gunicorn
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
