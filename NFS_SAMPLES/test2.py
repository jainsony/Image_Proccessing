import cv2
import numpy as np

def nothing(x):
    pass

# cv2.namedWindow("Tracking")
# cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
# cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
# cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
# cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
# cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
# cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

vidcap = cv2.VideoCapture("Videos/nfs1.mp4")
# Capture video frame by frame
success, frame = vidcap.read()


while True:

    # Capture video frame by frame
    success, frame = vidcap.read()

    # Resize the image frames
    resize = cv2.resize(frame, (640, 480))
    # frame = cv2.imread('nfs3.png')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # l_h = cv2.getTrackbarPos("LH", "Tracking")
    # l_s = cv2.getTrackbarPos("LS", "Tracking")
    # l_v = cv2.getTrackbarPos("LV", "Tracking")

    # u_h = cv2.getTrackbarPos("UH", "Tracking")
    # u_s = cv2.getTrackbarPos("US", "Tracking")
    # u_v = cv2.getTrackbarPos("UV", "Tracking")

    lower = np.array([78,0,142]) #For white range
    upper = np.array([132,24,255])
    
    yellower = np.array([16,0,134]) #For yellow range
    yelupper = np.array([64,177,255])
    
    yellowmask = cv2.inRange(hsv, yellower, yelupper)    
    whitemask = cv2.inRange(hsv, lower, upper)


    # l_b = np.array([l_h, l_s, l_v])
    # u_b = np.array([u_h, u_s, u_v])

    yellowmask = cv2.inRange(hsv, yellower, yelupper)    
    whitemask = cv2.inRange(hsv, lower, upper)

    mask = cv2.bitwise_or(yellowmask, whitemask)  
    res = cv2.bitwise_and(frame, frame, mask = mask)   

    # mask = cv2.inRange(hsv, l_b, u_b)

    # res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()