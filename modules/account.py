import json
import os

DATA_FILE = 'data/un_pw.json'

def load_up():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_up(up):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(up, file, ensure_ascii=False, indent=4)

def add_up(username, password):
    up = load_up()

    new_up = {
        "username": username,
        "password": password,
    }

    up.append(new_up)

    save_up(up)

def get_up():
    up = load_up()
    return up