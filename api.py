from flask import Flask, request, redirect, jsonify
import sqlite3
from datetime import datetime, timedelta
from time import sleep
from math import floor

app = Flask(__name__)
CONN = sqlite3.Connection("meds.db", check_same_thread=False)
CUR = CONN.cursor()


def time_to_deltatime(time):
    split_time = time.split(":")

    hours = int(split_time[0])
    minutes = int(split_time[1])
    seconds = int(split_time[2])

    deltatime = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return deltatime



@app.route('/nextmed', methods=['GET'])
def nextMed():
    current_datetime = datetime.now()
    round_seconds = floor(current_datetime.second)
    current_datetime.replace(second=round_seconds)

    nextDispenseTimes = CUR.execute("SELECT Datetime_NextDispense FROM events WHERE Dispensed = 'False'")
    nextDispenseTimes = nextDispenseTimes.fetchall()

    test = {}
    for time in nextDispenseTimes:
        datetime_obj = datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S.%f")
        test[datetime_obj - current_datetime] = datetime_obj

    min_datetime = min(test.values(), key=lambda x: x)
    print("=========================")
    print(min_datetime)
    print("=========================")

    find_event = f"SELECT EventID FROM events WHERE Datetime_NextDispense = '{min_datetime}'"
    event = CUR.execute(find_event).fetchall()
    eventID = event[0][0]

    find_medID = f"SELECT MedID FROM events WHERE EventID = {eventID}"
    medID = CUR.execute(find_medID).fetchall()[0][0]

    min_datetime = min_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({"NextMed": medID,
                    "Time": min_datetime})



@app.route('/dispense/<medID>', methods=['POST'])
def dispense(medID:int):
    def getCurrentTime():
        return datetime.now()

    def nextDispenseResult():
        current_datetime = datetime.now()
        print(datetime.now())
        round_seconds = floor(current_datetime.second)
        current_datetime.replace(second=round_seconds)

        time_interval = CUR.execute(f'SELECT `Dosing Interval` FROM medicine WHERE MedID = {medID}').fetchall()[0][0]

        newDispenseResult = current_datetime + time_to_deltatime(time_interval)
        
        return newDispenseResult

    #Dispense Code

    findLatestEvent = f"UPDATE events SET Dispensed = 'True' WHERE MedID = {medID} AND Dispensed = 'False'"
    latest_event = CUR.execute(findLatestEvent)
    latest_event = latest_event.fetchall()
    

    insertNewEvent = "INSERT INTO events (MedID, Datetime_Dispensed, Datetime_NextDispense, Dispensed) VALUES (?, ?, ?, ?)"
    newEventData = (int(medID), getCurrentTime(), nextDispenseResult(), "False")
    print(newEventData)
    CUR.execute(insertNewEvent, newEventData)
    CONN.commit()

    return jsonify({"Test": "123"})

@app.route('/presentation', methods=['GET'])
def presentation():
    CUR.execute("DELETE FROM events;")

    medID = CUR.execute('SELECT MedID, `Dosing Interval` FROM medicine')
    medID_list = medID.fetchall()

    for med in medID_list:
        current_datetime = datetime.now()
        round_seconds = floor(current_datetime.second)
        update = current_datetime.replace(second=round_seconds)
        
        print(update)

        sql = "INSERT INTO events (MedID, Datetime_Dispensed, Datetime_NextDispense, Dispensed) VALUES (?, ?, ?, ?)"
        data = (med[0], current_datetime, current_datetime + time_to_deltatime(med[1]), 'False')

        CUR.execute(sql, data)
        CONN.commit()
        

    return "Test"



app.run(debug=True, host='0.0.0.0', port='5000')