from flask import Flask, render_template_string, jsonify
from scraper import get_vfl_data
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
lagos_tz = pytz.timezone("Africa/Lagos")

@app.route('/')
def home():
    try:
        data = get_vfl_data()
        fixtures = data.get("fixtures", [])

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
                    background: linear-gradient(135deg, #001a33, #004080);
                    color: white;
                    text-align: center;
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
                .card {
                    width: 80%;
                    margin: 20px auto;
                    background: rgba(255,255,255,0.08);
                    backdrop-filter: blur(8px);
                    border-radius: 15px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.4);
                    padding: 20px;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    background: rgba(255,255,255,0.05);
                    margin: 8px 0;
                    padding: 10px;
                    border-radius: 8px;
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
                Dextane Virtual Bot ⚽
                <button class="menu-btn" onclick="toggleMenu()">☰</button>
                <div id="menu" class="menu-dropdown">
                    <a href="#" onclick="refreshData()">🔄 Scrape Now</a>
                </div>
            </header>

            <div class="card">
                <h2>SportyBet VFL Fixtures</h2>
                <ul>
                    {% for fix in fixtures %}
                        <li>{{ fix }}</li>
                    {% endfor %}
                </ul>
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
        return render_template_string(html, data=data, fixtures=fixtures, countdown_seconds=countdown_seconds)
    except Exception as e:
        return f"<h1>Error loading dashboard: {e}</h1>"

@app.route('/refresh')
def refresh():
    return jsonify(get_vfl_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
