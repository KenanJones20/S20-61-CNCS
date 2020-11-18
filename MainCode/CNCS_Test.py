import gpiozero as zero
from time import sleep

DELAY = 0.001  #Pulse duration in seconds
#The number of steps each stepper motor moves per inch
X_Constant = 21
Y_Constant = 500
Z_Constant = 500

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
SDA = 2
SCL = 3
X_Stop_Low = zero.Button(6)
X_Stop_High = zero.Button(13)
Y_Stop_Low = zero.Button(19)
Y_Stop_High = zero.Button(26)
Z_Stop_Low = zero.Button(16)
Z_Stop_High = zero.Button(20)

def check_if_dry():
    return 1

def water():
    Water_Solenoid.on()
    print("watering plant")
    sleep(0.5)
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
    print("Moving")
    #print("(X steps, Y steps) = ({0}, {1})".format(str(X_Steps),str(Y_Steps)))

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

def Plant_Seed(current_loc, destination):
    loc = Location().update(current_loc.x, current_loc.y, 20)
    Move(current_loc, loc)
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
        self.location = Location(x_loc, Y_loc)
        self.size = size

    def getx(self):
        return self.location.x

while 1:
    str = input("enter direction: u, d, l, r, f, b and distance to move: ").partition(" ")
    dir = str[0].lower()
    distance = int(str[2])
    if dir == "u":
        Move(Location(), Location(z=distance))
    elif dir == "d":
        Move(Location(z=distance), Location())
    elif dir == "l":
        Move(Location(), Location(y=distance))
    elif dir == "r":
        Move(Location(y=distance), Location())
    elif dir == "f":
        Move(Location(), Location(x=distance))
    elif dir == "b":
        Move(Location(x=distance), Location())
    elif dir == "w":
        water()
    elif dir == "p":
        Plant_Seed(Location(), Location(x=distance))
    elif dir == "x":
        break
    else: print("invalid command")