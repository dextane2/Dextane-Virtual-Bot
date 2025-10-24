from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

teams = [
    "LIV vs BHA", "ARS vs CHE", "MCI vs MUN", "NEW vs WHU", "TOT vs AVL",
    "LEI vs LEE", "SOU vs BUR", "FUL vs BRE", "CRY vs WOL", "BOU vs EVE"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_predictions")
def get_predictions():
    over15 = random.sample(teams, 5)
    under25 = random.sample(teams, 5)
    data = {
        "over15": [{"match": t, "prediction": "Over 1.5"} for t in over15],
        "under25": [{"match": t, "prediction": "Under 2.5"} for t in under25],
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
