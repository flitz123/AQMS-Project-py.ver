import tkinter as tk
from queue_manager import QueueManager


class AdminUI(tk.Frame):
    """
    Admin UI for generating reports and monitoring system activity.
    """

    def __init__(self, master):
        super().__init__(master)
        self.qm = QueueManager()

        tk.Label(
            self,
            text="ADMIN PANEL",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Button(
            self,
            text="Generate Report",
            command=self.generate_report
        ).pack(pady=5)

        self.report_text = tk.Text(self, height=20, width=60)
        self.report_text.pack(pady=10)

    def generate_report(self):
        """Generate a basic queue and service report."""
        self.report_text.delete(1.0, tk.END)

        served_count = self.qm.served_count()
        queue = self.qm.get_queue()

        self.report_text.insert(tk.END, "DAILY QUEUE REPORT\n")
        self.report_text.insert(tk.END, "-" * 30 + "\n")
        self.report_text.insert(tk.END, f"Patients Served: {served_count}\n\n")

        self.report_text.insert(tk.END, "Queue Status:\n")
        for p in queue:
            self.report_text.insert(
                tk.END,
                f"{p.token} | {p.name} | {p.service_type} | {p.status}\n"
            )
