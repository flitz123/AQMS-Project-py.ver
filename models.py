from datetime import datetime


class Patient:
    def __init__(self, token, name, national_id, service_type):
        self.token = token
        self.name = name
        self.national_id = national_id
        self.service_type = service_type
        self.arrival_time = datetime.now()
        self.status = "WAITING"
        self.called_time = None
        self.served_time = None

    def to_csv(self):
        return [
            self.token,
            self.name,
            self.national_id,
            self.service_type,
            self.arrival_time.isoformat(),
            self.status,
            self.called_time.isoformat() if self.called_time else "",
            self.served_time.isoformat() if self.served_time else ""
        ]

    @staticmethod
    def from_csv(row):
        p = Patient(row[0], row[1], row[2], row[3])
        p.arrival_time = datetime.fromisoformat(row[4])
        p.status = row[5]
        if row[6]:
            p.called_time = datetime.fromisoformat(row[6])
        if row[7]:
            p.served_time = datetime.fromisoformat(row[7])
        return p
