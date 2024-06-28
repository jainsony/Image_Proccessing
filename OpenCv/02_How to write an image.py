import cv2 as cv

img = cv.imread("lena.jpg")
cv.imshow('image', img)
print(img)
cv.waitKey(2000)
cv.imwrite('lena_black_and_white.png', img)

cv.destroyAllWindows()

