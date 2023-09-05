import cv2
import numpy as np

def nothing(x):
    pass

def roi(img):
    x = int(img.shape[1])
    y = int(img.shape[0])
    shape = np.array([[int(0), int(y)], [int(x), int(y)], [int(0.55*x), int(0.40*y)], [int(0.45*x), int(0.40*y)]])

    #define a numpy array with the dimensions of img, but comprised of zeros
    mask = np.zeros_like(img)

    #Uses 3 channels or 1 channel for color depending on input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #creates a polygon with the mask color
    cv2.fillPoly(mask, np.int32([shape]), ignore_mask_color)

    #returns the image only where the mask pixels are not zero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image




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

vidcap = cv2.VideoCapture("Videos/nfs1.mp4")
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

    edges = cv2.Canny(mask, 100, 254, 3)
    #  Canny( detected_edges, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size );
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)



    # cv2.imshow("frame", frame)


    # mask = cv2.inRange(hsv, l_b, u_b)
    roi_img = roi(mask)
    # res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("roi", roi_img) 
    # cv2.imshow("edges", edges) 
    # cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    # cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()