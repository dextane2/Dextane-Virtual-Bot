from flask import Flask, render_template_string, jsonify
from scraper import get_vfl_data
from datetime import datetime, timedelta
import pytz
import random

app = Flask(__name__)

# Lagos timezone
lagos_tz = pytz.timezone("Africa/Lagos")

# Demo prediction data generator
def generate_predictions():
    over_15 = random.sample([
        "Chelsea vs Arsenal", "Man City vs Liverpool", "Tottenham vs Newcastle",
        "Everton vs Aston Villa", "Leeds vs Brighton", "Napoli vs Roma"
    ], 3)

    under_25 = random.sample([
        "Juventus vs Inter Milan", "Atletico vs Real Betis", "PSG vs Lyon",
        "Benfica vs Porto", "Ajax vs Feyenoord"
    ], 2)

    return over_15, under_25


@app.route('/')
def home():
    try:
        data = get_vfl_data()
        over_15, under_25 = generate_predictions()

        current_time = datetime.now(lagos_tz)
        next_round_time = current_time + timedelta(minutes=2)
        countdown_seconds = int((next_round_time - current_time).total_seconds())

        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dextane Virtual Bot</title>
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #0a0f29, #001f4d);
                    color: white;
                    text-align: center;
                    padding: 0;
                    margin: 0;
                }
                header {
                    background: linear-gradient(90deg, #001f4d, #004080);
                    padding: 15px 20px;
                    font-size: 1.8rem;
                    font-weight: bold;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.5);
                    position: relative;
                }
                .menu-btn {
                    position: absolute;
                    right: 20px;
                    top: 18px;
                    cursor: pointer;
                    font-size: 1.5rem;
                    background: none;
                    border: none;
                    color: white;
                }
                .menu-dropdown {
                    display: none;
                    position: absolute;
                    right: 20px;
                    top: 60px;
                    background: #001a33;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.4);
                    border-radius: 10px;
                    overflow: hidden;
                    z-index: 10;
                }
                .menu-dropdown a {
                    display: block;
                    padding: 10px 15px;
                    color: white;
                    text-decoration: none;
                    transition: background 0.3s;
                }
                .menu-dropdown a:hover {
                    background: #004080;
                }
                .card-container {
                    display: flex;
                    overflow-x: auto;
                    scroll-snap-type: x mandatory;
                    padding: 20px;
                    gap: 20px;
                }
                .card {
                    flex: 0 0 90%;
                    background: rgba(255,255,255,0.08);
                    backdrop-filter: blur(8px);
                    border-radius: 15px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.4);
                    padding: 20px;
                    scroll-snap-align: center;
                    transition: transform 0.3s;
                }
                .card:hover {
                    transform: scale(1.02);
                }
                h2 {
                    color: #4da6ff;
                    margin-bottom: 10px;
                }
                ul {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                li {
                    background: rgba(255,255,255,0.05);
                    margin: 8px 0;
                    padding: 10px;
                    border-radius: 8px;
                    box-shadow: inset 0 0 5px rgba(0,0,0,0.3);
                }
                .countdown {
                    margin-top: 10px;
                    font-size: 1.2rem;
                    color: #ffcc00;
                }
                footer {
                    margin-top: 20px;
                    font-size: 0.9rem;
                    color: #aaa;
                }
            </style>
        </head>
        <body>
            <header>
                Dextane Virtual Bot
                <button class="menu-btn" onclick="toggleMenu()">☰</button>
                <div id="menu" class="menu-dropdown">
                    <a href="#" onclick="refreshData()">🔄 Scrape Now</a>
                </div>
            </header>

            <div class="card-container">
                <div class="card">
                    <h2>Over 1.5 Predictions</h2>
                    <ul>
                        {% for match in over_15 %}
                            <li>{{ match }}</li>
                        {% endfor %}
                    </ul>
                </div>

                <div class="card">
                    <h2>Under 2.5 Predictions</h2>
                    <ul>
                        {% for match in under_25 %}
                            <li>{{ match }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <div class="countdown">Next round in: <span id="timer">02:00</span></div>

            <footer>Last updated: {{ data.timestamp }} (Lagos)</footer>

            <script>
                let timeLeft = {{ countdown_seconds }};
                function updateTimer() {
                    let minutes = Math.floor(timeLeft / 60);
                    let seconds = timeLeft % 60;
                    document.getElementById('timer').textContent =
                        String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
                    if (timeLeft > 0) timeLeft--;
                }
                setInterval(updateTimer, 1000);

                function toggleMenu() {
                    const menu = document.getElementById('menu');
                    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
                }

                function refreshData() {
                    fetch('/refresh').then(() => location.reload());
                }
            </script>
        </body>
        </html>
        """
        return render_template_string(html, data=data, over_15=over_15, under_25=under_25, countdown_seconds=countdown_seconds)

    except Exception as e:
        return f"<h1>Error loading dashboard: {e}</h1>"

@app.route('/refresh')
def refresh():
    return jsonify(get_vfl_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
