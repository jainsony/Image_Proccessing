import cv2 as cv
import numpy as np

def click_event(event, x, y, flags, param):

    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), 3, (0, 0, 255), -1)
        points.append((x, y))
        if len(points) >= 2:
            cv.line(img, points[-1])
