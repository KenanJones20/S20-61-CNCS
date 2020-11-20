import gpiozero as zero
from time import sleep
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw

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
    def __init__(self, x_loc, y_loc):
        self.location = Location(x_loc, y_loc)

    def getx(self):
        return self.location.x

HOME = Location(0,0,10) #home location to return to when not operating
plants = [] #list of all the plants
WATER_FREQ = 5 #number of seconds to wait before watering again
DELAY = 0.001  #Pulse duration in seconds
#The number of steps each stepper motor moves per inch
X_Constant = 21
Y_Constant = 250
Z_Constant = 250

X_Dir = zero.LED(10)
X_Pulse = zero.LED(25)
Y_Dir = zero.LED(9)
Y_Pulse = zero.LED(8)
Z_Dir = zero.LED(11)
Z_Pulse = zero.LED(7)
Planter_Dir = zero.LED(15)
Planter_Pulse = zero.LED(18)
Planter_Solenoid = zero.LED(23)
Water_Solenoid = zero.LED(4)
X_Stop_Low = zero.Button(6)
X_Stop_High = zero.Button(13)
Y_Stop_Low = zero.Button(19)
Y_Stop_High = zero.Button(26)
Z_Stop_Low = zero.Button(16)
Z_Stop_High = zero.Button(20)

i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

def check_if_dry():
    if(ss.moisture_read()>500):
        return 0
    else:
        return 1

def water():
    Water_Solenoid.on()
    print("watering plant")
    sleep(1)
    Water_Solenoid.off()
    return None

def __move__(pulse_channel, direc_channel, end_stop, value, steps):
    if value:
        direc_channel.on()
    else:
        direc_channel.off()
    step = 0
    while not(end_stop.is_pressed):
        if step < steps:
            pulse_channel.on()
            step = step + 1
            sleep(DELAY)
            pulse_channel.off()
            sleep(DELAY)
        else: break
    return None

def Move(from_loc, to_loc):
    X_Steps = (to_loc.x-from_loc.x)*X_Constant
    Y_Steps = (to_loc.y-from_loc.y)*Y_Constant
    Z_Steps = (to_loc.z-from_loc.z)*Z_Constant
    print("(X steps, Y steps) = (" + str(X_Steps)
                    +","+str(Y_Steps)+")")

    if Z_Steps > 0:
        __move__(Z_Pulse, Z_Dir, Z_Stop_High, 1, Z_Steps)
    if X_Steps > 0:
        __move__(X_Pulse, X_Dir, X_Stop_High, 1, X_Steps)
    else:
        __move__(X_Pulse, X_Dir, X_Stop_Low, 0, abs(X_Steps))
    if Y_Steps > 0:
        __move__(Y_Pulse, Y_Dir, Y_Stop_High, 1, Y_Steps)
    else:
        __move__(Y_Pulse, Y_Dir, Y_Stop_Low, 0, abs(Y_Steps))
    if Z_Steps < 0:
        __move__(Z_Pulse, Z_Dir, Z_Stop_Low, 0, abs(Z_Steps))
    return to_loc

#Visit each plant and check to see if it needs to be watered
def Water_Main(plants, loc, check):
    for plant in plants:
        loc = Move(loc, plant.location)
        if (check or check_if_dry()): water()
    Move(loc, HOME)
    return HOME

def Plant_Seed(current_loc, destination):
    loc = Location(current_loc.x, current_loc.y, 10)
    Move(current_loc, loc)
    Move(loc, destination)
    #plant the seed
    Planter_Dir.on()
    for x in range(0,50):
        Planter_Pulse.on()
        sleep(DELAY)
        Planter_Pulse.off()
        sleep(DELAY)
    Planter_Dir.off()
    for x in range(0,50):
        Planter_Pulse.on()
        sleep(DELAY)
        Planter_Pulse.off()
        sleep(DELAY)
    Move(destination, HOME)
    return HOME
