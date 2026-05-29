import os
import bcrypt
import json

USERS_FILE = "users.json"
BASE = "users"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register(username, password):

    users = load_users()

    if username in users:
        return False

    # create user folder HERE ✅ IMPORTANT FIX
    user_path = f"{BASE}/{username}"
    os.makedirs(user_path, exist_ok=True)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    users[username] = hashed
    save_users(users)

    return True


def login(username, password):

    users = load_users()

    if username not in users:
        return False

    stored = users[username].encode()

    return bcrypt.checkpw(password.encode(), stored)