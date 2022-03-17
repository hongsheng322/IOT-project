import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
p = GPIO.PWM(2, 50)
p.start(50)

loop_count = True

def siren():
    for x in range(0, 361):
        sinVal = math.sin(x*(math.pi / 180.0))
        toneVal = 2000 + sinVal * 750
        p.ChangeFrequency(toneVal)
        time.sleep(0.001)

while loop_count is True:
    siren()


    