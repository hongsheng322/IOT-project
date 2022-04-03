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
topic1 = "kitchen/fire"
topic2 = "kitchen/light"
topic3 = "kitchen/motion"

#variables for sensors to update gpio values
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

# SOCKET====================================================
host, port = "192.168.1.129", 42069
BUFFER_SIZE = 1024 #Buffer size of 1024 bytes

# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
sock.bind((host, port))
print("listening")

def socketServer():
    global firestatus
    global motion1
    global motion2
    global light1
    global light2

    while True:
    
       #send to SOCKET CLIENTS
        time.sleep(0.1) #sleep 0.1 sec
        bytesAddressPair = sock.recvfrom(BUFFER_SIZE)

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        # print(clientMsg)
        # print(clientIP)

        #message to send to client
        message = "fire," + str(firestatus)
        bytesToSend = str.encode(message)

        # Sending a reply to client
        sock.sendto(bytesToSend, address)

        #message to send to client
        # print(str(light1))
        message = "light1," + str(light1)
        bytesToSend  = str.encode(message)
        # print(message)

        # Sending a reply to client
        sock.sendto(bytesToSend, address)

        message = "light2," + str(light2)
        bytesToSend  = str.encode(message)

        # Sending a reply to client
        sock.sendto(bytesToSend, address)


        #message to send to client
        message = "motion1," + str(motion1)
        bytesToSend  = str.encode(message)
        # print(message)

        #message to send to client
        message = "motion2," + str(motion2)
        bytesToSend  = str.encode(message)

        # Sending a reply to client
        sock.sendto(bytesToSend, address)

        
#============================================================


#MQTT======================================================
broker = 'test.mosquitto.org'
mqttport = 1883
topic = "python/mqtt"

def connect_mqtt() -> mqtt_client:
    def on_connect(mqttclient, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    mqttclient = mqtt_client.Client("Living_rm_PI")
    mqttclient.on_connect = on_connect
    mqttclient.connect(broker, mqttport)
    return mqttclient

def subscribe(mqttclient: mqtt_client):
    def on_message(mqttclient, userdata, msg):
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


        if msg.topic == "kitchen/light":
            light2 = int(msg.payload.decode())
            if light2 == 1:
                print("Light detected in the kitchen.")
            else:
                print("No light detected in the kitchen.")
                light2 = 0
                

        try:
            
            if GPIO.input(pirPin) == 1: #If motion is detected
                motion1 = 1
                print("Motion Detected!")
                print("Lights On!")
                light1 = 1
                GPIO.output(led1, GPIO.HIGH) #Switch on room light
                

            else:    
                print("No motion detected. Turning lights off")
                GPIO.output(led1, GPIO.LOW)
                motion1 = 0
                light1 = 0

        except KeyboardInterrupt:
            GPIO.cleanup()    
    
    mqttclient.subscribe(topic)
    mqttclient.subscribe(topic1)
    mqttclient.subscribe(topic2)
    mqttclient.subscribe(topic3)
    mqttclient.on_message = on_message

def mqttrun():
    mqttclient = connect_mqtt()
    subscribe(mqttclient)
    mqttclient.loop_forever()
#==========================================================

#for testing only
def boolflip(value):
    #global firestatus
    value = 1 - value
    firestatus = value
    return value

def boolflip2(value):
    #global light1
    # value = 1 - value
    light1 = value
    return value

def boolflip3(value):
    #global motion1
    # value = 1 - value
    motion1 = value
    return value

def YEET():
    while True:
        boolflip(firestatus)
        print(firestatus)
        time.sleep(0.5)
        #print("YEET!")

def YOINK():
    while True:
        print(firestatus)
        time.sleep(0.5)
        #print("YOINK!")

class mqttThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        mqttrun()

class socketThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        #YOINK()
        socketServer()

lock = threading.Lock()
mqttThread()
socketThread()
while True:
    pass
