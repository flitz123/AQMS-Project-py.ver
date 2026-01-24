# Flask REST API script for the AQMS project:

from flask import Flask, request, jsonify
from queue_manager import QueueManager
from auth import authenticate

app = Flask(__name__)
qm = QueueManager

# AUTH


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    role = authenticate(data.get("username"), data.get("password"))
    if role:
        return jsonify({"message": "Login Successful", "role": role})
    return jsonify({"message": "Invalid Credentials"}), 401

# RECEPTION


@app.route("/patients", methods=["POST"])
def register_patient():
    data = request.json
    patient = qm.register_patient(
        data["name"],
        data["national_id"],
        data["service_type"]
    )
    return jsonify(patient.to_dict()), 201


@app.route("/queue/call-next", methods=["POST"])
def call_next():
    patient = qm.call_next()
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"message": "No waiting patients"}), 404

# ADMIN


@app.route("/queue", methods=["GET"])
def view_queue():
    return jsonify([p.to_dict() for p in qm.get_queue()])


@app.route("/patients/<token>/serve", methods=["GET"])
def mark_served(token):
    patient = qm.mark_served(token)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"message": "Patient not found"}), 404


@app.route("/reports/daily", methods=["GET"])
def daily_report():
    return jsonify({
        "patient_served": qm.served_count(),
        "queue": [p.to_dict() for p in qm.get_queue()]
    })


if__name__ == "__main__":
app.run(debug=True)
