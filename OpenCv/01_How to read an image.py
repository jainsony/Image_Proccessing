import cv2 as cv

img = cv.imread("lena.jpg", 1)
cv.imshow('image', img)
print(img)
cv.waitKey(2000)
cv.destroyAllWindows()

