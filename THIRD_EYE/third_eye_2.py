# importing the module
import cv2
import math
import numpy as np
import time

Lx1=0
Ly1=0

Rx1=0
Ry1=0

# Rx=0
# Ry=0

destination_x =0
destination_y =0

Red_Robot_x =0
Red_Robot_y =0

edge_counter=0
counter = 0 # fior counting the left and right click instant
Twist = [0, 0] # linear_x, angular_z



vidcap = cv2.VideoCapture(1)
success, img = vidcap.read()
# displaying the image
cv2.imshow('image', img)
# setting mouse handler for the image
# and calling the click_event() function

# counter = 0
# if counter == 0:
# 	cv2.setMouseCallback('image', click_event)
# 	# Rx, Ry = detect_robot(img)
# 	counter = counter+1
# else:    
# 	cv2.setMouseCallback('image', click_event)
	
#Serial_control
def serial_control(Twist):
	count = 1

#Control_Robot
def control_loop():
	global destination_x
	global destination_y
	global Red_Robot_x
	global Red_Robot_y

	dist_x = destination_x - Red_Robot_x     # destination_x - Red_Robot_x       
	dist_y = destination_y - Red_Robot_y     # destination_y - Red_Robot_y
	distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)

	while distance > 1:
		dist_x = destination_x - Red_Robot_x     # destination_x - Red_Robot_x       
		dist_y = destination_y - Red_Robot_y     # destination_y - Red_Robot_y
		distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
		if distance > 1:      # Distance_Error_control
			# position
			Twist[0] = 2*distance
			# orientation
			goal_theta = math.atan2(dist_y, dist_x)
			diff = goal_theta - Twist[1]        #Alert###

			if diff > math.pi:
				diff -= 2*math.pi
			elif diff < -math.pi:
				diff += 2*math.pi

			Twist[1] = 6*diff
			print(Twist)
			serial_control(Twist)
			# success, img1 = vidcap.read()
			Red_Robot_x, Red_Robot_y = detect_robot()
			cv2.imshow('in control loop', img)
			time.sleep(1)

		else:
			# target reached!
			Twist[0] = 0.0
			Twist[1] = 0.0
			break
			# self.call_catch_turtle_server(self.turtle_to_catch_.name)
			# self.turtle_to_catch_ = None



#Main_Frame
def detect_robot():
	# pass
	global img

	global Lx1
	global Ly1
	global Rx1
	global Ry1
	success, imageFrame = vidcap.read()

	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

	red_lower = np.array([0, 100, 184], np.uint8) 
	red_upper = np.array([255, 255, 255], np.uint8) 
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

	kernel = np.ones((5, 5), "uint8") 
	
	# For red color 
	red_mask = cv2.dilate(red_mask, kernel) 
	res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask) 
	contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
	
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		if(area > 2500): 
			x, y, w, h = cv2.boundingRect(contour) 
			cv2.putText(imageFrame, "Robot detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), thickness=2)	 
			x = x+(w//2)
			y = y+(h//2)
			Rx = x
			Ry = y
			cv2.circle(img=imageFrame, center=(x, y), radius=3, color=(0, 255, 0), thickness=5)
			# img = imageFrame
			cv2.putText(img, str(Rx) + ',' +	str(Ry), (Rx,Ry), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			start_point = (Lx1, Ly1)
			end_point = (Rx, Ry)
			img = cv2.line(img, start_point, end_point, (0, 255, 0), 3)
			cv2.imshow('in main frame', img)
			print("detecting robot")
			return Rx, Ry
# function to display the coordinates of
# of the points clicked on the image

def click_event(event, x, y, flags, params):
	global Lx1
	global Ly1
	global Rx1
	global Ry1
	global edge_counter

	global destination_x
	global destination_y
	global Red_Robot_x
	global Red_Robot_y

	global counter
	
	vir_comment = 0
	############################################################ Robot Tracking -----OR----- checking for left mouse clicks 
	if vir_comment == 0 and counter == 0:
		if event == cv2.EVENT_LBUTTONDOWN:
			edge_counter = 0
			# Lx1=Rx
			# Ly1=Ry
			Lx1, Ly1 = detect_robot()
			# displaying the coordinates
			# on the Shell
			print(Lx1, ' ', Ly1)

			Red_Robot_x = Lx1
			Red_Robot_y = Ly1

			font = cv2.FONT_HERSHEY_SIMPLEX
			# cv2.putText(img, str(Lx1) + ',' +	str(Ly1), (Lx1,Ly1), font, 1, (255, 0, 0), 2)
			# cv2.imshow('image', img)
	
	############################################################# checking for right mouse clicks	
		if event==cv2.EVENT_RBUTTONDOWN:
			Rx1=x
			Ry1=y
			# cv2.putText(img, str(Rx1) + ',' +	str(Ry1), (Rx1,Ry1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			# start_point = (Lx1, Ly1)
			# end_point = (Rx1, Ry1)
			# print(Lx1, ' ', Ly1)
			# print(Rx1, ' ', Ry1)
			# color = (0, 255, 0)
			# thickness = 3
			# img = cv2.line(img, start_point, end_point, color, thickness)
			# dist = math.dist(start_point, end_point)
			# print("distance = "+str(dist))
			# cv2.imshow('image', img)
			destination_x = Rx1
			destination_y = Ry1
			control_loop()
			counter = counter + 1
			# time.sleep(2)



cv2.setMouseCallback('image', click_event)
# driver function
# if __name__=="__main__":
	# reading the image
	# img = cv2.imread('black.png', 1)
	# Capture video frame by frame
	# vidcap = cv2.VideoCapture(1)
	# success, img = vidcap.read()
	# # displaying the image
	# cv2.imshow('image', img)
	# # setting mouse handler for the image
	# # and calling the click_event() function

	# counter = 0
	# if counter == 0:
	# 	cv2.setMouseCallback('image', click_event)
	# 	# Rx, Ry = detect_robot(img)
	# 	counter = counter+1
	# else:    
	# 	cv2.setMouseCallback('image', click_event)
	# wait for a key to be pressed to exit
cv2.waitKey(0)
# close the window
cv2.destroyAllWindows()
