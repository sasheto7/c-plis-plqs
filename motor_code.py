import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode to BCM
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for motor control
IN1 = 36 
IN2 = 38
ENA = 40
IN3 = 8
IN4 = 10
ENA2 = 12

# Set up GPIO pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)

# Create PWM object with 50Hz frequency
pwm = GPIO.PWM(ENA, 50)
pwm2 = GPIO.PWM(ENA2, 50)

# Set initial duty cycle to 0
pwm.start(0)
pwm2.start(0)

# Define function to control motor speed and direction
def set_motor_speed(speed, direction):
    # Set IN1 and IN2 pins to control motor direction
    if direction == "forward":
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif direction == "reverse":
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    else:
        raise ValueError("Invalid direction. Please choose 'forward' or 'reverse'.")

    # Set duty cycle to control motor speed
    pwm.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)

# Example usage
try:
    while True:
        set_motor_speed(50, "forward") # 50% speed in forward direction
        time.sleep(2) # Wait 2 seconds
        set_motor_speed(0, "reverse") # Stop motor and change direction
        time.sleep(2) # Wait 2 seconds
        set_motor_speed(100, "forward") # 100% speed in forward direction
        time.sleep(2) # Wait 2 seconds

except KeyboardInterrupt:
    # Clean up GPIO pins on program exit
    GPIO.cleanup()
