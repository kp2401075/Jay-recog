#/bin/bash/python
import cv2
#import os
import sys
#import glob
import numpy as np
import config






FACE_WIDTH  = 184
FACE_HEIGHT = 224


HAAR_FACES         = 'haarcascade_frontalface_alt.xml'
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)




# Get user supplied values

#importing or defining haarcascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


# will have to find a way to change the camera for raspberry pi setup
#fourcc = cv2.VideoWriter_fourcc('XVID')
#out = cv2.VideoWriter('~Desktop/output.avi',fourcc, 20.0, (640,480))


def detect_single(image):
	"""Return bounds (x, y, width, height) of detected face in grayscale image.
	   If no face or more than one face are detected, None is returned.
	"""
	faces = face_cascade.detectMultiScale(image, 
				scaleFactor=HAAR_SCALE_FACTOR, 
				minNeighbors=HAAR_MIN_NEIGHBORS, 
				minSize=HAAR_MIN_SIZE, 
				flags=cv2.CASCADE_SCALE_IMAGE)
	if len(faces) != 1:
		return None
	return faces[0]


def bright(image):
	alpha = 5
	beta = 15


	result = cv2.addWeighted(image,alpha,np.zeros(image.shape,image.dtype),0,beta)
	return result

def crop(image, x, y, w, h):
	"""Crop box defined by x, y (upper left corner) and w, h (width and height)
	to an image with the same aspect ratio as the face training data.  Might
	return a smaller crop if the box is near the edge of the image.
	"""
	crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
	midy = y + h/2
	y1 = max(0, midy-crop_height/2)
	y2 = min(image.shape[0]-1, midy+crop_height/2)
	return image[y1:y2, x:x+w]

def resize(image):
	"""Resize a face image to the proper size for training and detection.
	"""
	return cv2.resize(image, 
					  (config.FACE_WIDTH, config.FACE_HEIGHT), 
					  interpolation=cv2.INTER_LANCZOS4)
