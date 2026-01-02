class NotificationServices:
    def notify(self, patient, message):
        print(f"[NOTIFICATION] {patient.token} - {patient.name} : {message}")
