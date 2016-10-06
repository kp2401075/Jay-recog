#!/usr/bin/env python
####### IMPORTING LIBS
import cv2
import config
import face
import io
import picamera
import numpy 
#for accessing the GPIO pins
import RPi.GPIO as GPIO
#used for time delays
import time as tm
import crop ## crop library (autocropping)
import os
import glob
import sys
import select
from datetime import datetime,time

POSITIVE_FILE_PREFIX = 'unauthorised_'
now = datetime.now()
now_time = now.time()

# the starting and ending time range
startHour = 9
startMin = 30
endHour = 23
endMin = 30

# function which returns true if current time is in the range, else return false
def withinRange():  #{
    if time(startHour, startMin) <= now.time() <= time(endHour, endMin):
        return True
    else:
        return False
#}

# check if current time is within the range and do something
if withinRange():
    print "within range"
else:
    print "Not within time range Program will now exit"
    exit()


##### LOADING TRAINED RECOGNIZING DATABASE #####

### this step takes little too much time but there is no alternative way to it
POSITIVE_THRESHOLD = 2700
	# File to save and load face recognizer model.
TRAINING_FILE = 'training.xml'
model = cv2.createEigenFaceRecognizer()
model.load(TRAINING_FILE)
print 'Molel Loaded'

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(40, GPIO.OUT)
##set pwm pin to pin 40, with cycle frequency in hertz
#pwm=GPIO.PWM(40,50)

	
	#### VARIABLE DEFINITIONS
	
	# POTIVE ID THREADHOLD LOWER IS BETTER RECOGNITION.

	
	# Value for positive and negative labels passed to face recognition model.
	# Can be any integer values, but must be unique from each other.
	# You shouldn't have to change these values.
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2
	# libraries are already imported at the start of the program
				
	# tell us which pins to use and what pin to set as output
	#GPIO.setmode(GPIO.BOARD)
	
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
	
	



try:
		while True:
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.setup(40, GPIO.OUT)
#set pwm pin to pin 40, with cycle frequency in hertz
			pwm=GPIO.PWM(40,50)
			
			if(GPIO.input(11) == 1):
				
					
				
				#### TO SAVE IMAGE FILE WITHOUT WRITING ACTUAL FILE ####
				stream = io.BytesIO()
				
				
				#### TO TAKE PICTURE WITH PI CAM
				with picamera.PiCamera() as camera:
				    camera.resolution = config.CAM_RES #900,900 works optimally
				    camera.capture(stream, format='jpeg')
				 
				####Convert the picture into a numpy array
				buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
					
				
				####Now creates an OpenCV image
				image = cv2.imdecode(buff, 1)    
				
								    
				#### CONVERT IMAGE TO GRAYSCALE
				   
				image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
				#cv2.imshow('image',image) 
				
				image = crop.bright(image)
				
				faces = crop.detect_single(image) # passinng captured image through face detection
				
				if(faces == None ):
					print 'no face detected try again'
					continue
			
					
				cr = crop.crop(image,faces[0],faces[1],faces[2],faces[3]) # cropping the image to the size of face
				
				cr = crop.resize(cr) # resizing image for recognition
				#cv2.imshow('cropped',image)
				
				
				
				
				#### recognition
				label, confidence = model.predict(cr)
				
							
				
				################### SERVO SETUP WITHOUT LIBRARY IMPORT #########################
				
				
				
				#### DECIDING THE RESULT FROM THRESHOLD VALUE
				
				##### LOWER THE THRESHOLD BETTER THE RECOGNITION
				  ### HAVE SET VERY HIGH THREASHOLD FOR NOW AS THIS IS IN ALPHA STAGES
				  ### AND IT IS EASY TO WORK ON THE SERVO WITH HIGH THRESHOLD
				
				print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
					'POSITIVE' if label == POSITIVE_LABEL else 'NEGATIVE', 
									confidence)
				if label == POSITIVE_LABEL and confidence < POSITIVE_THRESHOLD:
					#### PRINT RECOGNISED FACE AND OPEN THE LOCK (TUERN THE SERVO)
					
					print 'Recognized face!'
					# OPENING THE LOCK
					dutyCyclePercentage= lPos*100/msPerCycle
					pwm.start(dutyCyclePercentage)
					## WAITING FOR 7 SECONDS
					tm.sleep(2)
					## CLOSING THE LOCK
					dutyCyclePercentage= mPos*100/msPerCycle
					pwm.start(dutyCyclePercentage)
					tm.sleep(1)
					pwm.stop()
					GPIO.cleanup()
				
					
				else:
					print 'Did not recognize face! '
					count = 0


					if not os.path.exists(config.SAVE_DIR):
							os.makedirs(config.SAVE_DIR)
						# Find the largest ID of existing positive images.
						# Start new images after this ID value.
					files = sorted(glob.glob(os.path.join(config.SAVE_DIR, 
						POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
						
					if len(files) > 0:
						# Grab the count from the last filename.
						count = int(files[-1][-7:-4])+1
					
					filename = os.path.join(config.SAVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
					cv2.imwrite(filename, image)
					print 'Found face and wrote training image', filename
					count += 1

					


				
except KeyboardInterrupt:
	pwm.stop()
	GPIO.cleanup()
				
