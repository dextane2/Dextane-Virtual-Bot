from flask import Flask, render_template_string, jsonify
from datetime import datetime
import random
import pytz

app = Flask(__name__)

# -----------------------------
# Generate Demo Predictions
# -----------------------------
def generate_predictions():
    teams = [
        "Arsenal vs Chelsea", "Liverpool vs Man City", "PSG vs Lyon",
        "Bayern vs Dortmund", "Juventus vs Milan", "Ajax vs Feyenoord",
        "Barcelona vs Real Madrid", "Inter vs Napoli", "Porto vs Benfica",
        "Atletico vs Sevilla"
    ]
    random.shuffle(teams)
    over15 = random.sample(teams, 3)
    under25 = random.sample([t for t in teams if t not in over15], 2)
    return over15, under25


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    lagos = pytz.timezone("Africa/Lagos")
    now = datetime.now(lagos)
    over15, under25 = generate_predictions()
    return render_template_string(template, now=now, over15=over15, under25=under25)


@app.route("/api/predictions")
def api_predictions():
    lagos = pytz.timezone("Africa/Lagos")
    over15, under25 = generate_predictions()
    return jsonify({
        "over15": over15,
        "under25": under25,
        "timestamp": datetime.now(lagos).strftime("%Y-%m-%d %H:%M:%S")
    })


# -----------------------------
# Template
# -----------------------------
template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dextane Virtual Bot</title>
<style>
body {
  background-color: #0f172a;
  color: #e2e8f0;
  font-family: 'Poppins', sans-serif;
  margin: 0;
  padding: 0;
  text-align: center;
}
header {
  background-color: #1e293b;
  color: #38bdf8;
  padding: 20px;
  font-size: 22px;
  font-weight: bold;
  position: relative;
}
.menu {
  position: absolute;
  right: 20px;
  top: 60px;
  background: #1e293b;
  border-radius: 8px;
  display: none;
  flex-direction: column;
  min-width: 150px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.menu button {
  background: none;
  color: #e2e8f0;
  border: none;
  padding: 10px;
  cursor: pointer;
  text-align: left;
}
.menu button:hover {
  background: #334155;
}
.menu-toggle {
  position: absolute;
  right: 20px;
  top: 20px;
  font-size: 20px;
  background: none;
  color: #38bdf8;
  border: none;
  cursor: pointer;
}
.container {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  margin-top: 80px;
}
.card {
  background: #1e293b;
  border-radius: 16px;
  flex: 0 0 80%;
  margin: 0 10px;
  padding: 20px;
  scroll-snap-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.card h2 {
  color: #22d3ee;
  margin-bottom: 15px;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.list li {
  background: #0f172a;
  margin: 8px 0;
  padding: 10px;
  border-radius: 8px;
  color: #e2e8f0;
}
.time {
  margin-top: 20px;
  color: #94a3b8;
  font-size: 14px;
}
footer {
  margin-top: 30px;
  font-size: 13px;
  color: #64748b;
}
</style>
</head>
<body>

<header>
  🧠 Dextane Virtual Bot
  <button class="menu-toggle" onclick="toggleMenu()">☰</button>
  <div class="menu" id="menu">
    <button onclick="scrapeNow()">🔄 Scrape Now</button>
    <button onclick="window.location.reload()">🔃 Refresh</button>
  </div>
</header>

<div class="container">
  <div class="card" id="over15Card">
    <h2>Over 1.5 Predictions</h2>
    <ul class="list" id="over15List">
      {% for match in over15 %}
      <li>{{ match }}</li>
      {% endfor %}
    </ul>
  </div>

  <div class="card" id="under25Card">
    <h2>Under 2.5 Predictions</h2>
    <ul class="list" id="under25List">
      {% for match in under25 %}
      <li>{{ match }}</li>
      {% endfor %}
    </ul>
  </div>
</div>

<div class="time">
  🕒 Last updated: <span id="timestamp">{{ now.strftime('%Y-%m-%d %H:%M:%S') }}</span> (Lagos Time)
</div>

<footer>
  ⏱️ Next update in <span id="countdown">120</span> seconds
</footer>

<script>
function toggleMenu() {
  const menu = document.getElementById('menu');
  menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
}

function scrapeNow() {
  fetch('/api/predictions').then(r => r.json()).then(updateDashboard);
}

function updateDashboard(data) {
  const over15List = document.getElementById('over15List');
  const under25List = document.getElementById('under25List');
  const timestamp = document.getElementById('timestamp');

  over15List.innerHTML = data.over15.map(m => `<li>${m}</li>`).join('');
  under25List.innerHTML = data.under25.map(m => `<li>${m}</li>`).join('');
  timestamp.textContent = data.timestamp;
}

let countdown = 120;
setInterval(() => {
  countdown--;
  document.getElementById("countdown").textContent = countdown;
  if (countdown <= 0) {
    countdown = 120;
    fetch('/api/predictions').then(r => r.json()).then(updateDashboard);
  }
}, 1000);
</script>

</body>
</html>
"""

# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
