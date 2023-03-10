import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define GPIO pins for ultrasonic sensor
TRIG = 23
ECHO = 24

# Set up GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to calculate distance from sensor
def get_distance():
    # Send ultrasonic pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Measure time taken for pulse to return
    start_time = time.time()
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    end_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    pulse_duration = end_time - start_time

    # Calculate distance based on pulse duration
    speed_of_sound = 34300 # cm/s
    distance = (speed_of_sound * pulse_duration) / 2

    return distance

# Main loop to continuously read distance
try:
    while True:
        distance = get_distance()
        print("Distance: {:.2f} cm".format(distance))
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
