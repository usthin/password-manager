import tkinter as tk
from auth import register, login
from crypto_utils import decrypt_file
from password_manager import PasswordManager
from tkinter import messagebox


def start_login():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        root.geometry("300x250")

        tk.Label(root, text="Username").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login_user).pack(pady=10)
        tk.Button(root, text="Register", command=self.register_user).pack()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if register(username, password):
            messagebox.showinfo("Success", "Registered successfully")
        else:
            messagebox.showerror("Error", "User already exists")

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login(username, password):
            decrypt_file(username)

            self.root.destroy()

            dashboard = tk.Tk()
            PasswordManager(dashboard, username)
            dashboard.mainloop()

        else:
            messagebox.showerror("Error", "Invalid credentials")


if __name__ == "__main__":
    start_login()