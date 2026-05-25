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

        self.root.title(f"Password Manager - {username}")
        self.root.geometry("700x500")

        initialize_csv(username)

        # ---------------- UI FIELDS ----------------

        tk.Label(root, text="Title").pack()
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, width=50, show="*")
        self.password_entry.pack()

        tk.Label(root, text="URL/App").pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

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

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- CORE FEATURES ----------------

    def add_password(self):
        title = self.title_entry.get()
        password = self.password_entry.get()
        url = self.url_entry.get()
        notes = self.notes_entry.get()

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

        messagebox.showinfo("Success", "Password added")

    def search_password(self):
        title = self.title_entry.get()
        rows = read_passwords(self.username)

        for row in rows:
            if row["Title"] == title:
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, "********")

                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, row["URL"])

                self.notes_entry.delete(0, tk.END)
                self.notes_entry.insert(0, row["Notes"])

                self.current_password = row["EncryptedPassword"]

                return

        messagebox.showerror("Error", "Entry not found")

    def reveal_password(self):
        if self.current_password:
            decrypted = decrypt_text(self.username, self.current_password)

            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, decrypted)

    def update_password(self):
        title = self.title_entry.get()
        rows = read_passwords(self.username)

        for row in rows:
            if row["Title"] == title:
                row["EncryptedPassword"] = encrypt_text(
                    self.username,
                    self.password_entry.get()
                )

                row["URL"] = self.url_entry.get()
                row["Notes"] = self.notes_entry.get()

                write_passwords(self.username, rows)

                messagebox.showinfo("Success", "Password updated")
                return

        messagebox.showerror("Error", "Entry not found")

    def delete_password(self):
        title = self.title_entry.get()

        rows = read_passwords(self.username)
        new_rows = [r for r in rows if r["Title"] != title]

        write_passwords(self.username, new_rows)

        messagebox.showinfo("Success", "Password deleted")

    # ---------------- EXTRA FEATURES ----------------

    def copy_password(self):
        if self.current_password:
            decrypted = decrypt_text(self.username, self.current_password)

            self.root.clipboard_clear()
            self.root.clipboard_append(decrypted)

            messagebox.showinfo("Success", "Password copied to clipboard")

    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(16))

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    # ---------------- LOGOUT + CLOSE ----------------

    def logout(self):
        encrypt_file(self.username)

        messagebox.showinfo("Logout", "You have been logged out")

        self.root.destroy()

        import main
        main.start_login()

    def on_close(self):
        encrypt_file(self.username)
        self.root.destroy()