# _1 files are formatted for PEP 8 and updated to include button functionality
import RPi.GPIO as GPIO
from gpiozero import Button
from time import sleep
import math

GPIO.setmode(GPIO.BOARD)

# GPIO pin names
UI_Plant = 12
X_Axis_Dir = 8
Y_Axis_Dir = 19
Z_Axis_Dir = 24
Planter_Dir = 31
Water_Solenoid = 4
SDA = 3
SCL = 5
X_Stop_Low = 12
X_Stop_High = 15
Y_Stop_Low = 35
Y_Stop_High = 37
Z_Stop_Low = 38
Z_Stop_High = 40

# GPIO pin definitions
button_water = Button(UI_Water)
button_plant = Button(UI_Plant)
GPIO.setup(10, GPIO.OUT)
X_Axis_PWM = GPIO.PWM(10, 1000)
GPIO.setup(21, GPIO.OUT)
Y_Axis_PWM = GPIO.PWM(21, 1000)
GPIO.setup(25, GPIO.OUT)
Z_Axis_PWM = GPIO.PWM(25, 1000)
GPIO.setup(33, GPIO.OUT)
Planter_PWM = GPIO.PWM(33, 1000)
GPIO.setup((X_Axis_Dir, Y_Axis_Dir, Z_Axis_Dir,
            Planter_Dir, Water_Solenoid), GPIO.OUT)
GPIO.setup((X_Stop_Low, X_Stop_High, Y_Stop_Low,
            Y_Stop_High, Z_Stop_Low, Z_Stop_High), GPIO.IN)

X_Constant = 17
Y_Constant = 17
Z_Constant = 17


def check_if_dry():
    # move to location
    # use I2C to get water sensor value
    # return value < Water_Constant
    # return 1 if need water, 0 if not
    return 1


def water():
    # gpio.write(1,Water_Solenoid)
    print("watering plant")
    sleep(1)
    # gpio.write(0,Water_Solenoid)


def move(from_loc, to_loc):
    # the distance in inches
    delta_x = to_loc.x - from_loc.x
    delta_y = to_loc.y - from_loc.y
    delta_z = to_loc.z - from_loc.z
    # the number of steps needed to travel that far
    x_steps = delta_x * X_Constant
    y_steps = delta_y * Y_Constant
    z_steps = delta_z * Z_Constant
    print("(X steps, Y steps) = (", str(x_steps), str(y_steps), ")")
    # global location
    # location = to_loc
    return to_loc


# gave location a fourth parameter for if a plant is planted in that location
class Location:
    def __init__(self, x=0, y=0, z=0, p=0):
        self.x = x
        self.y = y
        self.z = z
        self.p = p

    def update(self, loc):
        self.x = loc.x
        self.y = loc.y
        self.z = loc.z
        self.p = loc.p
        return self

    def distance(self, loc):
        return math.sqrt(pow(loc.x - self.x, 2) + pow(loc.y - self.y, 2))


class Plant:
    def __init__(self, x_loc, y_loc, size):
        self.location = Location(x_loc, y_loc)
        self.size = size

    def getx(self):
        return self.location.x
