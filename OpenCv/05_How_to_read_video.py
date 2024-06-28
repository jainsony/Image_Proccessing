import cv2 as cv

vid = cv.VideoCapture(0)

while True:
    sig, frame = vid.read()
    # cv.imshow('frame', frame)
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray_img)
    if cv.waitKey(1) == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
