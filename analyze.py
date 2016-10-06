


####### IMPORTING LIBS
import cv2
import config
import face
import face
import io
import picamera
import numpy 
#for accessing the GPIO pins
import RPi.GPIO as GPIO
#used for time delays
import time
import crop ## crop library (autocropping)



#### VARIABLE DEFINITIONS

# POTIVE ID THREADHOLD LOWER IS BETTER RECOGNITION.
POSITIVE_THRESHOLD = 2
500
# File to save and load face recognizer model.
TRAINING_FILE = 'training.xml'

# Value for positive and negative labels passed to face recognition model.
# Can be any integer values, but must be unique from each other.
# You shouldn't have to change these values.
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2




###### BRANDING END#######



##### LOADING TRAINED RECOGNIZING DATABASE #####

### this step takes little too much time but there is no alternative way to it
model = cv2.createEigenFaceRecognizer()
model.load(TRAINING_FILE)



#### TO SAVE IMAGE FILE WITHOUT WRITING ACTUAL FILE ####
stream = io.BytesIO()


#### TO TAKE PICTURE WITH PI CAM
with picamera.PiCamera() as camera:
    camera.resolution = (1920,1080)
    camera.capture(stream, format='jpeg')


    
    
####Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)



####Now creates an OpenCV image
image = cv2.imdecode(buff, 1)    



    
#### CONVERT IMAGE TO GRAYSCALE
   
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#cv2.imshow('image',image) 

faces = crop.detect_single(image) # passinng captured image through face detection


cr = crop.crop(image,faces[0],faces[1],faces[2],faces[3]) # cropping the image to the size of face

cr = crop.resize(cr) # resizing image for recognition


#### recognition
label, confidence = model.predict(cr)




################### SERVO SETUP WITHOUT LIBRARY IMPORT #########################
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
	## OPENING THE LOCK
	#dutyCyclePercentage= lPos*100/msPerCycle
	#pwm.start(dutyCyclePercentage)
	### WAITING FOR 7 SECONDS
	#time.sleep(7)
	### CLOSING THE LOCK
	#dutyCyclePercentage= mPos*100/msPerCycle
	#pwm.start(dutyCyclePercentage)
	#time.sleep(1)
	#pwm.stop()
	#GPIO.cleanup()

	
else:
	print 'Did not recognize face! '

