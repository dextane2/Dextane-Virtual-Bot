# scraper.py
import time
from playwright.sync_api import sync_playwright
from database import store_fixture

URL = "https://www.sportybet.com/ng/m/virtual?from=virtuals-lobby"

def fetch_fixtures_with_browser():
    """
    Fetches current virtual fixtures and odds directly from SportyBet
    using Playwright (headless browser).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        # Wait for team names to appear
        try:
            page.wait_for_selector("span.match-teams", timeout=15000)
        except:
            print("❌ Could not find any matches. The page might have changed.")
            browser.close()
            return []

        matches = page.query_selector_all("span.match-teams")
        all_data = []

        for match in matches:
            text = match.inner_text().strip()
            if "-" not in text:
                continue

            home, away = [t.strip() for t in text.split("-", 1)]
            parent = match.evaluate_handle("node => node.closest('.match') || node.parentElement")

            # Try to locate odds nearby
            try:
                odds_cells = parent.query_selector_all("span.odds")
                if len(odds_cells) >= 3:
                    odd_home = odds_cells[0].inner_text().strip()
                    odd_draw = odds_cells[1].inner_text().strip()
                    odd_away = odds_cells[2].inner_text().strip()
                else:
                    odd_home = odd_draw = odd_away = None
            except:
                odd_home = odd_draw = odd_away = None

            # Example extra odds (optional)
            under = over = None
            try:
                under_elem = parent.query_selector("span:has-text('Under 2.5')")
                over_elem = parent.query_selector("span:has-text('Over 1.5')")
                if under_elem:
                    under = under_elem.inner_text().strip()
                if over_elem:
                    over = over_elem.inner_text().strip()
            except:
                pass

            fixture = {
                "home_team": home,
                "away_team": away,
                "odd_home": odd_home,
                "odd_draw": odd_draw,
                "odd_away": odd_away,
                "under_2_5": under,
                "over_1_5": over,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            print("✅ Fixture found:", fixture)
            store_fixture(fixture)
            all_data.append(fixture)

        browser.close()
        return all_data


if __name__ == "__main__":
    print("🕵️ Fetching current fixtures from SportyBet virtuals...")
    data = fetch_fixtures_with_browser()
    print(f"✅ {len(data)} fixtures saved.")
