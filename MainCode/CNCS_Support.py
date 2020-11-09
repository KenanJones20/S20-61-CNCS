import gpiozero as zero
from time import sleep

DELAY = 0.001  #Pulse duration in seconds.
#The number of steps each stepper motor axis moves per inch
X_Constant = 100
Y_Constant = 100
Z_Constant = 100

X_Dir = zero.LED(19)
X_Pulse = zero.LED(22)
Y_Dir = zero.LED(21)
Y_Pulse = zero(24)
Z_Dir = zero.LED(23)
Z_Pulse = zero.LED(26)
Planter_Dir = zero.LED(10)
Planter_Pulse = zero.LED(12)
Planter_Solenoid = zero.LED(16)
Water_Solenoid = zero.LED(7)
SDA = 3
SCL = 5
X_Stop_Low = zero.Button(31)
X_Stop_High = zero.Button(33)
Y_Stop_Low = zero.Button(35)
Y_Stop_High = zero.Button(37)
Z_Stop_Low = zero.Button(36)
Z_Stop_High = zero.Button(38)

def check_if_dry():
    #Use I2C to get water sensor value.
    #Return value < Water_Constant.
    return 1

def water():
    Water_Solenoid.on()
    print("watering plant")
    sleep(0.5)
    Water_Solenoid.off()
    return None

#Sets direc_channel to value and pulses pulse_channel
#steps times unless end_stop is pressed.
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

#   Moves up if needed, then across X and Y, then down if needed.
def Move(from_loc, to_loc):
    #Find the number of steps to move each axis.
    X_Steps = (to_loc.x-from_loc.x)*X_Constant
    Y_Steps = (to_loc.y-from_loc.y)*Y_Constant
    Z_Steps = (to_loc.z-from_loc.z)*Z_Constant
    print("(X steps, Y steps) = ({1}, {1})".format(
        str(X_Steps),str(Y_Steps)))

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

# Moves the planter head up, then across and down to plant the seed.
def Plant_Seed(current_loc, destination):
    loc = Location(0,0,0).update(current_loc)
    Move(current_loc, loc.update(loc.x, loc.y, 20))
    Move(loc, destination)
    #plant the seed
    for x in range(0,20):
        Planter_Pulse.on()
        sleep(DELAY)
        Planter_Pulse.off()
        sleep(DELAY)
    return destination

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
