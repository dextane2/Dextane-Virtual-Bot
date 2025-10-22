# scraper.py
import time
import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright

DB_PATH = "matches.db"
SPORTY_URL = "https://www.sportybet.com/ng/m/virtual?from=virtuals-lobby"

def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
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
    conn.commit()
    conn.close()

def parse_float(s):
    try:
        if s is None:
            return None
        s = s.strip().replace(',', '.')
        # remove non numeric suffix/prefix
        import re
        m = re.search(r'(\d+(?:[\\.,]\\d+)?)', s)
        if m:
            return float(m.group(1).replace(',', '.'))
    except:
        pass
    return None

def store(match):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO matches (timestamp, home_team, away_team, over_1_5_odds, under_2_5_odds, prediction)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        match.get("home_team"),
        match.get("away_team"),
        match.get("over1_5"),
        match.get("under2_5"),
        match.get("prediction")
    ))
    conn.commit()
    conn.close()

def scrape_once():
    print("🔍 Starting scrape:", datetime.utcnow().isoformat())
    found = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        try:
            page.goto(SPORTY_URL, timeout=45000)
            # small wait to let the page render JS
            page.wait_for_timeout(4000)
        except Exception as e:
            print("⚠️ Page load error:", e)
            browser.close()
            return 0

        # Try common selectors we observed earlier
        rows = page.query_selector_all(".market-table-row, .match-card, .match-row")
        if not rows:
            # fallback to spans with match-teams
            rows = page.query_selector_all("span.match-teams, span.match-teams-and-id-container")

        for r in rows:
            try:
                # get team names
                team_spans = r.query_selector_all(".participant-text-name, .team-name, .participant-name")
                if len(team_spans) >= 2:
                    home = team_spans[0].inner_text().strip()
                    away = team_spans[1].inner_text().strip()
                else:
                    # fallback: text split
                    txt = r.inner_text().strip()
                    if "-" in txt:
                        parts = [p.strip() for p in txt.split("-", 1)]
                        home, away = parts[0], parts[1]
                    else:
                        continue

                # find market cells near this row for Over 1.5 / Under 2.5
                over1_5 = None
                under2_5 = None

                # search next few market cells for titles/text
                candidates = r.query_selector_all("div.market-cell, .odd, .market-cell__content")
                # also search next siblings in DOM to increase chance
                if not candidates:
                    candidates = r.query_selector_all("*")

                for c in candidates:
                    title = ""
                    try:
                        title = c.get_attribute("title") or c.inner_text() or ""
                    except:
                        try:
                            title = c.inner_text() or ""
                        except:
                            title = ""
                    t = title.lower()
                    if "over 1.5" in t or "ov 1.5" in t or "o 1.5" in t or "over1.5" in t:
                        over1_5 = parse_float(title)
                    if "under 2.5" in t or "un 2.5" in t or "u 2.5" in t or "under2.5" in t:
                        under2_5 = parse_float(title)
                    # try to parse odd-value sibling elements
                    if ("over 1.5" in t or "under 2.5" in t) and (over1_5 or under2_5):
                        # keep going, we may already have parsed numbers
                        pass

                # secondary strategy: find odd-value spans inside row
                try:
                    odd_vals = r.query_selector_all(".odd-value, .grid .odd-value, span.odd-value")
                    if odd_vals and len(odd_vals) >= 1:
                        # sometimes Over/Under not present in same element; we'll not rely on this fully
                        pass
                except:
                    pass

                # compute a simple rule-based prediction if we have both odds
                prediction = None
                if over1_5 is not None and under2_5 is not None:
                    # simple rule: prefer the smaller odd as likely market? (you can change later)
                    if over1_5 < under2_5:
                        prediction = "Over 1.5"
                    else:
                        prediction = "Under 2.5"

                match = {
                    "home_team": home,
                    "away_team": away,
                    "over1_5": over1_5,
                    "under2_5": under2_5,
                    "prediction": prediction
                }
                store(match)
                found += 1
            except Exception as e:
                # robustly ignore parse errors per row
                # print("row parse error:", e)
                continue

        browser.close()
    print(f"🔁 Scrape done — items saved: {found}")
    return found

def main_loop(interval_seconds=120):
    ensure_db()
    while True:
        try:
            scrape_once()
        except Exception as e:
            print("❌ Scraper loop error:", e)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main_loop(interval_seconds=120)
