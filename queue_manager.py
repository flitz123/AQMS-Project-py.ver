from datetime import datetime
from models import Patient
from storage_service import StorageService


class QueueManager:
    def __init__(self):
        self.storage = StorageService()
        self.patients = self.storage.load_patients()
        numbers = []
        for patient in self.patients:
            if patient.token.startswith("T"):
                try:
                    numbers.append(int(patient.token[1:]))
                except ValueError:
                    pass
        self.counter = max(numbers, default=0)

    def register_patient(self, name, national_id, service_type):
        self.counter += 1
        token = f"T{self.counter:04d}"
        patient = Patient(token, name, national_id, service_type)
        self.patients.append(patient)
        self.storage.save_patients(self.patients)
        return patient

    def call_next(self):
        for p in self.patients:
            if p.status == "WAITING":
                p.status = "CALLED"
                p.called_time = datetime.now()
                self.storage.save_patients(self.patients)
                return p
        return None

    def call_patient(self, token):
        for patient in self.patients:
            if patient.token.upper() == token.upper() and patient.status == "WAITING":
                patient.status = "CALLED"
                patient.called_time = datetime.now()
                self.storage.save_patients(self.patients)
                return patient
        return None

    def mark_served(self, token):
        for p in self.patients:
            if p.token == token:
                p.status = "SERVED"
                p.served_time = datetime.now()
                self.storage.save_patients(self.patients)
                return p
        return None

    def update_status(self, token, status):
        if status not in {"SERVED", "CALLED", "WAITING", "CANCELLED", "NO_SHOW"}:
            return None
        for patient in self.patients:
            if patient.token == token:
                patient.status = status
                if status == "CALLED" and not patient.called_time:
                    patient.called_time = datetime.now()
                if status == "SERVED":
                    patient.served_time = datetime.now()
                self.storage.save_patients(self.patients)
                return patient
        return None

    def get_stats(self):
        return {
            "total": len(self.patients),
            "waiting": len([p for p in self.patients if p.status == "WAITING"]),
            "called": len([p for p in self.patients if p.status == "CALLED"]),
            "served": self.served_count(),
            "cancelled": len([p for p in self.patients if p.status in {"CANCELLED", "NO_SHOW"}]),
        }

    def get_queue(self):
        return self.patients

    def served_count(self):
        return len([p for p in self.patients if p.status == "SERVED"])
