import tkinter as tk
from queue_manager import QueueManager


class DisplayUI(tk.Frame):
    """
    Display UI for showing the current called patient and
    the full queue in real time (read-only).
    """

    def __init__(self, master):
        super().__init__(master)
        self.qm = QueueManager()

        tk.Label(
            self,
            text="QUEUE DISPLAY",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        self.current_label = tk.Label(
            self,
            text="Current:None",
            font=("Arial", 24),
            fg="blue"
        )
        self.current_label.pack(pady=15)

        tk.Label(self, text="Full Queue").pack()
        self.queue_text = tk.Text(self, height=15, width=50)
        self.queue_text.pack(pady=5)

        self.refresh_display()

    def refresh_display(self):
        """Refresh the queue display every 2 seconds."""
        queue = self.qm.get_queue()

        # Determine current called patient
        current = "None"
        for p in queue:
            if p.status == "CALLED":
                current = f"{p.token} - {p.name}"
                break

        self.current_label.config(text=f"Current: {current}")

        self.queue_text.delete(1.0, tk.END)
        for p in queue:
            self.queue_text.insert(
                tk.END,
                f"{p.token} | {p.name} | {p.service_type} | {p.status}\n"
            )

        # Auto refresh every 2 seconds
        self.after(2000, self.refresh_display)
