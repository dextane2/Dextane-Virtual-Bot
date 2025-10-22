from flask import Flask, jsonify
import threading
import time
import requests
from bs4 import BeautifulSoup
from database import store_fixture, get_all_data

app = Flask(__name__)

def scrape_sportybet_fixtures():
    """
    Scrapes SportyBet virtual football fixtures and generates predictions.
    """
    url = "https://www.sportybet.com/ng/virtuals"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract match elements (SportyBet changes layout often, so this may need adjustment)
        matches = soup.find_all("div", class_="fixture") or soup.find_all("div", class_="match")
        if not matches:
            print("⚠️ No fixtures found — layout may have changed.")
            return

        for match in matches[:5]:  # Limit to 5 for demo
            teams = match.get_text(separator="|").split("|")
            if len(teams) >= 2:
                home_team = teams[0].strip()
                away_team = teams[1].strip()

                # Simple demo prediction logic (can be upgraded later)
                prediction = "Over 1.5 goals" if len(home_team) % 2 == 0 else "Under 2.5 goals"

                fixture = {
                    "home_team": home_team,
                    "away_team": away_team,
                    "prediction": prediction,
                    "confidence": f"{70 + len(home_team) % 10}%",
                }

                store_fixture(fixture)
                print(f"✅ Prediction generated: {fixture}")

    except Exception as e:
        print(f"❌ Error scraping SportyBet: {e}")


def monitor_sportybet():
    """
    Background monitoring loop.
    """
    while True:
        print("🔍 Checking SportyBet virtual games...")
        scrape_sportybet_fixtures()
        time.sleep(60)  # Every minute


@app.route('/')
def home():
    return "🟢 Dextane Virtual Bot is live and monitoring SportyBet virtual football!"


@app.route('/api/data')
def api_data():
    """
    Returns all stored predictions.
    """
    return jsonify(get_all_data())


def run_background():
    thread = threading.Thread(target=monitor_sportybet)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    run_background()
    app.run(host='0.0.0.0', port=10000)
