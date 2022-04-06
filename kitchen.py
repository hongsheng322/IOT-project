import random
import time
from paho.mqtt import client as mqtt_client
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
time.sleep(0.1)
print("Ready")

broker = 'test.mosquitto.org'
mqttport = 1883

#topics to publish to living room
topic = "kitchen/fire"
topic2 = "kitchen/light"
topic3 = "kitchen/motion"

#Values to send to living room
light = 0
fire = 0
motion = 0

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, mqttport)
    return client


def publish(client):
    while True:
        time.sleep(0.1) # 0.1 seconds interval
    
        try:
            GPIO.add_event_detect(firePin, GPIO.BOTH, bouncetime=300) #flame sensor detection
            while (1):
                #publish motion data to living room
                if GPIO.input(pirPin) == 1: # There is motion detected
                    print("Motion detected!")
                    motion = 1
                    result1 = client.publish(topic3, motion)
                    if result1[0] == 0: #If successful
                        print(f"Send `{motion}` to topic `{topic3}`")
                    else:
                        print("Motion message did not publish")

                    #if light is not detected in the kitchen
                    if GPIO.input(lightPin) == 0:
                        light = 1 #Set light value to 1 (On the light because motion is detected)
                        print("Motion detected, turning lights on")
                        GPIO.output(led1, GPIO.HIGH) #Switch on LED (kitchen light)
                        result1 = client.publish(topic2, light)
                        if result1[0] == 0:
                            print(f"Send `{light}` to topic `{topic2}`")
                        
                        else:
                            print("Light message did not publish")

                    else:
                        print("Room light is already on")
                        print("LED is already on")
                        light = 0
                        result1 = client.publish(topic2, light)
                        if result1[0] == 0:
                            print(f"Send `{light}` to topic `{topic2}`")
                        
                        else:
                            print("Light message did not publish")


                else: #if no motion
                    print("No Motion Detected!")
                    motion = 0 #0
                    result1 = client.publish(topic3, motion)
                    if result1[0] == 0: #If successful
                        print(f"Send `{motion}` to topic `{topic3}`")
                    else:
                        print("Motion message did not publish")

                    if GPIO.input(lightPin) == 1: #Light is on
                        light = 0
                        print("Motion not detected, turning lights off")
                        print("LED OFF")
                        GPIO.output(led1, GPIO.LOW) #Switch off LED (kitchen light)
                        result1 = client.publish(topic2, light)
                        if result1[0] == 0:
                            print(f"Send `{light}` to topic `{topic2}`")
                        
                        else:
                            print("Light message did not publish")
                    else: #light is off
                        light = 0
                        result1 = client.publish(topic2, light)
                        if result1[0] == 0:
                            print(f"Send `{light}` to topic `{topic2}`")
                        
                        else:
                            print("Light message did not publish")
                        

                    #if fire is detected but no motion
                    if GPIO.event_detected(firePin): #return true / false
                        time.sleep(0.1)
                        print("Flame Detected!")
                        fire = 1
                        print("Buzzer on")
                        GPIO.output(buzzerled, GPIO.HIGH)
                        
                        result1 = client.publish(topic, fire)
                        if result1[0] == 0:
                            print(f"Send `{fire}` to topic `{topic}`")
                        else:
                            print("Fire message did not publish")

                    else:
                        print("Fire is off and no motion detected, no safety hazard")
                        fire = 0 #Fire is off
                        GPIO.output(buzzerled, GPIO.LOW) #Stop the buzzer 

                        result1 = client.publish(topic, fire)
                        
                        if result1[0] == 0:
                            print(f"Send `{fire}` to topic `{topic}`")
                        else:
                            print("Fire message did not publish")
                                    
                time.sleep(0.1)
                

        except KeyboardInterrupt:
            print("Quit")
            GPIO.cleanup()


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()