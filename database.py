import sqlite3, os
DB_NAME = 'dextane_data.db'

def connect():
    os.makedirs(os.path.dirname(DB_NAME) or '.', exist_ok=True)
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

def setup():
    conn = connect()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS fixtures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_team TEXT,
        away_team TEXT,
        odd_home REAL,
        odd_draw REAL,
        odd_away REAL,
        under_2_5 REAL,
        over_1_5 REAL,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def store_fixture(f):
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO fixtures (home_team, away_team, odd_home, odd_draw, odd_away, under_2_5, over_1_5, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (f.get('home_team'), f.get('away_team'), f.get('odd_home'), f.get('odd_draw'), f.get('odd_away'), f.get('under_2_5'), f.get('over_1_5'), f.get('timestamp')))
    conn.commit()
    conn.close()

def get_all_data(limit=200):
    conn = connect()
    cur = conn.cursor()
    rows = cur.execute('SELECT id, home_team, away_team, odd_home, odd_draw, odd_away, under_2_5, over_1_5, timestamp FROM fixtures ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [dict(zip(['id','home_team','away_team','odd_home','odd_draw','odd_away','under_2_5','over_1_5','timestamp'], r)) for r in rows]
