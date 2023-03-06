import cv2								#open cv library for python
import numpy as np							#numpy library 

cap = cv2.VideoCapture(0)						#initialise the default camera
template = cv2.imread("template.jpg", cv2.IMREAD_GRAYSCALE)		#load the template image for detection
w, h = template.shape[::-1]						#get the width and height of the template image
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   			#get width of the live image feed, integer
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))			#get height of the live image feed, integer

while True:
	#print(width//2, height//2)
	_, frame = cap.read()						#read the live stream
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		#conersion to grayscale for template matching

	res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)	#opencv template matching
	loc = np.where(res >= 0.6)					#identify location of matched template in live feed			
	i=0
	for pt in zip(*loc[::-1]):
		i = i+1;
		print(pt[0] + w//2, pt[1] + h//2)
		cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3) #boundary around the location of matched template
		cv2.circle(frame, (pt[0] + w//2, pt[1] + h//2), 7, (255, 255, 255), -1)	#center point of the matched template
	cv2.circle(frame, (width//2, height//2), 7, (255,255,0), -1)	#center point of the camera feed 
	cv2.imshow("Frame",frame)	#show the entire frame in a single window
	key = cv2.waitKey(1)		#capture the key pressed for input
	#print(key)
	if key == 32:			#if space is pressed,
		image = cap.read()	#capture current frame
		cv2.imwrite("template.png", image) # save image as template
	if  key == 27:			#if esc is pressed
		break			#end loop 

cap.release()				#close camera interface
cv2.destroyAllWindows()		#close all windows
