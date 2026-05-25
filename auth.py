import bcrypt
import json
import os

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


def register(username, password):
    users = load_users()

    if username in users:
        return False

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    users[username] = hashed.decode()

    save_users(users)

    return True


def login(username, password):
    users = load_users()

    if username not in users:
        return False

    stored_hash = users[username].encode()

    return bcrypt.checkpw(password.encode(), stored_hash)