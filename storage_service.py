import csv
import os
from pathlib import Path
from models import Patient


class StorageService:
    def __init__(self, filename="data/patients.csv"):
        filename = os.getenv("AQMS_DATA_FILE", filename)
        self.filename = filename
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

    def load_patients(self):
        patients = []
        if not os.path.exists(self.filename):
            return patients
        with open(self.filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 5:
                    patients.append(Patient.from_csv(row[:8] + [""] * max(0, 8 - len(row))))
        return patients

    def save_patients(self, patients):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for p in patients:
                writer.writerow(p.to_csv())
