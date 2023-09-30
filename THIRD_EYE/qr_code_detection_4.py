import cv2

camera_id = 1
delay = 10
window_name = 'OpenCV QR Code'

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)

x1=0
y1=0
x2=0
y2=0

tqx1=0
tqy1=0
tqx2=0
tqy2=0 

while True:
    ret, frame = cap.read()

    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    print(s)
                    print("p = "+str([p.astype(int)]))
                    # P1 = ([p[0][0], p[0][1]])
                    # P3 = ([p[2][0], p[2][1]])

                    # print([P1.astype(int)])
                    # print([P3.astype(int)])
                    # print("p = "+str(p[1][0]))
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                              
                x1 = int(p[0][0])
                y1 = int(p[0][1])

                x2 = int(p[2][0])
                y2 = int(p[2][1])

                # else:
                #     tqx1=0
                #     tqy1=0                     
                #     tqx2=0
                #     tqy2=0    

                first_qr_point = (tqx1, tqy1)
                second_qr_point = (tqx2, tqy2)

                start_point = (x1, y1)
                end_point = (x2, y2)

                thickness = 3
                
                img = cv2.line(frame, start_point, end_point, color, thickness)

                x, y = (x1 + x2) // 2, (y1 + y2) // 2

                if s == 'test_qr_1':
                    tqx1=x
                    tqy1=y
                
                elif s == 'test_qr_4':
                    tqx2=x
                    tqy2=y
                # Draw a circle in the center of rectangle
                img = cv2.circle(img=img, center=(x, y), radius=3, color=(0, 0, 255), thickness=3)

                img = cv2.line(frame, first_qr_point, second_qr_point, color, thickness)
                # img = cv2.line(frame, P1, P3, color, thickness)
                print("--------------")
                # print(P1[0][0])
                # P1 = [p[0][0], p[0][1]]
                # P3 = [p[2][0], p[2][1]]
                # print(P1)
                # print(P3)

                frame = img
        cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyWindow(window_name)

