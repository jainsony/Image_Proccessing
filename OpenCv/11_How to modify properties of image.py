import cv2 as cv

vid = cv.VideoCapture(0)

vid.set((cv.CAP_PROP_FRAME_WIDTH), 600)   # max value for my logitech
#vid.set((cv.CAP_PROP_FRAME_HEIGHT), 960)

print(vid.get(cv.CAP_PROP_FRAME_WIDTH))
print(vid.get(cv.CAP_PROP_FRAME_HEIGHT))

while vid.isOpened():
    sig, frame = vid.read()
    if sig == True:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)

        if cv.waitKey(1) == ord('q'):
            break
    else:
        break
vid.release()
cv.destroyAllWindows()