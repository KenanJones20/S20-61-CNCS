import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

FREQ = 500 #pwm frequency

#GPIO pin names
X_Axis_Dir = 10
Y_Axis_Dir = 9
Z_Axis_Dir = 11
Planter_Dir = 15

#GPIO pin definitions
GPIO.setup(25, GPIO.OUT)
X_Axis_PWM = GPIO.PWM(25,FREQ)
GPIO.setup(8, GPIO.OUT)
Y_Axis_PWM = GPIO.PWM(8,FREQ)
GPIO.setup(7, GPIO.OUT)
Z_Axis_PWM = GPIO.PWM(7,FREQ)
GPIO.setup(18, GPIO.OUT)
Planter_PWM = GPIO.PWM(18,FREQ)
GPIO.setup((X_Axis_Dir,Y_Axis_Dir,Z_Axis_Dir,Planter_Dir),
           GPIO.OUT, initial = GPIO.LOW)

#move X axis stepper motors
X_Axis_PWM.start(50)
sleep(2)
X_Axis_PWM.stop()

#move Y axis stepper motor
Y_Axis_PWM.start(50)
sleep(2)
Y_Axis_PWM.stop()

#move Z axis stepper motor
Z_Axis_PWM.start(50)
sleep(2)
Z_Axis_PWM.stop()

#move planter stepper motor
Planter_PWM.start(50)
sleep(2)
Planter_PWM.stop()

Sleep(1)

#move all the motors backward
GPIO.output((X_Axis_Dir,Y_Axis_Dir,Z_Axis_Dir,
             Planter_Dir), GPIO.HIGH)
X_Axis_PWM.ChangeFrequency(FREQ)
Y_Axis_PWM.ChangeFrequency(FREQ)
Z_Axis_PWM.ChangeFrequency(FREQ)
Planter_PWM.ChangeFrequency(FREQ)
X_Axis_PWM.start(50)
Y_Axis_PWM.start(50)
Z_Axis_PWM.start(50)
Planter_PWM.start(50)
sleep(3)
X_Axis_PWM.stop()
Y_Axis_PWM.stop()
Z_Axis_PWM.stop()
Planter_PWM.stop()

GPIO.cleanup()
