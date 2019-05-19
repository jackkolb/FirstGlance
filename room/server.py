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

@socketio.on('connect', namespace="/eye-catch")
def eyecatch():
    print("client connected - eyecatch")
    room_util.wait_for_doctor("Sumanth Dara")
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
        return render_template("medical.html")
    else:
        return redirect("/", code=302)

if __name__ == "__main__":
    room_util.get_room_number()
    app.run(port=4000)
