import RPi.GPIO as GPIO
import time

light = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(light,GPIO.IN)
for i in range (0,100):
    time.sleep(1)
    print GPIO.input(light)