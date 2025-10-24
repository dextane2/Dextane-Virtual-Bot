import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

lagos_tz = pytz.timezone("Africa/Lagos")

def get_vfl_data():
    """
    Smart scraper for SportyBet Scheduled Virtual Football (VFL)
    """
    try:
        url = "https://www.sportybet.com/ng/sport/football/scheduled-virtuals"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        fixtures = []
        # SportyBet sometimes changes structure, so we check multiple selector patterns
        possible_selectors = [
            "div.fixture-row",
            "div.Market__event",
            "div.EventRow",
            "tr.fixture",
        ]

        for selector in possible_selectors:
            rows = soup.select(selector)
            if rows:
                for row in rows[:10]:  # limit to 10 fixtures for speed
                    text = row.get_text(separator=" ").strip()
                    if not text:
                        continue
                    parts = text.split()
                    if len(parts) < 3:
                        continue
                    fixture = " ".join(parts[:4])
                    fixtures.append(fixture)
                break  # stop at the first valid pattern

        if not fixtures:
            fixtures = ["Unable to fetch fixtures — layout may have changed"]

        return {
            "fixtures": fixtures,
            "timestamp": datetime.now(lagos_tz).strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {
            "fixtures": [f"Error fetching SportyBet data: {e}"],
            "timestamp": datetime.now(lagos_tz).strftime("%Y-%m-%d %H:%M:%S")
        }
