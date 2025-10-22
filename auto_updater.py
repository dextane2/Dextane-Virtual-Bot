import threading, time
from scraper import fetch_current_fixtures

def background_updater(interval_minutes=2):
    def run():
        while True:
            try:
                print('[AUTO-UPDATE] fetching fixtures...')
                fetch_current_fixtures()
            except Exception as e:
                print('[AUTO-UPDATE] error', e)
            time.sleep(interval_minutes * 60)
    t = threading.Thread(target=run, daemon=True)
    t.start()
