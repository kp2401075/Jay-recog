#!/usr/bin/env python


#for accessing the GPIO pins
import RPi.GPIO as GPIO
#used for time delays
import time

########## SERVO SETUP WITHOUT LIBRARY IMPORT #########################
# libraries are already imported at the start of the program

# tell us which pins to use and what pin to set as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
#set pwm pin to pin 40, with cycle frequency in hertz
pwm=GPIO.PWM(40,50)

#duty cycles for specific duration
#figure out pulse times for the position you want
lPos=0.75
rPos=2.75
mPos=1.75

# list of directions to turn
#posList=[lPos,mPos,rPos,mPos]
#posList=[lPos,mPos]

#milliseconds in a cycle, calculated with hertz
msPerCycle=1000/50
######################### SERVO CONTROL SETUP CODE END #######################   


## OPENING THE LOCK
dutyCyclePercentage= lPos*100/msPerCycle
pwm.start(dutyCyclePercentage)
## WAITING FOR 7 SECONDS
time.sleep(7)
## CLOSING THE LOCK
dutyCyclePercentage= mPos*100/msPerCycle
pwm.start(dutyCyclePercentage)
time.sleep(1)
pwm.stop()
GPIO.cleanup()
