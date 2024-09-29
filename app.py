from flask import Flask, render_template, request, redirect, jsonify
import med_functions

app = Flask(__name__)

@app.route("/")
def index():
    medList = med_functions.getMedList()
    return render_template('index.html', medList=medList)

@app.route("/getMedList")
def getMedList():
    medList = med_functions.getMedList()
    return medList


@app.route("/addMed", methods=["POST"])
def addMed():
    name = request.form['name']
    time = request.form['time-interval']

    new_med = med_functions.Meds(name, time)
    new_med.addMed()

    return(redirect('/'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')