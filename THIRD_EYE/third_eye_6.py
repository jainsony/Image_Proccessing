# importing the module
import cv2
import math
import numpy as np
import time
import serial


#Variables
debug = 0


destination_x =1
destination_y =1
Red_Robot_x =1
Red_Robot_y =1
distance = 1
third_side_angle = 0 

distance_error_factor = 10
Twist = [0, 0]

#error
theta_error = 0
prev_error = 0

control_string = ""
control_string += str(0)+"," + str(0) +","+ str(0) +"," + str(0) + "\n"
speed = 50
# ser = serial.Serial(port='COM7',baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

cap = cv2.VideoCapture(1)

def get_twist_angle():
    global theta_error

def send_serial(speed, dir):
    control_string = "<"+str(int(speed)) +","+ str(int(dir))  +","+str(0)  +","+str(0)+">"+"\n"
    # if debug == 1:
    print(control_string)
    # ser.write(str.encode(control_string))
    time.sleep(0.1)

def calculate_distance(x1, y1, x2, y2):
    dist_x = x1 - x2     # destination_x - Red_Robot_x       
    dist_y = y1 - y2     # destination_y - Red_Robot_y
    length = math.sqrt(dist_x * dist_x + dist_y * dist_y)
    # length = int(length/10) # 10 is factor here
    return length

def robo_info(situation, signal, angle):
    # print(situation + '\n ' + signal)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(int(situation)) + " || " + str(int(signal))+ " || " + str(angle), (10, 20), font, 0.7, (0, 0, 255), 2)

def Calculate_angle(a, b, c):
    try:
        # Check if the input values can form a triangle
        if a + b > c and a + c > b and b + c > a:
            # Calculate angle A
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            angle_A = math.degrees(math.acos(cos_A))
            
            # Calculate angle B
            cos_B = (c**2 + a**2 - b**2) / (2 * c * a)
            angle_B = math.degrees(math.acos(cos_B))
            
            # Calculate angle C (by the sum of angles in a triangle)
            angle_C = 180 - angle_A - angle_B
            
            return angle_A, angle_B, angle_C
        else:
            raise ValueError("Invalid side lengths. They cannot form a triangle.")
    except ValueError as e:
        return [0, 0, 0]

#4 control robot (kinematics)
def control_loop():
    global Red_Robot_x
    global Red_Robot_y
    global destination_x
    global destination_y
    global distance_error_factor
    global distance
    global Twist
    global theta_error

    distance = calculate_distance(destination_x, destination_y, Red_Robot_x, Red_Robot_y) # x1, y1, x2, y2
    distance = int(distance/10) # 10 is factor here

    # print("Distance: "+str(distance)+", Dist_X: "+str(dist_x) + ", Dist_Y: "+str(dist_y)+", Theta: "+ str(goal_theta))

    if distance > distance_error_factor:      # Distance_Error_control
        # position
        Twist[0] = 2*distance #param

        # orientation
        Twist[1] = get_twist_angle()
        
        Red_Robot_x, Red_Robot_y = detect_robot()
        
        # send command now 
        # send_serial(Twist[0], Twist[1])

        if debug == 1:    
            print("..........in control loop.........")
            print(Twist) 
            print("Distance: "+str(distance)+", Speed: "+str(Twist[0]) + ", Dir: "+str(Twist[1]))


    else:
        # target reached!
        Twist[0] = 0.0
        Twist[1] = 0.0
        # send_serial(Twist[0], Twist[1])
        # self.call_catch_turtle_server(self.turtle_to_catch_.name)
        # self.turtle_to_catch_ = None


#3 detect robot
def detect_robot():
    detected_rx=0
    detected_ry=0
    detected_gx=0
    detected_gy=0   

    global third_side_angle 
    global destination_x
    global destination_y
    global Red_Robot_x
    global Red_Robot_y
    global theta_error

    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    # red mask    
    red_lower = np.array([0, 141, 206], np.uint8) 
    red_upper = np.array([8, 224, 255], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

    # red mask    
    green_lower = np.array([60, 40, 165], np.uint8) 
    green_upper = np.array([84, 140, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

    #blue
    kernel = np.ones((5, 5), "uint8") 

    # For red color 
    red_mask = cv2.dilate(red_mask, kernel) 
    res_red = cv2.bitwise_and(img, img, mask = red_mask) 
    cv2.imshow('red_mask', res_red)
    red_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    # For green color
    green_mask = cv2.dilate(green_mask, kernel) 
    res_green = cv2.bitwise_and(img, img, mask = green_mask) 
    cv2.imshow('green_mask', res_green)
    green_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
    
    #red contours
    for pic, contour in enumerate(red_contours): 
        area = cv2.contourArea(contour) 
        if(area > 1000): 
            x, y, w, h = cv2.boundingRect(contour) 
            cv2.putText(img, "Robot detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), thickness=2)	
            
            detected_rx = x +(w//2)
            detected_ry = y +(h//2)
            cv2.circle(img=img, center=(detected_rx, detected_ry), radius=3, color=(0, 255, 0), thickness=5)

    # grren contours
    for pic, contour in enumerate(green_contours): 
        area = cv2.contourArea(contour) 
        if(area > 1000): 
            x, y, w, h = cv2.boundingRect(contour) 
            cv2.putText(img, "Direction detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), thickness=2)	
            
            detected_gx = x +(w//2)
            detected_gy = y +(h//2)
            cv2.circle(img=img, center=(detected_gx, detected_gy), radius=3, color=(0, 255, 0), thickness=5)

    # Draw Arrow
    start_point = (detected_rx, detected_ry)
    end_point = (detected_gx, detected_gy)
    cv2.arrowedLine(img, start_point, end_point, (255, 0, 0), 3)

    # Calculate_distances # QS = arrow_lenght # 
    # arrow_length = calculate_distance(detected_gx, detected_gy, detected_rx, detected_ry) # x1, y1, x2, y2
    # third_side = calculate_distance(detected_gx, detected_gy, destination_x, destination_y) # x1, y1, x2, y2

    # calculate distances for arrow  triangle
    qr = abs(detected_gx - detected_rx)
    rs = abs(detected_gy - detected_ry)
    qs = calculate_distance(detected_gx, detected_gy, detected_rx, detected_ry) # x1, y1, x2, y2


    # calculate distances for destination  triangle
    ab = abs(destination_x - detected_rx)
    bc = abs(destination_y - detected_ry)
    ac = calculate_distance(destination_x, destination_y, Red_Robot_x, Red_Robot_y)

    # Calculate_angles 
    arrow_angles = Calculate_angle(qr, qs, rs) # recived A, B, C = arrow_angle, third_side_angle, distance_angle
    destination_angles = Calculate_angle(ab, ac, bc) # recived A, B, C = arrow_angle, third_side_angle, distance_angle

    
    # print(str("arrow_angles: ")+str(int(arrow_angles[2]))+str(" destination_angles: ")+str(int(destination_angles[2]))+str(" theta_error: ")+str(int(theta_error)))
    # print(str("destination_angles: ")+str(destination_angles[2]))
    #print info
    # robo_info(arrow_length, third_side, third_side_angle/10)


    return detected_rx, detected_ry

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

    color = (0, 255, 0)
    thickness = 3
    cv2.line(img, start_point, end_point, color, thickness)


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

    # img = cv2.flip(img, 0)
    # Red_Robot_x, Red_Robot_y = detect_robot()
    Update_frame()
    cv2.imshow('img', img)
    # cv2.imshow('frame', frame)
    cv2.setMouseCallback('img', click_event)
    control_loop()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
















