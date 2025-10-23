# scraper.py
import asyncio
import time
from playwright.async_api import async_playwright
from database import save_data  # make sure you have a save_data() in database.py

SPORTYBET_URL = "https://www.sportybet.com/ng/virtuals/football"

async def scrape_sportybet_page():
    """Main Playwright scraping logic with smart selector adjustment."""
    print("🎯 Starting SportyBet scraper...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(SPORTYBET_URL, timeout=60000)
            await page.wait_for_timeout(5000)

            # Smart selectors with fallback
            possible_selectors = [
                ".fixture-row",                  # Original layout
                "div[data-testid='fixture']",    # Modern layout
                ".event-card",                   # Alternate layout
                ".match-row"                     # Older layout
            ]

            fixtures = []
            for selector in possible_selectors:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"✅ Using selector: {selector}")
                    for el in elements:
                        try:
                            home_team = await el.query_selector_eval(
                                ".home, .team-home, .home-team",
                                "(el) => el.innerText"
                            )
                            away_team = await el.query_selector_eval(
                                ".away, .team-away, .away-team",
                                "(el) => el.innerText"
                            )
                            over_15 = await el.query_selector_eval(
                                ".over15, .market-over15, [data-outcome='over_1_5']",
                                "(el) => el.innerText"
                            )
                            under_25 = await el.query_selector_eval(
                                ".under25, .market-under25, [data-outcome='under_2_5']",
                                "(el) => el.innerText"
                            )

                            fixtures.append({
                                "home_team": home_team.strip(),
                                "away_team": away_team.strip(),
                                "over_15": over_15.strip(),
                                "under_25": under_25.strip(),
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                            })
                        except Exception as e:
                            print(f"⚠️ Error parsing fixture: {e}")
                    break
            else:
                print("❌ No fixtures found using any selector pattern!")

            await browser.close()

            if fixtures:
                print(f"✅ Scraped {len(fixtures)} fixtures.")
                save_data(fixtures)
            else:
                print("⚠️ No data to save.")
    except Exception as e:
        print(f"🚨 Error during scraping: {e}")

def run_scraper():
    """Wrapper for Render or Flask threading."""
    try:
        asyncio.run(scrape_sportybet_page())
    except RuntimeError:
        # Prevent 'event loop already running' errors
        loop = asyncio.get_event_loop()
        loop.run_until_complete(scrape_sportybet_page())
