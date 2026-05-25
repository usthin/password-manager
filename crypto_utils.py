from cryptography.fernet import Fernet
import os

KEY_FOLDER = "users"

def generate_key(username):
    path = f"{KEY_FOLDER}/{username}"

    if not os.path.exists(path):
        os.makedirs(path)

    key = Fernet.generate_key()

    with open(f"{path}/key.key", "wb") as f:
        f.write(key)

    return key


def load_key(username):
    path = f"{KEY_FOLDER}/{username}/key.key"

    if not os.path.exists(path):
        return generate_key(username)

    with open(path, "rb") as f:
        return f.read()


def get_cipher(username):
    key = load_key(username)
    return Fernet(key)


def encrypt_text(username, text):
    cipher = get_cipher(username)
    return cipher.encrypt(text.encode()).decode()


def decrypt_text(username, encrypted_text):
    cipher = get_cipher(username)
    return cipher.decrypt(encrypted_text.encode()).decode()


def encrypt_file(username):
    path = f"users/{username}/passwords.csv"

    if not os.path.exists(path):
        return

    with open(path, "rb") as f:
        data = f.read()

    cipher = get_cipher(username)
    encrypted_data = cipher.encrypt(data)

    with open(f"users/{username}/passwords.enc", "wb") as f:
        f.write(encrypted_data)

    os.remove(path)


import os

def decrypt_file(username):
    enc_path = f"users/{username}/passwords.enc"
    csv_path = f"users/{username}/passwords.csv"

    folder = f"users/{username}"

    # ✅ IMPORTANT: ensure folder exists
    os.makedirs(folder, exist_ok=True)

    if not os.path.exists(enc_path):
        # create empty CSV safely
        with open(csv_path, "w") as f:
            f