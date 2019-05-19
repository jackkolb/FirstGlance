# SERVER FOR THE ROOM COMPUTERS!

from flask import Flask, render_template, request, redirect
import room_util
import time
import multiprocessing

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("roomindex.html")


@app.route("/eyes")
def eyes():
    return render_template("eyes.html")


@app.route("/medical", methods=["POST"])
def medical():
    if room_util.wait_for_doctor():
        return render_template("medical.html")
    else:
        return redirect("/", code=302)


def periodic():
    while True:
        
        time.sleep(5)

if __name__ == "__main__":
    p = multiprocessing.Process(target=periodic)
    p.start()

    room_util.get_room_number()


    app.run()
