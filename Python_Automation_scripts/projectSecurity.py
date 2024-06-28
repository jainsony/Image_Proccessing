import cv2
import numpy as np
import smtplib
from email.message import EmailMessage
import time

trigger = 1

msg = EmailMessage()

msg['Subject'] = 'demo'
msg['From'] = 'Dev'
msg['To'] = "pythonproject01rec@gmail.com", "jain.dhani@gmail.com"

cap = cv2.VideoCapture(0)
codec = cv2.VideoWriter_fourcc(*'XVID')

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter("Scene_video.mp4", codec, 5.0, (1280, 720))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

print(frame1.shape)

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if(cv2.contourArea(contour) < 6000): #or (trigger == 1):  #################################################
            continue
        print(cv2.contourArea(contour))
        print("Security Breach !!!")
        #MOVEMENT

        for i in range(3):
            print("Taking "+str(i))
            time.sleep(2)
            return_value, image = cap.read()
            cv2.imwrite('opencv' + str(i) + '.png', image)

        print("Sending Email...")
        print("Please wait")

        for i in range(3):
            with open('opencv' + str(i) + '.png', 'rb') as f:
                img = f.read()
                file_name = f.name
                msg.add_attachment(img, maintype='application', subtype='png', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("pythonproject01send@gmail.com", "Python@123")
            server.send_message(msg)

        print("Email sent !!!")

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()