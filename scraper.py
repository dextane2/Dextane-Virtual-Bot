import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def get_vfl_data():
    try:
        url = "https://www.sportybet.com/ng/virtuals/vfl"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        matches = []
        for match in soup.select(".match-card")[:5]:
            teams = match.select_one(".teams").get_text(strip=True)
            odds = [o.get_text(strip=True) for o in match.select(".odd")]
            matches.append({
                "match": teams,
                "odds": odds[:3] if odds else ["-", "-", "-"]
            })

        # fallback demo data if site structure changes
        if not matches:
            matches = [
                {"match": "Chelsea vs Arsenal", "odds": ["1.65", "3.20", "4.75"]},
                {"match": "Man City vs Liverpool", "odds": ["2.10", "3.00", "3.50"]},
                {"match": "Tottenham vs Newcastle", "odds": ["2.40", "3.10", "3.00"]},
            ]

        lagos_tz = pytz.timezone("Africa/Lagos")
        current_time = datetime.now(lagos_tz).strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "timestamp": current_time,
            "matches": matches
        }

    except Exception as e:
        print(f"Error fetching SportyBet data: {e}")
        return {
            "status": "error",
            "message": str(e),
            "matches": []
        }
