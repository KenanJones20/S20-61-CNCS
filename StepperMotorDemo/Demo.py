import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

#GPIO pin names
X_Axis_Dir = 18
Y_Axis_Dir = 23
Z_Axis_Dir = 8
Planter_Dir = 10

#GPIO pin definitions
GPIO.setup(17, GPIO.OUT)
X_Axis_PWM = GPIO.PWM(17,1000)
GPIO.setup(22, GPIO.OUT)
Y_Axis_PWM = GPIO.PWM(22,1000)
GPIO.setup(7, GPIO.OUT)
Z_Axis_PWM = GPIO.PWM(7,1000)
GPIO.setup(9, GPIO.OUT)
Planter_PWM = GPIO.PWM(9,1000)
GPIO.setup((X_Axis_Dir,Y_Axis_Dir,Z_Axis_Dir,Planter_Dir),
           GPIO.OUT, initial = GPIO.LOW)

#move X axis stepper motors
X_Axis_PWM.start(50)
sleep(1)
X_Axis_PWM.stop()

#move Y axis stepper motor
Y_Axis_PWM.start(50)
sleep(1)
Y_Axis_PWM.stop()

#move Z axis stepper motor
Z_Axis_PWM.start(50)
sleep(1)
Z_Axis_PWM.stop()

#move planter stepper motor
Planter_PWM.start(50)
sleep(1)
Planter_PWM.stop()

#move all the motors backward
GPIO.output((X_Axis_Dir,Y_Axis_Dir,Z_Axis_Dir,Planter_Dir), GPIO.HIGH)
X_Axis_PWM.start(50)
Y_Axis_PWM.start(50)
Z_Axis_PWM.start(50)
Planter_PWM.start(50)
sleep(1)
X_Axis_PWM.stop()
Y_Axis_PWM.stop()
Z_Axis_PWM.stop()
Planter_PWM.stop()

GPIO.cleanup()