from time import time
import sqlite3


#Global Variables
CONN = sqlite3.Connection('meds.db', check_same_thread=False)
CUR = CONN.cursor()

class Meds:
    def __init__(self, name:str, time_interval:str):
        self.name = name
        self.time_interval = time_interval

    #setters and getters
    def getName():
        return self.name
    def setName(name:str):
        self.name = name
    
    def getTime_interval():
        return self.time_interval
    def setTime_interval(time_interval:str):
        self.time_interval = time_interval

    def formatTime(self):
        time_input = self.time_interval
        if len(time_input) < 3:
            time_input = [letter for letter in time_input]
            time_input.insert(0, "0")
            time_input = ''.join(time_input)

        category = time_input[-1]
        time_amount = time_input[:2]

        times = {"s": f"00:00:{time_amount}",
                 "m": f"00:{time_amount}:00",
                 "h": f"{time_amount}:00:00"}

        return times[category]

    def addMed(self):
        sql = "INSERT INTO `medicine` (`Name`, `Dosing Interval`) VALUES (?, ?)"
        data = (self.name, self.formatTime())
        CUR.execute(sql, data)  # Pass variables as a tuple
        CONN.commit() 


def getMedList():
    med_list = CUR.execute("SELECT Name, `Dosing Interval` FROM medicine;")
    return(med_list.fetchall())