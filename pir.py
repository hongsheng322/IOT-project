import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led1 = 23
pirPin = 24
lightPin = 25
firePin = 27
buzzerled = 26

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(pirPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(lightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(firePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzerled, GPIO.OUT)

print("Sensor Alarm (CTRL+C to exit)")
time.sleep(.2)
print("Ready")
    

try:

    GPIO.add_event_detect(firePin, GPIO.BOTH, bouncetime=300)


    while 1:
        #if motion is detected, no light, lights on
        if GPIO.input(pirPin) == 1:
                print GPIO.input(pirPin)
                print("Motion Detected!")

                #if light is detected
                if GPIO.input(lightPin) == 1:
                    print("Room Lightning Detected!")
                    print("LED Off")
                    GPIO.output(led1, GPIO.LOW)
                else:
                    print("No Room Lightning Detected!")
                    print("LED On")
                    GPIO.output(led1, GPIO.HIGH)

        #if no motion, check light, if lights on, off light
        else:
            print("No Motion Detected!")
            
            #if fire is detected
            if GPIO.event_detected(firePin):
                time.sleep(5)
                print("Flame Detected!")
                print("Buzzer LED On")
                GPIO.output(buzzerled, GPIO.HIGH)

                #if light is detected
                if GPIO.input(lightPin) == 1:
                    time.sleep(5)
                    print("Room Lightning Detected!")
                    print("Buzzer LED On")
                    GPIO.output(buzzerled, GPIO.HIGH)

            #no fire is detected
            else:
                print("No Flame Detected!")

                #if light is detected
                if GPIO.input(lightPin) == 1:
                    time.sleep(10)
                    print("Room Lightning Detected!")
                    print("Buzzer LED On")
                    GPIO.output(buzzerled, GPIO.HIGH)
                else:
                    print("No Room Lightning Detected!")
                    GPIO.output(buzzerled, GPIO.LOW)
            
        time.sleep(2)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
