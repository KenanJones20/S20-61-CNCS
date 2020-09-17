
import CNCS_Support as CNCS

#global variables
HOME = CNCS.Location(0,0,20) #home location to return to when not operating
location = CNCS.Location().update(HOME) #the current location of the planter head, in inches
plants = [] #list of all the plants

#Visit each plant and check to see if it needs to be watered
def Water_Main():
    for plant in plants:
        global location
        location = CNCS.Move(location, plant.location)
        if CNCS.check_if_dry(): CNCS.water()

def main():
    #if gpio.read(UI_enable): UI_Main_Loop()
    #if time()>Water_Next: Water_Main()
    
    print("In main function")

#this loop is a simple text-based UI for testing purposes only
loop = 1
while loop:
    plants.append(CNCS.Plant(
        int(input("Enter plant x location: ")),
        int(input("Enter plant y location: ")),1))
    print("Plant added at " + str(plants[-1].location.x)
          + ", " + str(plants[-1].location.y))
    if input("enter X to exit main loop ") == "X":
        loop = 0
        plants.sort(key=CNCS.Plant.getx)
    else: main()
    Water_Main()
CNCS.GPIO.cleanup()
