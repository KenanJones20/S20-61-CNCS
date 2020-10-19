import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

FREQ = 500 #pwm frequency
#The number of steps each stepper motor axis moves per inch
X_Constant = 200
Y_Constant = 200
Z_Constant = 200

#GPIO pin names
X_Dir = 10
Y_Dir = 9
Z_Dir = 11
Planter_Dir = 15
UI_Enable = 12
Water_Solenoid = 4
SDA = 2
SCL = 3
X_Stop_Low = 6
X_Stop_High = 13
Y_Stop_Low = 19
Y_Stop_High = 26
Z_Stop_Low = 16
Z_Stop_High = 20

#GPIO pin definitions
GPIO.setup(UI_Enable, GPIO.IN)
GPIO.setup(25, GPIO.OUT)
X_Axis_PWM = GPIO.PWM(25,FREQ)
GPIO.setup(8, GPIO.OUT)
Y_Axis_PWM = GPIO.PWM(8,FREQ)
GPIO.setup(7, GPIO.OUT)
Z_Axis_PWM = GPIO.PWM(7,FREQ)
GPIO.setup(18, GPIO.OUT)
Planter_PWM = GPIO.PWM(18,FREQ)
GPIO.setup((X_Dir,Y_Dir,Z_Dir,
            Planter_Dir,Water_Solenoid), GPIO.OUT)
GPIO.setup((X_Stop_Low,X_Stop_High,Y_Stop_Low,
            Y_Stop_High,Z_Stop_Low,Z_Stop_High),GPIO.IN)

def check_if_dry():
    #Use I2C to get water sensor value.
    #Return value < Water_Constant.
    return 1

def water():
    GPIO.output(Water_Solenoid, GPIO.HIGH)
    print("watering plant")
    sleep(0.5)
    GPIO.output(Water_Solenoid, GPIO.LOW)

def Move(from_loc, to_loc):
    #Find the number of steps to move each axis.
    X_Steps = (to_loc.x-from_loc.x)*X_Constant
    Y_Steps = (to_loc.y-from_loc.y)*Y_Constant
    Z_Steps = (to_loc.z-from_loc.z)*Z_Constant
    print("(X steps, Y steps) = (",str(X_Steps),str(Y_Steps),")")
    
    GPIO.output(X_Dir, GPIO.HIGH if (X_Steps>0) else GPIO.LOW)
    X_Axis_PWM.start(50)
    sleep(abs(X_Steps/FREQ))
    X_Axis_PWM.stop()

    GPIO.output(Y_Dir, GPIO.HIGH if (Y_Steps>0) else GPIO.LOW)
    Y_Axis_PWM.start(50)
    sleep(abs(Y_Steps/FREQ))
    Y_Axis_PWM.stop()

    GPIO.output(Z_Dir, GPIO.HIGH if (Z_Steps>0) else GPIO.LOW)
    Z_Axis_PWM.start(50)
    sleep(abs(Z_Steps/FREQ))
    Z_Axis_PWM.stop()

    return to_loc

class Location:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def update(self, loc):
        self.x = loc.x
        self.y = loc.y
        self.z = loc.z
        return self

class Plant:
    def __init__(self, x_loc, y_loc, size):
        self.location = Location(x_loc,y_loc)
        self.size = size

    def getx(self):
        return self.location.x
