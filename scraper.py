import asyncio
from playwright.async_api import async_playwright
from database import store_fixture
from bs4 import BeautifulSoup
import datetime

SPORTYBET_URL = "https://www.sportybet.com/ng/m/virtual?from=virtuals-lobby"

async def scrape_once():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(SPORTYBET_URL, wait_until="networkidle")

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        fixtures = []

        for match in soup.select(".match-row"):
            teams = match.select_one(".match-teams")
            odds = match.select(".odd-value")

            if not teams or len(odds) < 2:
                continue

            home_team = teams.select_one(".team-name--strong").text.strip()
            away_team = teams.select(".team-name")[1].text.strip() if len(teams.select(".team-name")) > 1 else ""
            under_25 = None
            over_15 = None

            for odd in match.select(".market-cell"):
                title = odd.get("title", "").lower()
                value = odd.select_one(".odd-value").text.strip() if odd.select_one(".odd-value") else None

                if "under 2.5" in title:
                    under_25 = value
                elif "over 1.5" in title:
                    over_15 = value

            if home_team and away_team:
                fixture = {
                    "home_team": home_team,
                    "away_team": away_team,
                    "under_25": under_25,
                    "over_15": over_15,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                fixtures.append(fixture)
                store_fixture(fixture)

        await browser.close()
        return fixtures

def scrape_sportybet():
    asyncio.run(scrape_once())
