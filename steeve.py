import smtplib
from email.mime.text import MIMEText
from picamera2 import MappedArray
from password import ivan_password
import RPi.GPIO as GPIO
import cv2
import libcamera
from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder
import time

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 40
ECHO_PIN = 38
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

bachkai = 1

def measure_distance():
    # send a pulse to the ultrasonic sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
 
    # measure the time it takes for the echo to return
    start_time = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        if (time.time() - start_time) > 0.1:
            return -1
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        if (time.time() - start_time) > 0.1:
            return -1
    pulse_end = time.time()
 
    # calculate the distance based on the time it took for the echo to return
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
 
    return distance
    
dis1 = measure_distance()

while(bachkai==1):
	dis = measure_distance()
	if(dis!=dis1):
		bachkai = 0
	
GPIO.cleanup()

if(bachkai==0):
	# Set up email information
	sender_email = 'ivan.g.genov.2021@elsys-bg.org'
	sender_password = ivan_password
	recipient_email = 'gixirobot@gmail.com'
	subject = 'Person detected'
	body = 'A person has been detected in the video stream.'

	# Create SMTP session
	smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
	smtp_server.starttls()
	smtp_server.login(sender_email, sender_password)

	# Create email message
	message = MIMEText(body)
	message['From'] = sender_email
	message['To'] = recipient_email
	message['Subject'] = subject

	def draw_faces(request):
		global faces
		with MappedArray(request, "main") as m:
			for f in faces:
				(x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
				cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
				# Send email when face is detected
				smtp_server.sendmail(sender_email, recipient_email, message.as_string())
				time.sleep(5)
				
	picam2 = Picamera2()
	picam2.start_preview(Preview.QTGL)
	config = picam2.create_preview_configuration(main={"size": (640, 480)},
												 lores={"size": (320, 240), "format": "YUV420"})
	config["transform"] = libcamera.Transform(hflip=1, vflip=1)
	picam2.configure(config)

	(w0, h0) = picam2.stream_configuration("main")["size"]
	(w1, h1) = picam2.stream_configuration("lores")["size"]
	s1 = picam2.stream_configuration("lores")["stride"]
	faces = []
	picam2.post_callback = draw_faces

	encoder = H264Encoder(10000000)
	picam2.start_recording(encoder, "test.h264")

	start_time = time.monotonic()
	# Run for 10 seconds.
	while time.monotonic() - start_time < 100:
		buffer = picam2.capture_buffer("lores")
		grey = buffer[:s1 * h1].reshape((h1, s1))
		faces = face_detector.detectMultiScale(grey, 1.1, 3)

	picam2.stop_recording()
	smtp_server.quit()
