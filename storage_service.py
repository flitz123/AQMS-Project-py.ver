import csv
import os
from models import Patient


class StorageService:
    def __init__(self, filename="data/patients.csv"):
        self.filename = filename
        os.makedirs("data", exist_ok=True)

    def load_patients(self):
        patients = []
        if not os.path.exists(self.filename):
            return patients
        with open(self.filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                patients.append(Patient.from_csv(row))
        return patients

    def save_patients(self, patients):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for p in patients:
                writer.writerow(p.to_csv())
