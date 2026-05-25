import csv
import os

CSV_HEADERS = ["Title", "EncryptedPassword", "URL", "Notes"]


def get_csv_path(username):
    return f"users/{username}/passwords.csv"


def initialize_csv(username):
    path = get_csv_path(username)

    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)


def read_passwords(username):
    path = get_csv_path(username)

    if not os.path.exists(path):
        return []

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_passwords(username, rows):
    path = get_csv_path(username)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)

        writer.writeheader()

        writer.writerows(rows)