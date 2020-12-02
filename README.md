# S20-61-CNCS
Python code for our senior design project: a CNC planter box.

StepperMotorDemo uses the Rpi.GPIO library to move X, Y, and Z axis stepper motors back and forth without further user control to test and demonstrate motor control.
Main Code contains the fully functional code that still relies on command line input instead of wireless communication. S2061CNCS.py runs the high level functions, while CNCS_Test allows individual control of each axis and output channel.
Server contains the final working code for the prject. plant-server.py manages the high level connection details using the plantlib.py functions, which then call functions from CNCS_Support.py to control the hardware.
