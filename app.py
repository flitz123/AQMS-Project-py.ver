from datetime import datetime
from flask import Flask, jsonify, render_template, request
from queue_manager import QueueManager
from auth import authenticate

app = Flask(__name__)
qm = QueueManager()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    role = authenticate(data.get("username"), data.get("password"))
    if role:
        return jsonify({"message": "Login Successful", "role": role})
    return jsonify({"message": "Invalid Credentials"}), 401

@app.route("/patients", methods=["POST"])
def register_patient():
    data = request.get_json(silent=True) or {}
    required = ("name", "national_id", "service_type")
    missing = [field for field in required if not str(data.get(field, "")).strip()]
    if missing:
        return jsonify({"message": "Please complete all required fields"}), 400
    patient = qm.register_patient(
        str(data["name"]).strip(),
        str(data["national_id"]).strip(),
        str(data["service_type"]).strip(),
    )
    return jsonify(patient.to_dict()), 201

@app.route("/queue/call-next", methods=["POST"])
def call_next():
    patient = qm.call_next()
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"message": "No waiting patients"}), 404


@app.route("/patients/<token>/call", methods=["POST"])
def call_patient(token):
    patient = qm.call_patient(token)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"message": "Patient is not available to call"}), 404

@app.route("/queue", methods=["GET"])
def view_queue():
    return jsonify([p.to_dict() for p in qm.get_queue()])


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify(qm.get_stats())


@app.route("/patients/<token>/status", methods=["PATCH"])
def update_status(token):
    data = request.get_json(silent=True) or {}
    patient = qm.update_status(token.upper(), str(data.get("status", "")).upper())
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"message": "Patient not found"}), 404


@app.route("/patients/<token>/serve", methods=["POST", "GET"])
def mark_served(token):
    patient = qm.mark_served(token.upper())
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"message": "Patient not found"}), 404


@app.route("/reports/daily", methods=["GET"])
def daily_report():
    today = datetime.now().date()
    today_patients = [p for p in qm.get_queue() if p.arrival_time.date() == today]
    return jsonify({
        "patient_served": len([p for p in today_patients if p.status == "SERVED"]),
        "stats": qm.get_stats(),
        "queue": [p.to_dict() for p in today_patients]
    })


if __name__ == "__main__":
    app.run(debug=True)
