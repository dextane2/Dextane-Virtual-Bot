import requests
from bs4 import BeautifulSoup
from database import store_fixture
from datetime import datetime

SPORTY_URL = 'https://www.sportybet.com/ng/m/virtual?from=virtuals-lobby'

def parse_odd_text(node):
    if not node:
        return None
    text = node.get_text(separator=' ').strip()
    # try to extract a float in the text
    import re
    m = re.search(r'(\d+\.\d+)', text)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def fetch_current_fixtures():
    """Fetch fixtures from SportyBet virtual lobby page.
    This function is intentionally defensive: it parses team blocks and nearby market blocks.
    It stores each found fixture into local database via store_fixture().
    Returns list of fixture dicts saved in this run.
    """
    try:
        r = requests.get(SPORTY_URL, timeout=15)
        r.raise_for_status()
        html = r.text
    except Exception as e:
        print('scraper: request error', e)
        return []

    soup = BeautifulSoup(html, 'html.parser')
    fixtures = []

    # find parent rows that look like market-table-row (based on earlier samples)
    rows = soup.select('.market-table-row')
    if not rows:
        # fallback: look for spans with class match-teams
        rows = soup.select('span.match-teams, span.match-teams-and-id-container')

    for row in rows:
        try:
            # find team names
            team_spans = row.select('.participant-text-name')
            if len(team_spans) >= 2:
                home = team_spans[0].get_text(strip=True)
                away = team_spans[1].get_text(strip=True)
            else:
                # fallback: try splitting text content by '-'
                text = row.get_text(separator=' ').strip()
                if '-' in text:
                    parts = [p.strip() for p in text.split('-')]
                    home, away = parts[0], parts[1]
                else:
                    continue

            # attempt to find odds in the same row
            odd_values = row.select('.odd-value')
            odd_home = parse_odd_text(odd_values[0]) if len(odd_values) > 0 else None
            odd_draw = parse_odd_text(odd_values[1]) if len(odd_values) > 1 else None
            odd_away = parse_odd_text(odd_values[2]) if len(odd_values) > 2 else None

            # attempt to find Over/Under 2.5 and Over 1.5 by matching ids or nearby elements
            under25 = None
            over15 = None
            # search by id patterns containing match id if present
            # naive search on page for titles 'Under 2.5' and 'Over 1.5' near this text
            # search sibling market cells
            parent = row
            # look nearby in document for market cells with 'Under 2.5' or 'Over 1.5'
            for candidate in row.find_all_next(class_='market-cell', limit=12):
                title = candidate.get('title') or ''
                title_l = title.lower()
                if 'under 2.5' in title_l or 'un 2.5' in title_l:
                    under25 = parse_odd_text(candidate)
                if 'over 1.5' in title_l or 'ov 1.5' in title_l:
                    over15 = parse_odd_text(candidate)
                if under25 and over15:
                    break

            fixture = {
                'home_team': home,
                'away_team': away,
                'odd_home': odd_home,
                'odd_draw': odd_draw,
                'odd_away': odd_away,
                'under_2_5': under25,
                'over_1_5': over15,
                'timestamp': datetime.utcnow().isoformat()
            }
            # store to DB
            store_fixture(fixture)
            fixtures.append(fixture)
        except Exception as ex:
            # skip malformed rows
            print('scraper row parse error', ex)
            continue

    return fixtures
