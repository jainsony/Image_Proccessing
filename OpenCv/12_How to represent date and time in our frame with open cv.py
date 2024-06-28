import cv2 as cv
import datetime
vid = cv.VideoCapture(0)

while (vid.isOpened()):
    sig, frame = vid.read()
    if sig == True:
        font = cv.FONT_HERSHEY_DUPLEX
        text = 'width:'+str(vid.get(3))+'Height:'+str(vid.get(4))
        date = str(datetime.datetime.now())
        frame = cv.putText(frame, date, (20, 60), font, 1, (0, 0, 0), 2, cv.LINE_AA)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', frame)

        if cv.waitKey(1) == ord('q'):
            break
    else:
        break
vid.release()
cv.destroyAllWindows()