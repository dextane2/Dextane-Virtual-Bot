from flask import Flask, render_template
from datetime import datetime
import pytz
import random

app = Flask(__name__)

# Simulated predictions (random demo)
def get_predictions():
    teams = [
        ("Chelsea", "Arsenal"),
        ("Man City", "Liverpool"),
        ("Tottenham", "Newcastle"),
        ("Everton", "Aston Villa"),
        ("Leeds", "West Ham"),
        ("Brighton", "Brentford"),
    ]
    over15 = random.sample(teams, 3)
    under25 = random.sample(teams, 2)
    return over15, under25

@app.route('/')
def home():
    # Lagos timezone
    lagos_tz = pytz.timezone('Africa/Lagos')
    lagos_time = datetime.now(lagos_tz).strftime('%Y-%m-%d %H:%M:%S')

    over15, under25 = get_predictions()

    return render_template(
        'index.html',
        lagos_time=lagos_time,
        over15=over15,
        under25=under25
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
