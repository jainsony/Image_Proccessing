import smtplib
from email.message import EmailMessage

msg = EmailMessage()

msg['Subject'] = 'demo'
msg['From'] = 'Dev'
msg['To'] = "pythonproject01rec@gmail.com"  # we can add other like --> "jainsony05@gmail.com", "pythonproject01rec@gmail.com"


with open("lena.jpg", 'rb') as f:
    img = f.read()
    file_name = f.name
    msg.add_attachment(img, maintype='application', subtype='jpg', filename=file_name)


with open("output.avi", 'rb') as f:
    img = f.read()
    file_name = f.name
    msg.add_attachment(img, maintype='application', subtype='avi', filename=file_name)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server. login("pythonproject01send@gmail.com", "Python@123")
    server.send_message(msg)

print("Email sent !!!")
