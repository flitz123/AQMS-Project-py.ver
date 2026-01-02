from datetime import datetime
from models import Patient
from storage_service import StorageService


class QueueManager:
    def __init__(self):
        self.storage = StorageService()
        self.patients = self.storage.load_patients()
        self.counter = len(self.patients)

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
            return None

        def mark_served(self, token):
            for p in self.patients:
                if p.token == token:
                    p.status = "SERVED"
                    p.served_time = datetime.now()
                    self.storage.save_patients(self.patients)
                    return p

        def get_queue(self):
            return self.patients

        def served_count(self):
            return len([p for p in self.patients if p.status == "SERVED"])
