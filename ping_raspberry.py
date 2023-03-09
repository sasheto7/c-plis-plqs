import os
import smtplib
from password import ivan_password
import cv2

ip_address = "10.1.79.235"
response = os.system("ping -c 1 " + ip_address)
if response == 0:
    print("Ping successful!")
else:
    print("Ping not successful!")
    sender_email = "ivan.g.genov.2021@elsys-bg.org"
    receiver_email = "gixirobot@gmail.com"
    password = ivan_password
    subject = "Malfunction in the system"
    body = "Maybe there is a problem with the robot!!! Please check it asap."
    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_email, message)

    server.quit()



face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)

while True:
    _, img =cap.read()

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 10)

    if len(faces) > 0:
        sender_email = "ivan.g.genov.2021@elsys-bg.org"
        receiver_email = "gixirobot@gmail.com"
        password = ivan_password
        subject = "SOMEONE IS DETECTED"
        body = "Please check the area as soon as possible."
        message = f"Subject: {subject}\n\n{body}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, message)

        server.quit()
    
    
    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k==27:
        break

cap.release()