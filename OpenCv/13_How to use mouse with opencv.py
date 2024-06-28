import cv2 as cv
import numpy as np

#events = [i for i in dir(cv) if 'EVENTS' in i ]
# prints(events)

def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, ',', y)
        font = cv.FONT_HERSHEY_DUPLEX
        strxy = str(x) + ',' + str(y)
        cv.putText(img, strxy, (x, y), font, 1, (0, 255, 255), 2)
        cv.imshow('image', img)

img = np.zeros((512, 512, 3), np.uint8)
cv.imshow('image', img)
cv.setMouseCallback('image', click_event)

cv.waitKey(0)
cv.destroyAllWindows()