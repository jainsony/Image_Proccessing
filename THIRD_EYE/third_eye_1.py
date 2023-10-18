# importing the module
import cv2
import math
import numpy as np
import time

x1=0
y1=0

x2=0
y2=0

Rx=0
Ry=0

live_img1=0
live_img2=0

edge_counter=0

Twist = [0, 0] # linear_x, angular_z

#Serial_control
def serial_control(Twist):
	pass

#Control_Robot
def control_loop(destination_x, destination_y, Red_Robot_x, Red_Robot_y):

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
			# success, img = vidcap.read()
			Red_Robot_x, Red_Robot_y = get_main_frame(img)
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
def get_main_frame(imageFrame):
	# pass
	global Rx
	global Ry
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
			imageFrame = cv2.circle(img=imageFrame, center=(x, y), radius=3, color=(0, 255, 0), thickness=5)

			cv2.imshow('in main frame', imageFrame)
			return Rx, Ry
# function to display the coordinates of
# of the points clicked on the image

def click_event(event, x, y, flags, params):
	global x1
	global y1
	global x2
	global y2
	global edge_counter

	vir_comment = 0
	############################################################ Robot Tracking -----OR----- checking for left mouse clicks 
	if vir_comment == 0:
		if event == cv2.EVENT_LBUTTONDOWN:
			edge_counter = 0
			# x1=Rx
			# y1=Ry
			x1, y1 = get_main_frame(img)
			# displaying the coordinates
			# on the Shell
			print(x1, ' ', y1)

			# displaying the coordinates
			# on the image window
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(img, str(x1) + ',' +	str(y1), (x1,y1), font, 1, (255, 0, 0), 2)
			cv2.imshow('image', img)
	
	############################################################ checking for right mouse clicks	
		if event==cv2.EVENT_RBUTTONDOWN:
			x2=x
			y2=y
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(img, str(x2) + ',' +	str(y2), (x2,y2), font, 1, (255, 0, 0), 2)
			start_point = (x1, y1)
			# End coordinate, here (250, 250)
			# represents the bottom right corner of image
			end_point = (x2, y2)
			print(x1, ' ', y1)
			print(x2, ' ', y2)
			# Green color in BGR
			color = (0, 255, 0)
			# Line thickness of 9 px
			thickness = 3
			# Using cv2.line() method
			# Draw a diagonal green line with thickness of 9 px
			image = cv2.line(img, start_point, end_point, color, thickness)
			dist = math.dist(start_point, end_point)
			print("distance = "+str(dist))
			# cv2.imshow('image', img)
			control_loop(x2, y2, x1, y1)
			# time.sleep(2)



# driver function
if __name__=="__main__":
	# reading the image
	# img = cv2.imread('black.png', 1)
	# Capture video frame by frame
	vidcap = cv2.VideoCapture(1)
	success, img = vidcap.read()
	# displaying the image
	cv2.imshow('image', img)
	# setting mouse handler for the image
	# and calling the click_event() function

	counter = 0
	if counter == 0:
		cv2.setMouseCallback('image', click_event)
		# Rx, Ry = get_main_frame(img)
		counter = counter+1
	else:    
		cv2.setMouseCallback('image', click_event)
	# wait for a key to be pressed to exit
	cv2.waitKey(0)
	# close the window
	cv2.destroyAllWindows()
