# importing the module
import cv2
import math

x1=0
y1=0

x2=0
y2=0

edge_counter=0
# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
	global x1
	global y1
	global x2
	global y2
	global edge_counter
	
	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:
		edge_counter = 0
		x1=x
		y1=y
		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)

		# displaying the coordinates
		# on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img, str(x1) + ',' +	str(y1), (x1,y1), font, 1, (255, 0, 0), 2)
		cv2.imshow('image', img)

	############################################################ checking for right mouse clicks	
	if event==cv2.EVENT_RBUTTONDOWN:
		if edge_counter == 0:
			x2=x
			y2=y
			edge_counter = edge_counter+1
		else:
			x1=x2
			y1=y2
			x2=x
			y2=y

		# displaying the coordinates
		# on the Shell
		# print(x2, ' ', y2)

		# displaying the coordinates
		# on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		# b = img[y, x, 0]
		# g = img[y, x, 1]
		# r = img[y, x, 2]
		cv2.putText(img, str(x2) + ',' +	str(y2), (x2,y2), font, 1, (255, 0, 0), 2)
		#################### line
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
		cv2.imshow('image', img)
            

# driver function
if __name__=="__main__":

	# reading the image
	# img = cv2.imread('black.png', 1)
	vidcap = cv2.VideoCapture(1)
	# Capture video frame by frame

	success, img = vidcap.read()

	# displaying the image
	cv2.imshow('image', img)

	# setting mouse handler for the image
	# and calling the click_event() function
	counter = 0
	if counter == 0:
		cv2.setMouseCallback('image', click_event)
		counter = counter+1
	else:    
		cv2.setMouseCallback('image', click_event)

	# wait for a key to be pressed to exit
	cv2.waitKey(0)

	# close the window
	cv2.destroyAllWindows()
