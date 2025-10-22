import sqlite3

DB_PATH = "data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def store_fixture(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fixtures (home_team, away_team, odd_home, odd_draw, odd_away, under_2_5, over_1_5)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("home_team"),
        data.get("away_team"),
        data.get("odd_home"),
        data.get("odd_draw"),
        data.get("odd_away"),
        data.get("under_2_5"),
        data.get("over_1_5")
    ))
    conn.commit()
    conn.close()

def get_all_data(limit=100):
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT id, home_team, away_team, odd_home, odd_draw, odd_away, under_2_5, over_1_5, timestamp
        FROM fixtures ORDER BY id DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "home_team": row[1],
            "away_team": row[2],
            "odd_home": row[3],
            "odd_draw": row[4],
            "odd_away": row[5],
            "under_2_5": row[6],
            "over_1_5": row[7],
            "timestamp": row[8],
        }
        for row in rows
    ]
