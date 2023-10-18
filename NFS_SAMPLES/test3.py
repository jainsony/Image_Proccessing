import cv2
import numpy as np

def nothing(x):
    pass

######### config
# white tracking
cv2.namedWindow("WTracking")
cv2.createTrackbar("WLH", "WTracking", 20, 255, nothing)
cv2.createTrackbar("WLS", "WTracking", 0, 255, nothing)
cv2.createTrackbar("WLV", "WTracking", 180, 255, nothing)

cv2.createTrackbar("WUH", "WTracking", 255, 255, nothing)
cv2.createTrackbar("WUS", "WTracking", 16, 255, nothing)
cv2.createTrackbar("WUV", "WTracking", 240, 255, nothing)

# yellow tracking
cv2.namedWindow("YTracking")
cv2.createTrackbar("YLH", "YTracking", 16, 255, nothing)
cv2.createTrackbar("YLS", "YTracking", 0, 255, nothing)
cv2.createTrackbar("YLV", "YTracking", 134, 255, nothing)

cv2.createTrackbar("YUH", "YTracking", 64, 255, nothing)
cv2.createTrackbar("YUS", "YTracking", 177, 255, nothing)
cv2.createTrackbar("YUV", "YTracking", 250, 255, nothing)
########### end config

# vidcap = cv2.VideoCapture("Videos/nfs1.mp4")
vidcap = cv2.VideoCapture(1)
# Capture video frame by frame
success, frame = vidcap.read()


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

    # lower = np.array([78,0,142]) #For white range
    # upper = np.array([132,24,255])
    
    # yellower = np.array([16,0,134]) #For yellow range
    # yelupper = np.array([64,177,255])
    
    yellowmask = cv2.inRange(hsv, yellower, yelupper)    
    whitemask = cv2.inRange(hsv, lower, upper)

    yellowmask = cv2.inRange(hsv, yellower, yelupper)    
    whitemask = cv2.inRange(hsv, lower, upper)

    mask = cv2.bitwise_or(yellowmask, whitemask)  
    res = cv2.bitwise_and(frame, frame, mask = mask)   

    # mask = cv2.inRange(hsv, l_b, u_b)

    # res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()