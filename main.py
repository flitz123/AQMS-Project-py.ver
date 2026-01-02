import tkinter as tk
from login_ui import LoginUI
from reception_ui import ReceptionUI


def launch_app(role):
    root.destroy()
    app = tk.Tk()
    app.title("AQMS - Python ver")
    app.geometry("800x600")

    tabs = tk.ttk.NoteBook(app)

    reception = ReceptionUI(tabs)
    display = DisplayUI(tabs)
    admin = AdminUI(tabs)

    tabs.add(reception, text="Reception")
    tabs.add(display, text="Display")
    tabs.add(admin, text="Admin")

    tabs.pack(expand=1, fill="both")
    app.mainloop()


root = tk.Tk()
root.title("AQMS - Python ver - Login")
LoginUI(root, launch_app).pack(padx=20, pady=20)
root.mainloop()
