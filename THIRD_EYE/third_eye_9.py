# importing the module
import cv2
import math
import numpy as np
import time
import serial


#Variables
debug = 0

list_of_points = []
execution_flag = 0

destination_x =1
destination_y =1
Red_Robot_x =1
Red_Robot_y =1
distance = 1
third_side_angle = 0 

min_speed = 35
max_speed = 40
distance_error_factor = 5
Twist = [0, 0]

#error
theta_error = 0
prev_error = 0

control_string = ""
control_string += str(0)+"," + str(0) +","+ str(0) +"," + str(0) + "\n"
speed = 50
ser = serial.Serial(port='COM7',baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

cap = cv2.VideoCapture(1)

def map_range(value, from_low, from_high, to_low, to_high):
    # Check if value is outside the from range
    if value < from_low:
        return to_low
    if value > from_high:
        return to_high

    # Map the value from the from range to the to range
    from_range = from_high - from_low
    to_range = to_high - to_low
    scaled_value = (value - from_low) / from_range
    mapped_value = to_low + (scaled_value * to_range)

    return mapped_value


def send_serial(speed, dir):
    if destination_x != 1:
        control_string = "<"+str(int(speed)) +","+ str(int(dir))  +","+str(0)  +","+str(0)+">"+"\n"
        # if debug == 1:
        print(control_string)
        ser.write(str.encode(control_string))
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
    global min_speed
    global max_speed
    global list_of_points

    destination_x, destination_y = list_of_points[0]
    distance = calculate_distance(destination_x, destination_y, Red_Robot_x, Red_Robot_y) # x1, y1, x2, y2
    distance = int(distance/10) # 10 is factor here
   
    if distance > distance_error_factor:      # Distance_Error_control
   
        Red_Robot_x, Red_Robot_y, turnig,  = detect_robot()

        # position
        speed = map_range(distance, 10, 100, 40, 45)

        #simultaneuos
        # Twist[0] = int(speed) #param
        # Twist[1] = int(turnig)

        #step-by-step
        if turnig == 0:
            Twist[0] = int(speed) #param
            Twist[1] = int(turnig)
        else:
            Twist[0] = int(0) #param
            Twist[1] = int(turnig)

        # # send command now 
        send_serial(Twist[0], Twist[1])

        if debug == 0:    
            print(str("in control loop : ")+"Distance: "+str(distance)+", Speed: "+str(Twist[0]) + ", Dir: "+str(Twist[1]))

    else:
        if debug == 0:    
            print(str("next goal : ")+"Distance: "+str(distance)+", Speed: "+str(Twist[0]) + ", Dir: "+str(Twist[1]))
        # target reached!
        list_of_points.pop(0)
        Twist[0] = 0.0
        Twist[1] = 0.0
        send_serial(Twist[0], Twist[1])
        # self.call_catch_turtle_server(self.turtle_to_catch_.name)
        # self.turtle_to_catch_ = None


#3 detect robot
def detect_robot():
    detected_rx=0
    detected_ry=0
    detected_gx=0
    detected_gy=0   

    mod_destination_angle=0
    mod_arrow_angle=0

    derivative_constant=1
    mapped_value = 0
    global min_speed
    global max_speed
    angle_error_factor = 5

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
        if(area > 200): 
            x, y, w, h = cv2.boundingRect(contour) 
            cv2.putText(img, "Robot detected", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), thickness=2)	
            
            detected_rx = x +(w//2)
            detected_ry = y +(h//2)
            cv2.circle(img=img, center=(detected_rx, detected_ry), radius=3, color=(0, 255, 0), thickness=5)

    # grren contours
    for pic, contour in enumerate(green_contours): 
        area = cv2.contourArea(contour) 
        if(area > 200): 
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
    theta_error = destination_angles[2] - arrow_angles[2]

    # Theta modification

    # for arrow
    if detected_gy > Red_Robot_y and detected_gx > Red_Robot_x:
        mod_arrow_angle = arrow_angles[2]
    elif detected_gy > Red_Robot_y and detected_gx < Red_Robot_x:
        mod_arrow_angle = 180 - arrow_angles[2]
    elif detected_gy < Red_Robot_y and detected_gx < Red_Robot_x:
        mod_arrow_angle = 180 + arrow_angles[2]
    elif detected_gy < Red_Robot_y and detected_gx > Red_Robot_x:
        mod_arrow_angle = 360 - arrow_angles[2]
    else:
        print("object is not there")

    # fro path
    if destination_y > Red_Robot_y and destination_x > Red_Robot_x:
        mod_destination_angle = destination_angles[2]
    elif destination_y > Red_Robot_y and destination_x < Red_Robot_x:
        mod_destination_angle = 180 - destination_angles[2]
    elif destination_y < Red_Robot_y and destination_x < Red_Robot_x:
        mod_destination_angle = 180 + destination_angles[2]
    elif destination_y < Red_Robot_y and destination_x > Red_Robot_x:
        mod_destination_angle = 360 - destination_angles[2]
    else:
        print("path is not there")

    #edge case error handle
    if mod_destination_angle>215 and mod_arrow_angle<45:
            mod_theta_error = - 1*mod_arrow_angle -1*(360 - mod_destination_angle)
    else:
        mod_theta_error = mod_destination_angle - mod_arrow_angle

    if mod_theta_error > math.pi:
        mod_theta_error -= 2*math.pi
    elif mod_theta_error < -math.pi:
        mod_theta_error += 2*math.pi
    
    # for left command
    if mod_theta_error < -1*angle_error_factor:
        mapped_value = map_range(mod_theta_error, -360, -1*angle_error_factor, max_speed, min_speed)
        mapped_value = -1*mapped_value
    # for right command
    elif mod_theta_error > angle_error_factor:
        mapped_value = map_range(mod_theta_error, angle_error_factor, 360, min_speed, max_speed)
    else:
        mapped_value = 0

    turnig = derivative_constant*mapped_value

    if debug == 1:
        print(str("info: ")
            # +str("arrow_angles: ")+str(int(arrow_angles[2]))+str(" destination_angles: ")+str(int(destination_angles[2]))
            +str(" turnig: ")+str((turnig))
            # +str(" goal_theta: ")+str(int(10*goal_theta))+str(" robot_theta: ")+str(int(10*robot_theta))+str(" diff: ")+str(10*diff)
            +str(" mod_destination_angle: ")+str(int(mod_destination_angle))+str(" mod_arrow_angle: ")+str(int(mod_arrow_angle))+str(" mod_theta_error: ")+str(int(mod_theta_error))
        )

    return detected_rx, detected_ry, turnig

#2 Update frame
def Update_frame(): # only updates static frame with destination_x, destination_y, Red_Robot_x, Red_Robot_y coordinates and path
    global Red_Robot_x
    global Red_Robot_y
    global destination_x
    global destination_y

    Red_Robot_x, Red_Robot_y , _ = detect_robot()
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
    global execution_flag

    if event == cv2.EVENT_LBUTTONDOWN:
        list_of_points.append([x, y])

    if event==cv2.EVENT_RBUTTONDOWN:
        # destination_x=x
        # destination_y=y
        execution_flag = 1


# ret, frame = cap.read()
# run_once()
while True:
    ret, img = cap.read()

    # img = cv2.flip(img, 0)
    # Red_Robot_x, Red_Robot_y = detect_robot()
    cv2.setMouseCallback('img', click_event)
    if  len(list_of_points) != 0 and execution_flag == 1:
        Update_frame()
        destination_x= Red_Robot_x
        destination_y= Red_Robot_y
        cv2.imshow('img', img)
        # cv2.imshow('frame', frame)
        cv2.setMouseCallback('img', click_event)
        control_loop()
    else:
        execution_flag = 0

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()



""" 
This file is to handle the edge case error
"""












