from time import time

import CNCS_Support as CNCS


#This is the location to return to when not operating.
HOME = CNCS.Location(0,0,20)
#Stores the current location of the planter head in inches.
Location = CNCS.Location().update(HOME)
plants = []
#The program waits this many seconds between watering the plants.
WATER_DELAY = 20
WATER_NEXT = time() + WATER_DELAY


#Visit each plant and check to see if it needs to be watered.
def Water_Main():
    if plants:
        for plant in plants:
            global Location
            Location = CNCS.Move(Location, plant.location)
            if CNCS.check_if_dry(): CNCS.water()
        Location = CNCS.Move(HOME)
    else: print("There are currently no plants to water.")


def main():
    #if gpio.read(UI_enable): UI_Main_Loop()
    
    print("In main function")
    global WATER_NEXT
    if (time() >= WATER_NEXT):
        Water_Main()
        WATER_NEXT = time() + WATER_DELAY
    else: print("No need to water right now.")


#This loop is a simple text-based UI for testing purposes only.
loop = 1
while loop:
    plants.append(CNCS.Plant(
        int(input("Enter plant x location: ")),
        int(input("Enter plant y location: ")),1))
    CNCS.Plant_Seed(Location, plants[-1].location)
    print("Plant added at ({0}, {1}).".format(
        plants[-1].location.x, plants[-1].location.y))
    plants.sort(key=CNCS.Plant.getx)
    if input("enter X to exit main loop ") == "X": loop = 0
    main()
