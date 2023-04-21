import cv2								#open cv library for python
import numpy as np							#numpy library 

ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(3)
ser.reset_input_buffer()
print ("Serial OK")


cap = cv2.VideoCapture(0)						#initialise the default camera
template = cv2.imread("template.jpg", cv2.IMREAD_GRAYSCALE)		#load the template image for detection
w, h = template.shape[::-1]						#get the width and height of the template image
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   			#get width of the live image feed, integer
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))			#get height of the live image feed, integer


object_points = np.array([						#define the real world dimensions of the object to be detected
    [0, 0, 0],  # Bottom-left corner (x1, y1, z1)			#origin
    [0.055, 0, 0], # Bottom-right corner (x2, y2, z2)		#all units considered in metre
    [0.055, 0.07, 0], # Top-right corner (x3, y3, z3)
    [0, 0.07, 0]   # Top-left corner (x4, y4, z4)
], dtype=np.float32)

camera_matrix = np.array([						#camera matrix obtained from calibration
	[606.559382, 0.000000, 310.204595],
	[0.000000, 604.758576, 261.755160],
	[0.000000, 0.000000, 1.000000]
], dtype=np.float32)

distortion_coefficients = (-0.319684, 0.480112, 0.022131, -0.006103, 0.000000)	#distrortion parameters obtained from calibration

while True:
	#print(width//2, height//2)
	_, frame = cap.read()						#read the live stream
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		#conersion to grayscale for template matching

	res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)	#opencv template matching
	#print(res)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)		#obtaining detected area bounding box points
	top_left = max_loc
	bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
	image_points = np.array([top_left, (bottom_right[0], top_left[1]), (top_left[0], bottom_right[1]), bottom_right], dtype=np.float32)
	loc = np.where(res >= 0.6)				#identify location of matched template in live feed			
	i=0
	
	try:
		x_px = round(sum(loc[0])/len(loc[0]))
		y_px = round(sum(loc[1])/len(loc[1]))
		#print(x_px, y_px)
		if len(res) >= 4:
			ret, rotation_vector, translation_vector = cv2.solvePnP(object_points, image_points, camera_matrix, distortion_coefficients)					#opencv function to obtain the rotation and translation vectors based on detected object
		if ret:
			cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)		#plot bounding box in live image
			#print(rotation_vector, translation_vector)
			for pt in zip(*loc[::-1]):
				i = i+1;
			cv2.circle(frame, (pt[0] + w//2, pt[1] + h//2), 7, (255, 255, 255), -1)	#center point of the matched template
			cv2.circle(frame, (width//2, height//2), 7, (255,255,0), -1)	#center point of the camera feed
			
			#rotation_vector = np.array(rotation_vector)
			#translation_vector = np.array(translation_vector)
			#theta = np.linalg.norm(rotation_vector)
			#if theta != 0 :
    				#k = rotation_vector / theta;
    				#K = np.array([[0, -k[2], k[1]],
                  		#		[k[2], 0, -k[0]],
                  		#		[-k[1], k[0], 0]])
    				#R = np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*K@K
			#else:
    			#	R = np.eye(3)

		# Combine the rotation matrix with the translation vector to obtain a homogeneous transformation matrix
		#T = np.vstack((np.hstack((R, translation_vector.reshape(-1, 1))), np.array([0, 0, 0, 1])))

		# Multiply the homogeneous transformation matrix with the homogeneous coordinates of the end effector to obtain the 3D position of the end effector
		#end_effector_pos = T @ np.array([0, 0, 0, 1]).reshape(-1, 1)
		#print(end_effector_pos)
		L1 = 0.11						#Length of arm 1
		L2 = 0.1						#Length of arm 2
		#print(translation_vector)
		d_x, d_y, d_z = translation_vector			#Initialise translation vectors
		
		##Start of Inverse Kinematics Implemented from Matlab
		d = np.sqrt(d_x**2, d_y**2)				
		theta1 = np.arctan2(d_y, d_x)	
		dwc = np.sqrt(d**2 - L2**2)
		alpha = np.arctan2(L2, d)
		beta1 = np.arccos((dwc**2 + L1**2 - L2**2)/(2*dwc*L1))
		beta2 = np.arccos((L1**2 + L2**2 - dwc**2)/(2*L1*L2))
		theta2 = alpha - beta1
		#print(theta1, theta2)
		theta1 = np.rad2deg(theta1)
		theta2 = np.rad2deg(theta2)
		print(theta1, theta2)
		##End of Inverse Kinematics ##
		
		##Identify center of the bounding box##
		x, y = loc[1][0], loc[0][0]
        	w, h = template.shape[::-1]
		cx, cy = x + w // 2, y + h // 2
		
		##Find center of the camera frame##
        	frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
        	
        	##Check for difference in the center points. If more than 20 pixels, send the pan and tilt angle to arduino
        	if ((frame_center[0] - 20 <= cx <= frame_center[0] + 20) and (frame_center[1] - 20 <= cy <= frame_center[1] + 20)):
        		print("centered")
        	else:
           		# Send the pan and tilt angles to the arduino
            		ser.write(f'{pan},{tilt}\n'.encode())
	except(ZeroDivisionError):
		pass
	#for pt in zip(*loc[::-1]):
	#	i = i+1;
		
		#print(pt[0] + w//2, pt[1] + h//2)
	#	cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3) #boundary around the location of matched template
	#	cv2.circle(frame, (pt[0] + w//2, pt[1] + h//2), 7, (255, 255, 255), -1)	#center point of the matched template
	#cv2.circle(frame, (width//2, height//2), 7, (255,255,0), -1)	#center point of the camera feed 
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
