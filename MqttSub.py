from multiprocessing.sharedctypes import Value
import socket
import time
from paho.mqtt import client as mqtt_client
from threading import Thread
import threading
import RPi.GPIO as GPIO
import math

broker = 'test.mosquitto.org'
mqttport = 1883
topic = "kitchen/fire"
topic2 = "kitchen/light"
topic3 = "kitchen/motion"


firestatus = 0
light1 = 0
light2 = 0
motion1 = 0
motion2 = 0

light_room = 5
led1 = 17
pirPin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(light_room,GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(pirPin, GPIO.IN)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("Living_rm_PI")
    client.on_connect = on_connect
    client.connect(broker, mqttport)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global firestatus
        global motion1
        global motion2
        global light1
        global light2
        
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        if msg.topic == "kitchen/fire":
            fire = int(msg.payload.decode()) #Retrieve the value sent by the publisher (kitchen)
            print("The value of fire is " + str(fire))
            if fire == 1: #If fire is detected and no motion, the buzzer will sound
                print("Fire left unattended in kitchen. Sounding buzzer now")
                firestatus = 1
                GPIO.setup(2,GPIO.OUT)
                p = GPIO.PWM(2, 50)
                p.start(50)
                for x in range(0, 30):
                    sinVal = math.sin(x*(math.pi / 180.0))
                    toneVal = 2000 + sinVal * 750
                    p.ChangeFrequency(toneVal)
                    time.sleep(0.1)

        if msg.topic == "kitchen/motion":
            motion2 = int(msg.payload.decode())
            if motion2 == 1:
                print("Motion detected in the kitchen. Turning kitchen lights on")
                GPIO.output(led1, GPIO.HIGH) #Turn on the kitchen LED

            else:
                print("No motion detected in the kitchen. Turning kitchen lights off")
                motion2 = 0
                GPIO.output(led1, GPIO.LOW)
            
        try:
            if GPIO.input(pirPin) == 1: #If motion is detected
                motion1 = 1
                print("Motion Detected!")
                print("Lights On!")
                light1 = 1
                GPIO.output(light_room, GPIO.HIGH) #Switch on room light
                

            else:    
                print("No motion detected. Turning lights off")
                GPIO.output(light_room, GPIO.LOW)
                light1 = 0

        except KeyboardInterrupt:
            GPIO.cleanup()    

    client.subscribe(topic)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()