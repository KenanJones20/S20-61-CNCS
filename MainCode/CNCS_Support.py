
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

#GPIO pin names
UI_Enable = 12
X_Axis_Dir = 18
Y_Axis_Dir = 23
Z_Axis_Dir = 8
Planter_Dir = 10
Water_Solenoid = 4
SDA = 2
SCL = 3
X_Stop_Low = 5
X_Stop_High = 6
Y_Stop_Low = 13
Y_Stop_High = 19
Z_Stop_Low = 20
Z_Stop_High = 21

#GPIO pin definitions
GPIO.setup(UI_Enable, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
X_Axis_PWM = GPIO.PWM(17,1000)
GPIO.setup(22, GPIO.OUT)
Y_Axis_PWM = GPIO.PWM(22,1000)
GPIO.setup(7, GPIO.OUT)
Z_Axis_PWM = GPIO.PWM(7,1000)
GPIO.setup(9, GPIO.OUT)
Planter_PWM = GPIO.PWM(9,1000)
GPIO.setup((X_Axis_Dir,Y_Axis_Dir,Z_Axis_Dir,
            Planter_Dir,Water_Solenoid), GPIO.OUT)
GPIO.setup((X_Stop_Low,X_Stop_High,Y_Stop_Low,
            Y_Stop_High,Z_Stop_Low,Z_Stop_High),GPIO.IN)

X_Constant = 17
Y_Constant = 17
Z_Constant = 17

def check_if_dry():
    #use I2C to get water sensor value
    #return value < Water_Constant
    return 1

def water():
    #gpio.write(1,Water_Solenoid)
    print("watering plant")
    sleep(1)
    #gpio.write(0,Water_Solenoid)

def Move(from_loc, to_loc):
    #the distance in inches
    Delta_x = to_loc.x-from_loc.x
    Delta_y = to_loc.y-from_loc.y
    Delta_z = to_loc.z-from_loc.z
    #the number of steps needed to travel that far
    X_Steps = Delta_x*X_Constant
    Y_Steps = Delta_y*Y_Constant
    Z_Steps = Delta_z*Z_Constant
    print("(X steps, Y steps) = (",str(X_Steps),str(Y_Steps),")")
    #global location
    #location = to_loc
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