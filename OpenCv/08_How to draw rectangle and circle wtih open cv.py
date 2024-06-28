import numpy as np
import cv2 as cv

img = cv.imread('lena.jpg')
img = cv.rectangle(img, (50, 50), (255, 255), (0, 255, 0), 5)
img = cv.circle(img, (100, 100), 40, (0, 255, 0), 5)

cv.imshow('image', img)

cv.waitKey(0)
cv.destroyAllWindows()
