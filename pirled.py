import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

led1 = 17
pirPin = 23

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(pirPin, GPIO.IN)

print("Motion Sensor Alarm (CTRL+C to exit)")
time.sleep(.2)
print("Ready")

try:
    for i in range(100):
        if GPIO.input(pirPin) == 1:
            print GPIO.input(pirPin)
            print("Motion Detected!")
            print("Lights On!")
            GPIO.output(led1, GPIO.HIGH)
            time_off = 5
            for j in range(time_off, 0, -1):
                print("No motion detected. Time off in " + str(time_off) + " seconds")
                time_off -= 1
                time.sleep(1)
        
        else:
            print("No Motion Detected!")
            print("Lights Off!")
            GPIO.output(led1, GPIO.LOW)
            time.sleep(1)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
