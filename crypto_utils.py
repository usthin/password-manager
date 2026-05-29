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

    csv_path = f"users/{username}/passwords.csv"
    enc_path = f"users/{username}/passwords.enc"

    if not os.path.exists(csv_path):
        return

    with open(csv_path, "rb") as f:
        data = f.read()

    cipher = get_cipher(username)
    encrypted = cipher.encrypt(data)

    with open(enc_path, "wb") as f:
        f.write(encrypted)

    # DO NOT DELETE FILE IF YOU WANT SAFETY
    # OR only delete AFTER successful encryption
    os.remove(csv_path)

import os

def decrypt_file(username):

    enc_path = f"users/{username}/passwords.enc"
    csv_path = f"users/{username}/passwords.csv"

    if not os.path.exists(enc_path):
        open(csv_path, "w").close()
        return

    with open(enc_path, "rb") as f:
        encrypted = f.read()

    cipher = get_cipher(username)
    decrypted = cipher.decrypt(encrypted)

    with open(csv_path, "wb") as f:
        f.write(decrypted)