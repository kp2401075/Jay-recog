import glob
import os
import sys
import select
import cv2
import face
import io
import picamera
import numpy 
import config
POSITIVE_FILE_PREFIX = 'positive_'

##### CAPTURE IMAGE WITH PICAM
stream = io.BytesIO()

with picamera.PiCamera() as camera:
    camera.resolution = (92, 112)
    camera.capture(stream, format='jpeg')
    
    
#Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#Now creates an OpenCV image
image = cv2.imdecode(buff, 1)    
    
#### CONVERT IMAGE TO GRAYSCALE
   
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    


#### DEFINING HAAR CASCADE TO FIND THE FACE
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')    



#### CHEKING FOR THE FACE AND LOCATING IT


faces = face_cascade.detectMultiScale(image, 1.1, 5)

count = 0


if not os.path.exists(config.POSITIVE_DIR):
		os.makedirs(config.POSITIVE_DIR)
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, 
	POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
	
if len(files) > 0:
	# Grab the count from the last filename.
	count = int(files[-1][-7:-4])+1

filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
cv2.imwrite(filename, image)
print 'Found face and wrote training image', filename
count += 1

