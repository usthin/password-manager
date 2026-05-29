# Updated `password_manager.py`


import tkinter as tk
from tkinter import messagebox
from storage import read_passwords, write_passwords, initialize_csv
from crypto_utils import encrypt_text, decrypt_text, encrypt_file
import secrets
import string


class PasswordManager:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.current_password = None
        self.is_closed = False

        self.root.title(f"Password Manager - {username}")
        self.root.geometry("700x500")

        initialize_csv(username)

        # ---------------- TITLE ----------------

        tk.Label(root, text="Title").pack()
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack()

        # ---------------- PASSWORD ----------------

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, width=50, show="*")
        self.password_entry.pack()

        # ---------------- URL ----------------

        tk.Label(root, text="URL/App").pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        # ---------------- NOTES ----------------

        tk.Label(root, text="Notes").pack()
        self.notes_entry = tk.Entry(root, width=50)
        self.notes_entry.pack()

        # ---------------- BUTTONS ----------------

        tk.Button(root, text="Add", command=self.add_password).pack(pady=3)
        tk.Button(root, text="Search", command=self.search_password).pack(pady=3)
        tk.Button(root, text="Update", command=self.update_password).pack(pady=3)
        tk.Button(root, text="Delete", command=self.delete_password).pack(pady=3)

        tk.Button(root, text="Reveal Password", command=self.reveal_password).pack(pady=3)
        tk.Button(root, text="Copy Password", command=self.copy_password).pack(pady=3)
        tk.Button(root, text="Generate Password", command=self.generate_password).pack(pady=3)

        tk.Button(root, text="Logout", command=self.logout).pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- ADD PASSWORD ----------------

    def add_password(self):

        title = self.title_entry.get().strip()
        password = self.password_entry.get().strip()
        url = self.url_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not title or not password:
            messagebox.showerror("Error", "Title and Password required")
            return

        encrypted_password = encrypt_text(self.username, password)

        rows = read_passwords(self.username)

        rows.append({
            "Title": title,
            "EncryptedPassword": encrypted_password,
            "URL": url,
            "Notes": notes
        })

        write_passwords(self.username, rows)

        # save latest encrypted password
        self.current_password = encrypted_password

        messagebox.showinfo("Success", "Password added successfully")

    # ---------------- SEARCH PASSWORD ----------------

    def search_password(self):

        title = self.title_entry.get().strip()

        if not title:
            messagebox.showerror("Error", "Enter title to search")
            return

        rows = read_passwords(self.username)

        for row in rows:

            saved_title = row["Title"].strip()

            if saved_title.lower() == title.lower():

                # store encrypted password
                self.current_password = row["EncryptedPassword"]

                # hide password initially
                self.password_entry.config(show="*")

                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, "Hidden Password")

                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, row["URL"])

                self.notes_entry.delete(0, tk.END)
                self.notes_entry.insert(0, row["Notes"])

                messagebox.showinfo("Success", "Entry found")
                return

        messagebox.showerror("Error", "Entry not found")

    # ---------------- REVEAL PASSWORD ----------------

    def reveal_password(self):

        if not self.current_password:
            messagebox.showerror("Error", "Search for a password first")
            return

        try:
            decrypted = decrypt_text(
                self.username,
                self.current_password
            )

            self.password_entry.config(show="")

            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, decrypted)

        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed:\n{e}")

    # ---------------- UPDATE PASSWORD ----------------

    def update_password(self):

        title = self.title_entry.get().strip()

        rows = read_passwords(self.username)

        for row in rows:

            if row["Title"].strip().lower() == title.lower():

                encrypted_password = encrypt_text(
                    self.username,
                    self.password_entry.get()
                )

                row["EncryptedPassword"] = encrypted_password
                row["URL"] = self.url_entry.get()
                row["Notes"] = self.notes_entry.get()

                write_passwords(self.username, rows)

                self.current_password = encrypted_password

                messagebox.showinfo("Success", "Password updated")
                return

        messagebox.showerror("Error", "Entry not found")

    # ---------------- DELETE PASSWORD ----------------

    def delete_password(self):

        title = self.title_entry.get().strip()

        rows = read_passwords(self.username)

        new_rows = [
            r for r in rows
            if r["Title"].strip().lower() != title.lower()
        ]

        write_passwords(self.username, new_rows)

        self.current_password = None

        messagebox.showinfo("Success", "Password deleted")

    # ---------------- COPY PASSWORD ----------------

    def copy_password(self):

        password = self.password_entry.get()

        if not password or password == "Hidden Password":
            messagebox.showerror("Error", "No visible password to copy")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)

        messagebox.showinfo("Success", "Password copied")

    # ---------------- GENERATE PASSWORD ----------------

    def generate_password(self):

        chars = string.ascii_letters + string.digits + "!@#$%^&*"

        password = ''.join(secrets.choice(chars) for _ in range(16))

        self.password_entry.config(show="")

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    # ---------------- LOGOUT ----------------

    def logout(self):

        if not self.is_closed:
            encrypt_file(self.username)
            self.is_closed = True

        messagebox.showinfo("Logout", "You have been logged out")

        self.root.destroy()

        import main
        main.start_login()

    # ---------------- WINDOW CLOSE ----------------

    def on_close(self):

        if not self.is_closed:
            encrypt_file(self.username)
            self.is_closed = True

        self.root.destroy()

