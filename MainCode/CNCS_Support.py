import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

FREQ = 500 #pwm frequency
WATER_FREQ = 5 #time to wait before watering in seconds.
Water_NEXT = 0 #next time to water the plants
#constants that control how far each axis moves
X_Constant = 17
Y_Constant = 17
Z_Constant = 17

#GPIO pin names
X_Axis_Dir = 10
Y_Axis_Dir = 9
Z_Axis_Dir = 11
Planter_Dir = 15
UI_Enable = 12
Water_Solenoid = 4
SDA = 2
SCL = 3
X_Stop_Low = 6
X_Stop_High = 13
Y_Stop_Low = 19
Y_Stop_High = 26
Z_Stop_Low = 216
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
GPIO.setup((X_Axis_Dir,Y_Axis_Dir,Z_Axis_Dir,
            Planter_Dir,Water_Solenoid), GPIO.OUT)
GPIO.setup((X_Stop_Low,X_Stop_High,Y_Stop_Low,
            Y_Stop_High,Z_Stop_Low,Z_Stop_High),GPIO.IN)

def check_if_dry():
    #use I2C to get water sensor value
    #return value < Water_Constant
    return 1

def water():
    GPIO.write(1,Water_Solenoid)
    print("watering plant")
    sleep(0.5)
    GPIO.write(0,Water_Solenoid)

def Move(from_loc, to_loc):
    #the number of steps needed to travel that far
    X_Steps = (to_loc.x-from_loc.x)*X_Constant
    Y_Steps = (to_loc.y-from_loc.y)*Y_Constant
    Z_Steps = (to_loc.z-from_loc.z)*Z_Constant
    print("(X steps, Y steps) = (",str(X_Steps),str(Y_Steps),")")
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
    def distance(self, loc):
        return math.sqrt(pow(loc.x-self.x,2)+pow(loc.y-self.y,2))

class Plant:
    def __init__(self, x_loc, y_loc, size):
        self.location = Location(x_loc,y_loc)
        self.size = size
    def getx(self):
        return self.location.x
