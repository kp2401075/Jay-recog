import RPi.GPIO as GPIO

import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
#set pwm pin to pin 40, with cycle frequency in hertz
pwm=GPIO.PWM(40,50)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.setup(7,GPIO.OUT)
#GPIO.output(7,0)

lPos=0.75
rPos=2.75
mPos=1.75

msPerCycle=1000/50
######################### SERVO CONTROL SETUP CODE END #######################   



try:
		while True:
#GPIO.output(7,GPIO.input(11))
			
			###### Code goes here ###
			if(GPIO.input(12)== 1):
				## OPENING THE LOCK
				dutyCyclePercentage= lPos*100/msPerCycle
				pwm.start(dutyCyclePercentage)
				## WAITING FOR 7 SECONDS
				time.sleep(5)
				## CLOSING THE LOCK
				dutyCyclePercentage= mPos*100/msPerCycle
				pwm.start(dutyCyclePercentage)
				time.sleep(1)
				
				
				

				#GPIO.output(7,1)
			#else:
				#GPIO.output(7,0)
			
except KeyboardInterrupt:
	pwm.stop()
	GPIO.cleanup()



########## SERVO SETUP WITHOUT LIBRARY IMPORT #########################
# libraries are already imported at the start of the program

# tell us which pins to use and what pin to set as output
#GPIO.setmode(GPIO.BOARD)


#duty cycles for specific duration
#figure out pulse times for the position you want

# list of directions to turn
#posList=[lPos,mPos,rPos,mPos]
#posList=[lPos,mPos]

#milliseconds in a cycle, calculated with hertz

