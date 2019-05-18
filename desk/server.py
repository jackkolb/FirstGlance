from flask import Flask, render_template, request, redirect
import checkin
import time
import multiprocessing

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def login():
    patient_id = request.form["patient_id"]
    checkin.checkin_patient(patient_id)
    return redirect("/", code=302)

def periodic():
    while True:
        checkin.align_rooms()
        time.sleep(5)

if __name__ == "__main__":
    p = multiprocessing.Process(target=periodic)
    p.start()

    app.run()
