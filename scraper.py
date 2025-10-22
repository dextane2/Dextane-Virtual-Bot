import asyncio
from playwright.async_api import async_playwright
import re
import time
from database import store_fixture


async def scrape_sportybet_page(page):
    """Scrape SportyBet virtual football fixtures with fallback selectors."""
    data = []

    # Try multiple possible selector patterns to adapt to layout changes
    possible_row_selectors = [
        "div[class*='match-row']",
        "div[class*='fixture-row']",
        "div[class*='event-row']",
        "div[data-testid*='event-row']",
        "div[data-test*='fixture']",
    ]

    for selector in possible_row_selectors:
        rows = await page.query_selector_all(selector)
        if rows:
            print(f"[✅] Using selector: {selector} ({len(rows)} matches found)")
            break
    else:
        print("[❌] No valid row selector found.")
        return []

    for row in rows:
        try:
            text = await row.inner_text()
            # Try to extract meaningful parts using regex
            parts = re.split(r"\s{2,}", text.strip())

            # Attempt to find Over/Under odds automatically
            over_1_5 = None
            under_2_5 = None

            odds = re.findall(r"\d+\.\d+", text)
            if len(odds) >= 2:
                over_1_5 = odds[0]
                under_2_5 = odds[1]

            # Extract team names intelligently
            teams = re.findall(r"[A-Za-z\s]+vs[A-Za-z\s]+", text)
            if teams:
                home_team, away_team = [t.strip() for t in teams[0].split("vs")]
            else:
                # fallback: split the parts if "vs" is missing
                if len(parts) >= 2:
                    home_team = parts[0].strip()
                    away_team = parts[1].strip()
                else:
                    continue

            data.append({
                "home_team": home_team,
                "away_team": away_team,
                "over_1_5": over_1_5,
                "under_2_5": under_2_5,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception as e:
            print(f"Error parsing row: {e}")
            continue

    return data


async def run_async_scraper():
    """Run the Playwright scraper asynchronously."""
    print("[🏃‍♂️] Launching browser for scraping...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "https://www.sportybet.com/ng/virtuals/football"
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(7000)  # wait for data to load

        scraped_data = await scrape_sportybet_page(page)
        await browser.close()

        if scraped_data:
            for fixture in scraped_data:
                store_fixture(
                    fixture["home_team"],
                    fixture["away_team"],
                    fixture["over_1_5"],
                    fixture["under_2_5"],
                    fixture["timestamp"],
                )
            print(f"[✅] Saved {len(scraped_data)} fixtures to database.")
        else:
            print("[⚠️] No fixtures scraped — check if SportyBet layout changed.")


def run_scraper():
    """Wrapper for Render / Flask threading."""
    asyncio.run(run_async_scraper())
