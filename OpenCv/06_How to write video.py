import cv2 as cv

vid = cv.VideoCapture(0)
codec = cv.VideoWriter_fourcc(*'XVID')
vid_out = cv.VideoWriter('output_video.mp4', codec, 10.0, (640, 480))

while (vid.isOpened()):
    sig, frame = vid.read()
    if sig == True:
        vid_out.write(frame)
        # cv.imshow('frame', frame)

        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
vid.release()
vid_out.release()
cv.destroyAllWindows()
