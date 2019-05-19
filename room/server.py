# SERVER FOR THE DOCTOR ROOM COMPUTERS!

from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import room_util
import multiprocessing

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eyes")
def eyes():
    return render_template("eyes.html")

@app.route("/close", methods=["GET"])
def close():
    room_util.open_room(room_util.room_number)
    return redirect("/", code=302)


@socketio.on('connect', namespace="/eye-catch")
def eyecatch():
    print("client connected - eyecatch")
    room_util.wait_for_doctor(room_util.doctor_name)
    socketio.emit('continue', {'pass': True}, namespace='/eye-catch')


@socketio.on('connect', namespace="/periodic")
def periodic():
    print("client connected - periodic")
    room_util.periodicLoop()
    socketio.emit('continue', {'pass': True}, namespace='/periodic')


@app.route("/medical")
def medical():
    doctor_name = room_util.doctor_name
    if room_util.wait_for_doctor(doctor_name):
        patient_data = room_util.get_patient_medical(room_util.patient_id)
        return render_template("medical.html", patient_id=room_util.patient_id, first_name=patient_data["first name"], last_name=patient_data["last name"], height=patient_data["height"], weight=patient_data["weight"], DOB=patient_data["DOB"], preferred_physician=patient_data["preferred physician"], medical_history=patient_data["medical history"], allergies=patient_data["allergies"])
    else:
        return redirect("/", code=302)

if __name__ == "__main__":
    room_util.get_room_number()
    app.run(host='0.0.0.0', port=4000)
