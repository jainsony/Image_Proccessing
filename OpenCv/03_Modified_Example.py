import cv2 as cv

img = cv.imread('lena.jpg', 0)
cv.imshow('image', img)
k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('w'):
    cv.imwrite('lena_black&white.png', img)
    cv.destroyAllWindows()