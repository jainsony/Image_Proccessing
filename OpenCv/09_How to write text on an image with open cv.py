import numpy as np
import cv2 as cv

img = cv.imread('lena.jpg')

font = cv.FONT_HERSHEY_DUPLEX
img = cv.putText(img, 'BINOD', (10, 500), font, 4, (0, 255, 0), 5, cv.LINE_AA)

cv.imshow('image', img)

cv.waitKey(0)
cv.destroyAllWindows()
