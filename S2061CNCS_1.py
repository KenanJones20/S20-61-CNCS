import CNCS_Support_1 as CNCS

# global variables
HOME = CNCS.Location(0, 0, 20)  # home location to return to when not operating
location = CNCS.Location().update(HOME)  # the current location of the planter head, in inches
plant_loc = []
num_rows = 9
num_plants = 9
x_start = 0
y_start = 0
z_start = 0
d_rows = 3  # the distance between rows required for plants to grow properly
d_plants = 3  # distance between plants in row for them to grow properly
water_delay = 1 # time to wait before watering plants again

# Initialize the location list
for j in range(0, num_rows):
    for k in range(0, num_plants):
        plant_loc.append(CNCS.Location(x_start+d_rows*j, y_start+d_plants*k, z_start, 0))


# Visit each plant and check to see if it needs to be watered
def water_main():
    for i in range(len(plant_loc)):
        if plant_loc[i].p:
            CNCS.move(location, plant_loc[i])
            if CNCS.check_if_dry():
                CNCS.water()


# move to the next open spot and plant a plant
def plant_main():
    for i in range(len(plant_loc)):
        if plant_loc[i].p == 0:
            CNCS.move(location, plant_loc[i])
            # plant a plant
            plant_loc[i].p = 1
            CNCS.move(location, HOME)
            break
        if i == len(plant_loc) - 1:
            CNCS.move(location, HOME)


timer = time()
loop = 1
while loop:
    # two buttons, one to water and one to plant new plants
    if (time() > timer + water_delay):
        water_main()
        timer = time()
    CNCS.button_plant.when_pressed = plant_main

CNCS.GPIO.cleanup()
