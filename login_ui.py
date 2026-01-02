import tkinter as tk
from tkinter import messagebox

USERS = {
    "admin": ("admin123", "ADMIN"),
    "reception": ("receppass", "RECEPTION")
}


class LoginUI(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success

        tk.Label(self, text="AQMS Login", font=("Arial", 16)).pack(pady=10)
        self.username = tk.Entry(self)
        self.password = tk.Entry(self, show="*")
        self.username.pack()
        self.password.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if user in USERS and USERS[user][0] == pwd:
            self.on_success(USERS[user][1])
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
