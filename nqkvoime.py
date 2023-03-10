import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

napred1 = 3
napred2 = 5
nazad1 = 11
nazad2 = 13

GPIO.setup(napred1, GPIO.OUT)
GPIO.setup(napred2, GPIO.OUT)
GPIO.setup(nazad1, GPIO.OUT)
GPIO.setup(nazad1, GPIO.OUT)

GPIO.output(napred1, GPIO.HIGH)
GPIO.output(napred2, GPIO.LOW)
time.sleep(3)
GPIO.output(nazad1, GPIO.HIGH)
GPIO.output(nazad1, GPIO.LOW)
time.sleep(3)

GPIO.cleanup()