import asyncio
from playwright.async_api import async_playwright
from database import store_fixture
from datetime import datetime

SPORTYBET_URL = "https://www.sportybet.com/ng/m/virtual?from=virtuals-lobby"

async def smart_scrape_data():
    print(f"🚀 [{datetime.now()}] Starting smart scrape...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(SPORTYBET_URL, timeout=60000)
            print("✅ Page loaded successfully")

            # Wait for matches container (varies by site version)
            await page.wait_for_selector("div[class*='match'], div[class*='fixture'], span[class*='match-teams']", timeout=30000)

            # Get all visible match sections
            html = await page.content()
            print(f"📄 Page content length: {len(html)}")

            # Match blocks (covering different layouts)
            matches = await page.query_selector_all("div[class*='match'], div[class*='fixture'], li[class*='match'], span[class*='match-teams']")
            print(f"🧩 Found {len(matches)} match containers")

            for match in matches:
                try:
                    # Try multiple patterns for team names
                    home_team = await try_extract(match, ["span.team-name--strong", ".home", ".homeTeamName", ".participant-text-name.team-name--strong"])
                    away_team = await try_extract(match, ["span.team-name:not(.team-name--strong)", ".away", ".awayTeamName", ".participant-text-name:not(.team-name--strong)"])

                    # Try multiple patterns for odds
                    over_1_5 = await try_extract(match, ["div[title*='Over 1.5']", "div:has-text('OV 1.5')", ".over1_5"])
                    under_2_5 = await try_extract(match, ["div[title*='Under 2.5']", "div:has-text('UN 2.5')", ".under2_5"])

                    # Validate and store only if both teams found
                    if home_team and away_team:
                        print(f"➡️ {home_team} vs {away_team} | O1.5: {over_1_5 or 'N/A'} | U2.5: {under_2_5 or 'N/A'}")
                        store_fixture(home_team, away_team, over_1_5 or "N/A", under_2_5 or "N/A")
                    else:
                        print("⚠️ Could not extract team names; skipping.")

                except Exception as e:
                    print(f"❌ Error parsing match: {e}")

            await browser.close()
            print("✅ Scraping completed and browser closed!")

        except Exception as e:
            print(f"💥 Scraper failed: {e}")
            await browser.close()


async def try_extract(element, selectors):
    """Try multiple CSS selectors until one succeeds."""
    for selector in selectors:
        try:
            el = await element.query_selector(selector)
            if el:
                text = (await el.inner_text()).strip()
                if text:
                    return text
        except:
            continue
    return None


def run_scraper():
    asyncio.run(smart_scrape_data())
