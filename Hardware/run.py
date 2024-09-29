import gpiozero as zero
from time import sleep
from datetime import datetime
import requests

Motor_A = zero.OutputDevice(17)
Motor_B = zero.OutputDevice(27)
Motor_C = zero.OutputDevice(22)

def run_motor(x:int):
    if x == 1:
        Motor_A.on()
        sleep(0.5)
        Motor_A.off()
    elif x == 2:
        Motor_B.on()
        sleep(0.5)
        Motor_B.off()
    elif x == 3:
        Motor_C.on()
        sleep(0.5)
        Motor_C.off()

def presentation():
    requests.get('http://10.0.0.179:5000/presentation')
    
    for i in range(10):
        nextmed_response = requests.get('http://10.0.0.179:5000/presentation').json()
        
        medID = nextmed_response['NextMed']
        execute_time = nextmed_response['Time']
        execute_time = execute_time.strptime(execute_time,'%Y-%m-%d %H:%M:%S')
        
        stop = False
        while stop == False:
            current_time = datetime.now()
            if current_time >= execute_time:
                run_motor(nextmed)
                requests.post(f'http://10.0.0.179:5000/dispense/{medID}')
                stop = True
            sleep(5)
            
presentation()
        