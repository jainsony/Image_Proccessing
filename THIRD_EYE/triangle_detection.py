import cv2
import numpy as np

def nothing(x):
    pass

######### config
# white tracking
cv2.namedWindow("WTracking")
cv2.createTrackbar("WLH", "WTracking", 75, 255, nothing)
cv2.createTrackbar("WLS", "WTracking", 94, 255, nothing)
cv2.createTrackbar("WLV", "WTracking", 134, 255, nothing)

cv2.createTrackbar("WUH", "WTracking", 255, 255, nothing)
cv2.createTrackbar("WUS", "WTracking", 255, 255, nothing)
cv2.createTrackbar("WUV", "WTracking", 255, 255, nothing)

# yellow tracking
cv2.namedWindow("YTracking")
cv2.createTrackbar("YLH", "YTracking", 0, 255, nothing)
cv2.createTrackbar("YLS", "YTracking", 0, 255, nothing)
cv2.createTrackbar("YLV", "YTracking", 0, 255, nothing)

cv2.createTrackbar("YUH", "YTracking", 0, 255, nothing)
cv2.createTrackbar("YUS", "YTracking", 0, 255, nothing)
cv2.createTrackbar("YUV", "YTracking", 0, 255, nothing)
########### end config

# vidcap = cv2.VideoCapture("Videos/nfs1.mp4")
vidcap = cv2.VideoCapture(1)
# Capture video frame by frame
# success, frame = vidcap.read()

def control_robot(situation, signal):
    print(situation + '\n ' + signal)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(res, situation + " - " + signal, (10, 20), font, 0.3, (255, 255, 0), 1)


def processTriangle(image):
    ##########################################################################33################################################################
    maxI=0
    # arrow angle detection algorithm
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #GaussianBlur()
    blur = cv2.GaussianBlur(gray,(9, 9), 2, 2)
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thresh,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #####################################################################################################################################
    #print("large " + str(len(contours)))
    if len(contours) == 3 :
        #print("Found 3 contours")
        maxX=0
        maxI=0
        i =0

        for cont in contours:
            mu = cv2.moments(cont)
            if mu['m00'] > 100.0 :
                #cv2.drawContours(image, [cont], 0, (0,255,0), 3)
                x,y,w,h = cv2.boundingRect(cont)
                if i==0  :
                    maxX=x
                else :
                    maxI = i if x>maxX else maxI

            i=i+1
        #new algorithm - CIRCLE ALGO 26-09-2018 to get direction of arrow
	#System.out.println("1 contour detected")

    if maxI < len(contours):
        pointarrray = contours[maxI]
        (x,y),radius = cv2.minEnclosingCircle(pointarrray)
        cv2.drawContours(image, pointarrray, -1, (255,255,0), 2)
        center = [int(x),int(y)]
        print("center : " + str(center))
        rad = int(radius)
        rad=rad-5

        # cv2.circle(image,center,rad,(255, 128, 255),2)
        # cv2.circle(image, int(center[0]), int(center[1]), rad, (255, 128, 255), max(2, 0))
        cv2.circle(img=image, center=(int(center[0]), int(center[1])), radius=3, color=(0, 255, 0), thickness=2)
        corners = []
        for p in pointarrray:
            point = (p[0][0],p[0][1])
            #print pt
            #cv2.circle(im,pt,5,(200,0,0),2)
            leftV = (point[1]-center[1])*(point[1]-center[1])+(point[0]-center[0])*(point[0]-center[0])
            if leftV > rad*rad :
                corners.append(point)
                #System.out.println("hi"+point.x+" "+point.y)
        #print("corners  " + str(len(corners)))
        p1x = 0
        p1y = 0
        pn1=0
        p2x = 0
        p2y = 0
        pn2=0
        p3x = 0
        p3y = 0
        pn3=0   
        if len(corners)>3:
                p1x=corners[0][0]
                p1y=corners[0][1]
                pn1=pn1+1
                offset=10
                for corner in corners :
                    cornerX=corner[0]
                    cornerY=corner[1]
                    if (cornerX < p1x/pn1+offset) and (cornerX > p1x/pn1-offset) and (cornerY < p1y/pn1+offset) and (cornerY > p1y/pn1-offset) :
                        p1x=p1x+cornerX
                        p1y=p1y+cornerY
                        pn1=pn1+1
                    else :
                        if pn2==0 :
                            p2x=cornerX
                            p2y=cornerY
                            pn2=pn2+1
                        elif (cornerX < p2x/pn2+offset) and (cornerX > p2x/pn2-offset) and (cornerY < p2y/pn2+offset) and (cornerY > p2y/pn2-offset) :
                            p2x=p2x+cornerX
                            p2y=p2y+cornerY
                            pn2=pn2+1
                        else :
                            if pn3==0  :
                                p3x=cornerX
                                p3y=cornerY
                                pn3=pn3+1
                            elif (cornerX < p3x/pn3+offset) and (cornerX > p3x/pn3-offset) and (cornerY < p3y/pn3+offset) and (cornerY > p3y/pn3-offset) :
                                p3x=p3x+cornerX
                                p3y=p3y+cornerY
                                pn3=pn3+1
                if pn1 > 0 and pn2 > 0 and pn3 > 0 : 
                    p1x/=pn1
                    p2x/=pn2
                    p3x/=pn3
                    p1y/=pn1
                    p2y/=pn2
                    p3y/=pn3

                    #print("corner point1 = " + str(p1x)+","+str(p1y))
                    #print("corner point2 = " + str(p2x)+","+str(p2y))
                    #print("corner point3 = " + str(p3x)+","+str(p3y))
                    # cv2.circle(image,p1x,p1y,4,(0, 255, 255),2)
                    # cv2.circle(image,p2x,p2y,4,(0, 255, 255),2)
                    # cv2.circle(image,p3x,p3y,4,(0, 255, 255),2)
                    cv2.circle(img=image, center=(int(p1x), int(p1y)), radius=4, color=(0, 255, 255), thickness=2)
                    cv2.circle(img=image, center=(int(p2x), int(p2y)), radius=4, color=(0, 255, 255), thickness=2)
                    cv2.circle(img=image, center=(int(p3x), int(p3y)), radius=4, color=(0, 255, 255), thickness=2)

                    length1_2 = (p1x - p2x)*(p1x - p2x)+(p1y - p2y)*(p1y - p2y)
                    length2_3 = (p2x - p3x)*(p2x - p3x)+(p2y - p3y)*(p2y - p3y)
                    length3_1 = (p3x - p1x)*(p3x - p1x)+(p3y - p1y)*(p3y - p1y)

                    #print("length1_2 = " + str(length1_2))
                    #print("length2_3 = " + str(length2_3))
                    #print("length3_1 = " + str(length3_1))
                    
                    directedX=0
                    directedY=0
                    if length1_2 <=length2_3 :
                        if length3_1<length1_2 : 
                            directedX=p2x
                            directedY=p2y
                        else :
                            directedX=p3x
                            directedY=p3y
                    else :
                        if length3_1<length2_3 :
                            directedX=p2x
                            directedY=p2y
                        else :
                            directedX=p1x
                            directedY=p1y
                    # cv2.circle(image,(directedX,directedY),5,(0, 0, 255),2)
                    cv2.circle(img=image, center=(int(directedX), int(directedY)), radius=5, color=(0, 0, 255), thickness=2)
                    start_point = (int(directedX), int(directedY))
                    end_point = (int(center[0]), int(center[1]))
                    cv2.line(image, start_point, end_point, (0, 255, 0), 3)
                    angle = 0
                    
                    numer = y-directedY #numerator
                    denom = x-directedX #denominator
                    if denom != 0 :
                        angle = np.absolute(np.degrees(np.arctan(numer/denom)))
                    else :
                        angle = 90
                    #print("angle "+str(angle))
                    turnningSignal = ""
                    if angle < 8 and denom < 0:
                        turnningSignal = "TURN RIGHT ANGLE = 90"
                    elif angle < 8 and denom > 0:
                        turnningSignal = "TURN LEFT ANGLE = 90"
                    elif angle > 82 and numer > 0:
                        turnningSignal = "GO FORWARD"
                        isTriangleFound = False
                    elif angle > 82 and numer < 0:
                        turnningSignal = "TURN DIRECTLY BACK"
                    elif numer > 0 and  denom < 0:
                        turnningSignal = "TURN RIGHT ANGLE = "+ str(90-angle)
                    elif numer > 0 and  denom > 0:
                        turnningSignal = "TURN LEFT ANGLE = "+ str(90-angle)
                    elif numer < 0 and  denom < 0:
                        turnningSignal = "TURN RIGHT ANGLE = "+ str(90+angle)
                    elif numer < 0 and  denom > 0:
                        turnningSignal = "TURN LEFT ANGLE = "+ str(90+angle)
                    control_robot("",turnningSignal)


