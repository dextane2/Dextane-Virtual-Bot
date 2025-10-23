# database.py
import sqlite3

DB_FILE = "fixtures.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team TEXT,
            away_team TEXT,
            over_15 TEXT,
            under_25 TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_data(records):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for record in records:
        c.execute("""
            INSERT INTO fixtures (home_team, away_team, over_15, under_25, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            record['home_team'],
            record['away_team'],
            record['over_15'],
            record['under_25'],
            record['timestamp']
        ))
    conn.commit()
    conn.close()

def get_all_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT home_team, away_team, over_15, under_25, timestamp FROM fixtures ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return rows

# Initialize database on import
init_db()
