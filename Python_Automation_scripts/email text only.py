import smtplib as s
import cv2 as cv
from email.message import EmailMessage


ob = s.SMTP("smtp.gmail.com", 587)
ob.starttls()

ob.login("pythonproject01send@gmail.com", "Python@123")

subject = "Sending email using python"
body = "this is tutorial of sending email using python script"

msg = EmailMessage()
message = "Subject:{}\n\n{}".format(subject, body)

listOfAddress = ["pythonproject01rec@gmail.com"]    #we can do that too ---> listOfAddress = ["jainsony05@gmail.com", "pythonproject01rec@gmail.com"]

ob.sendmail("pythonproject01", listOfAddress, message)
print("send successfully...")
ob.quit()



