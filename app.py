from flask import Flask, render_template, jsonify
from scraper import fetch_current_fixtures
from database import get_all_data, setup as db_setup
from auto_updater import background_updater
import os

app = Flask(__name__)

@app.route('/')
def home():
    # returns latest stored data for UI to render
    records = get_all_data()
    return render_template('index.html', fixtures=records)

@app.route('/api/fixtures')
def api_fixtures():
    records = get_all_data()
    return jsonify(records)

if __name__ == '__main__':
    # ensure DB exists
    db_setup()
    # start background updater (interval_minutes=2)
    background_updater(interval_minutes=2)
    port = int(os.environ.get('PORT', 5000))
    # recommended production start on Render is via gunicorn in Procfile
    app.run(host='0.0.0.0', port=port)
