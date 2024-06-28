import cv2 as cv
import numpy as np

img = np.zeros([512, 512, 3], np.uint8)

cv.imshow('image', img)

cv.waitKey(0)
cv.destroyAllWindows()