while True:

    # Capture video frame by frame
    success, frame = vidcap.read()

    # Resize the image frames
    frame = cv2.resize(frame, (640, 480))
    # frame = cv2.resize(frame, (1280, 720))

    # frame = cv2.imread('nfs3.png')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

######### config
    #white
    w_l_h = cv2.getTrackbarPos("WLH", "WTracking")
    w_l_s = cv2.getTrackbarPos("WLS", "WTracking")
    w_l_v = cv2.getTrackbarPos("WLV", "WTracking")

    w_u_h = cv2.getTrackbarPos("WUH", "WTracking")
    w_u_s = cv2.getTrackbarPos("WUS", "WTracking")
    w_u_v = cv2.getTrackbarPos("WUV", "WTracking")

    #yellow
    y_l_h = cv2.getTrackbarPos("YLH", "YTracking")
    y_l_s = cv2.getTrackbarPos("YLS", "YTracking")
    y_l_v = cv2.getTrackbarPos("YLV", "YTracking")

    y_u_h = cv2.getTrackbarPos("YUH", "YTracking")
    y_u_s = cv2.getTrackbarPos("YUS", "YTracking")
    y_u_v = cv2.getTrackbarPos("YUV", "YTracking")

    lower = np.array([w_l_h, w_l_s, w_l_v]) #For white range
    upper = np.array([w_u_h, w_u_s, w_u_v])
    
    yellower = np.array([y_l_h, y_l_s, y_l_v]) #For yellow range
    yelupper = np.array([y_u_h, y_u_s, y_u_v])
########### end config
    bars_show =1
    if bars_show == 1:
        yellowmask = cv2.inRange(hsv, yellower, yelupper)    
        whitemask = cv2.inRange(hsv, lower, upper)

        yellowmask = cv2.inRange(hsv, yellower, yelupper)    
        whitemask = cv2.inRange(hsv, lower, upper)

    mask = cv2.bitwise_or(yellowmask, whitemask)  
    res = cv2.bitwise_and(frame, frame, mask = mask)  

    edges = cv2.Canny(mask, 100, 254, 3)

    processTriangle(res)



    print(edges)
    # cv2.imshow("edges", edges) 
    # cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()