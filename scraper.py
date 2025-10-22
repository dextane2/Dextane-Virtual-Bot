import asyncio
import sqlite3
from playwright.async_api import async_playwright
from datetime import datetime

DB_PATH = "matches.db"

async def fetch_data():
    print("🔍 Fetching fresh data...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            home_team TEXT,
            away_team TEXT,
            over_1_5_odds REAL,
            under_2_5_odds REAL,
            prediction TEXT
        )
    """)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 🌐 Replace with your actual virtual football URL
        url = "https://www.sportybet.com/ng/virtuals"
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(5000)

        # Example selectors — adjust as needed
        games = await page.query_selector_all(".match-card, .fixture-row")
        for game in games:
            try:
                home_team = await game.query_selector_eval(".home-team, .home", "el => el.innerText")
                away_team = await game.query_selector_eval(".away-team, .away", "el => el.innerText")

                over15 = await game.query_selector_eval(".over15, .market-O15", "el => el.innerText").replace(" ", "")
                under25 = await game.query_selector_eval(".under25, .market-U25", "el => el.innerText").replace(" ", "")

                over15 = float(over15) if over15.replace('.', '', 1).isdigit() else None
                under25 = float(under25) if under25.replace('.', '', 1).isdigit() else None

                prediction = None
                if over15 and under25:
                    prediction = "Over 1.5" if over15 < under25 else "Under 2.5"

                cursor.execute("""
                    INSERT INTO matches (timestamp, home_team, away_team, over_1_5_odds, under_2_5_odds, prediction)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    home_team, away_team, over15, under25, prediction
                ))
            except Exception as e:
                print("⚠️ Error parsing a match:", e)
                continue

        await browser.close()
        conn.commit()
        conn.close()
        print("✅ Data saved successfully.")

async def main():
    while True:
        await fetch_data()
        print("⏳ Waiting 2 minutes before next update...")
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
