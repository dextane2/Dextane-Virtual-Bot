# app.py
from flask import Flask, render_template_string, jsonify
from threading import Thread
from scraper import run_scraper
from database import get_all_data
import datetime

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dextane Virtual Bot</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #101820; color: #fff; text-align: center; margin: 0; padding: 20px; }
        table { width: 90%; margin: 20px auto; border-collapse: collapse; }
        th, td { border: 1px solid #444; padding: 10px; text-align: center; }
        th { background-color: #00539C; }
        tr:nth-child(even) { background-color: #1a1a1a; }
        button { background-color: #00539C; color: white; border: none; padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 8px; }
        button:hover { background-color: #0074D9; }
        .header { font-size: 24px; margin-top: 10px; color: #00d9ff; }
    </style>
</head>
<body>
    <div class="header">⚽ Dextane Virtual Bot</div>
    <p>Last updated: {{ last_updated }}</p>
    <form action="/scrape" method="get">
        <button type="submit">🧠 Scrape Now</button>
    </form>

    <table>
        <tr>
            <th>Home Team</th>
            <th>Away Team</th>
            <th>Over 1.5</th>
            <th>Under 2.5</th>
            <th>Timestamp</th>
        </tr>
        {% if fixtures %}
            {% for fixture in fixtures %}
            <tr>
                <td>{{ fixture[0] }}</td>
                <td>{{ fixture[1] }}</td>
                <td>{{ fixture[2] }}</td>
                <td>{{ fixture[3] }}</td>
                <td>{{ fixture[4] }}</td>
            </tr>
            {% endfor %}
        {% else %}
            <tr><td colspan="5">No records yet. Click "Scrape Now" to begin.</td></tr>
        {% endif %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        fixtures = get_all_data()
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return render_template_string(HTML_TEMPLATE, fixtures=fixtures, last_updated=now)
    except Exception as e:
        print(f"Error loading home page: {e}")
        return "An error occurred while loading the page.", 500


@app.route("/scrape")
def scrape():
    try:
        thread = Thread(target=run_scraper)
        thread.start()
        return jsonify({"message": "Scraper started.", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Error: {e}", "status": "failed"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
