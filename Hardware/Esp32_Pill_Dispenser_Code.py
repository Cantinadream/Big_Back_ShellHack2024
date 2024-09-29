from machine import Pin
from time import sleep

Motor_A1 = Pin(27, Pin.OUT)
Motor_A2 = Pin(26, Pin.OUT)
Motor_A3 = Pin(25, Pin.OUT)
Motor_A4 = Pin(33, Pin.OUT)

Motor_B1 = Pin(16, Pin.OUT)
Motor_B2 = Pin(17, Pin.OUT)
Motor_B3 = Pin(18, Pin.OUT)
Motor_B4 = Pin(19, Pin.OUT)

Motor_C1 = Pin(21, Pin.OUT)
Motor_C2 = Pin(22, Pin.OUT)
Motor_C3 = Pin(32, Pin.OUT)
Motor_C4 = Pin(23, Pin.OUT)

Run_A = Pin(2, Pin.IN)
Run_B = Pin(4, Pin.IN)
Run_C = Pin(34, Pin.IN,Pin.PULL_DOWN)


step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def stepper_A(steps, delay):
    for _ in range(steps):
        for step in step_sequence:
            Motor_A1.value(step[0])
            Motor_A2.value(step[1])
            Motor_A3.value(step[2])
            Motor_A4.value(step[3])
            sleep(delay)
            
def stepper_B(steps, delay):
    for _ in range(steps):
        for step in step_sequence:
            Motor_B1.value(step[0])
            Motor_B2.value(step[1])
            Motor_B3.value(step[2])
            Motor_B4.value(step[3])
            sleep(delay)
            
def stepper_C(steps, delay):
    for _ in range(steps):
        for step in step_sequence:
            Motor_C1.value(step[0])
            Motor_C2.value(step[1])
            Motor_C3.value(step[2])
            Motor_C4.value(step[3])
            sleep(delay)
# Example usage: Move the stepper motor 512 steps with a delay of 10ms
while True:
    
    if Run_A.value() == 1:
        stepper_A(512, 0.001)
        
    elif Run_B.value() == 1:
        stepper_B(512, 0.001)
    
    elif Run_C.value() == 1:
        stepper_C(512, 0.001)

