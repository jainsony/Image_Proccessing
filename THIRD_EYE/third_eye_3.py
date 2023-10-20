# importing the module
import cv2
import math
import numpy as np
import time


#Variables
destination_x =0
destination_y =0
Red_Robot_x =0
Red_Robot_y =0

Twist = [0, 0]

cap = cv2.VideoCapture(1)

#4 control robot (kinematics)
def control_loop():
    global Red_Robot_x
    global Red_Robot_y
    global destination_x
    global destination_y

    global Twist

    dist_x = destination_x - Red_Robot_x     # destination_x - Red_Robot_x       
    dist_y = destination_y - Red_Robot_y     # destination_y - Red_Robot_y
    distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)

    while distance > 200:
        dist_x = destination_x - Red_Robot_x     # destination_x - Red_Robot_x       
        dist_y = destination_y - Red_Robot_y     # destination_y - Red_Robot_y
        distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
        if distance > 1:      # Distance_Error_control
            # position
            Twist[0] = 2*distance #param
            # orientation
            goal_theta = math.atan2(dist_y, dist_x)
            diff = goal_theta - Twist[1]        #Alert###

            if diff > math.pi:
                diff -= 2*math.pi #param
            elif diff < -math.pi:
                diff += 2*math.pi #param

            Twist[1] = 6*diff  #param
            print("in control loop")
            print(Twist)
            # serial_control(Twist)
            # success, img = vidcap.read()
            Red_Robot_x, Red_Robot_y = detect_robot(img)
            # cv2.imshow('in control loop', img)
            time.sleep(0.5)

        else:
            # target reached!
            Twist[0] = 0.0
            Twist[1] = 0.0
            break
            # self.call_catch_turtle_server(self.turtle_to_catch_.name)
            # self.turtle_to_catch_ = None


#3 detect robot
def detect_robot():
    detected_x=0
    detected_y=0

    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
        
    red_lower = np.array([0, 100, 184], np.uint8) 
    red_upper = np.array([255, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

    kernel = np.ones((5, 5), "uint8") 

    # For red color 
    red_mask = cv2.dilate(red_mask, kernel) 
    res_red = cv2.bitwise_and(img, img, mask = red_mask) 
    # cv2.imshow('mask', res_red)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 3000): 
            x, y, w, h = cv2.boundingRect(contour) 
            cv2.putText(img, "Robot detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), thickness=2)	
            
            detected_x = x+(w//2)
            detected_y = y+(h//2)
            cv2.circle(img=img, center=(detected_x, detected_y), radius=3, color=(0, 255, 0), thickness=5)
        
    return detected_x, detected_y

#2 Update frame
def Update_frame(): # only updates static frame with destination_x, destination_y, Red_Robot_x, Red_Robot_y coordinates and path
    global Red_Robot_x
    global Red_Robot_y
    global destination_x
    global destination_y

    Red_Robot_x, Red_Robot_y = detect_robot()
    cv2.putText(img, str(destination_x) + ',' +str(destination_y), (destination_x,destination_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    start_point = (Red_Robot_x, Red_Robot_y)
    end_point = (destination_x, destination_y)
    print("in update_frame")
    print(Red_Robot_x, ' ', Red_Robot_y)
    print(destination_x, ' ', destination_y)
    color = (0, 255, 0)
    thickness = 3
    cv2.line(img, start_point, end_point, color, thickness)
    # cv2.imshow('in main frame', frame)


#1 click event
def click_event(event, x, y, flags, params):
    global destination_x
    global destination_y

    if event==cv2.EVENT_RBUTTONDOWN:
        destination_x=x
        destination_y=y


# ret, frame = cap.read()
# run_once()
while True:
    ret, img = cap.read()
    # Red_Robot_x, Red_Robot_y = detect_robot()
    Update_frame()
    cv2.imshow('img', img)
    # cv2.imshow('frame', frame)
    cv2.setMouseCallback('img', click_event)


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindow()

















# def run_once():
#     global Red_Robot_x
#     global Red_Robot_y   

#     Red_Robot_x, Red_Robot_y = detect_robot()
#     cv2.setMouseCallback('image', click_event)
#     if(Red_Robot_x !=0 and Red_Robot_y !=0):
#         cv2.imshow('frame', frame)
#         cv2.waitKey(0)
