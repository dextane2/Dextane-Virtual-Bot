import json
import os

DB_FILE = "predictions.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def store_fixture(fixture):
    init_db()
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    data.append(fixture)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_all_data():
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)
