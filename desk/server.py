from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def login():
    patient_id = request.form["patient_id"]
    print(patient_id)
    return redirect("/", code=302)

 app.run()