import numpy as np
import cv2 as cv

img = cv.imread('lena.jpg')
#img = cv.line(img, (0, 0), (255, 255), (0, 255, 0), 5)
img = cv.arrowedLine(img, (0, 0), (255, 255), (0, 255, 0), 5)

cv.imshow('image', img)

cv.waitKey(0)
cv.destroyAllWindows()
