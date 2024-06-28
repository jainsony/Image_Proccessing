import cv2 as cv
import numpy as np

#events = [i for i in dir(cv) if 'EVENTS' in i ]
# prints(events)

def click_event(event, x, y, flags, param):
    if event == cv.EVENT_RBUTTONDOWN:

        blue = img[y, x, 0]
        green = img[y, x, 1]
        red = img[y, x, 2]

        font = cv.FONT_HERSHEY_DUPLEX
        strBGR = str(blue) + ',' + str(green) + ',' + str(red)
        cv.putText(img, strBGR, (x, y), font, 0.5, (0, 255, 255), 2)
        cv.imshow('image', img)

img = cv.imread('lena.jpg')
cv.imshow('image', img)

cv.setMouseCallback('image', click_event)
cv.waitKey(0)
cv.destroyAllWindows()