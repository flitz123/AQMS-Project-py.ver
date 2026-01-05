import tkinter as tk
from queue_manager import QueueManager


class ReceptionUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.qm = QueueManager()

        tk.Label(self, text="Reception Panel").pack()
        self.name = tk.Entry(self)
        self.nid = tk.Entry(self)
        self.service = tk.Entry(self)

        self.name.pack()
        self.nid.pack()
        self.service.pack()

        tk.Button(self, text="Register Patient", command=self.register).pack()
        tk.Button(self, text="Call_Next", command=self.call_next).pack()

        self.log = tk.Text(self, height=10)
        self.log.pack()

    def register(self):
        p = self.qm.register_patient(
            self.name.get(), self.nid.get(), self.service.get()
        )
        self.log.insert(tk.END, f"Registered {p.token} - {p.name}\n")

    def call_next(self):
        p = self.qm.call_next()
        if p:
            self.log.insert(tk.END, f"Called {p.token} - {p.name}\n")
