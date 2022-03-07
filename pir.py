#python pir.py
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

led1 = 17
led2 = 27
pirPin = 26

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(pirPin, GPIO.IN)


print("Motion Sensor Alarm (CTRL+C to exit)")
time.sleep(.2)
print("Ready")

try:
    while 1:
        #if motion is detected
        if GPIO.input(pirPin):
            print("Motion Detected!")
            print("Lights on")
            GPIO.output(led1, GPIO.HIGH)
            GPIO.output(led2, GPIO.HIGH)

        else:
            print("No Motion Detected!")
            print("Lights off")
            GPIO.output(led1, GPIO.LOW)
            GPIO.output(led2, GPIO.LOW)
        time.sleep(2)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()