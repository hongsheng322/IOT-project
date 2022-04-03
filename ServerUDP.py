from multiprocessing.sharedctypes import Value
import socket
import time
from paho.mqtt import client as mqtt_client
from threading import Thread

#variables for sensors to update gpio values
firestatus = 1
light1 = 0
light2 = 1
motion1 = 0
motion2 = 0

# SOCKET====================================================
host, port = "192.168.1.148", 42069
BUFFER_SIZE = 1024 #Buffer size of 1024 bytes

# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
sock.bind((host, port))
print("listening")

def socketServer():
    while True:
       #send to SOCKET CLIENTS
        time.sleep(0.5) #sleep 0.5 sec
        bytesAddressPair = sock.recvfrom(BUFFER_SIZE)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        #message to send to client
        message = "fire," + str(boolflip(firestatus))
        bytesToSend  = str.encode(message)

        # Sending a reply to client
        sock.sendto(bytesToSend, address)

        #message to send to client
        message = "light1," + str(boolflip2(light1))
        bytesToSend  = str.encode(message)

        # Sending a reply to client
        sock.sendto(bytesToSend, address)

            #message to send to client
        message = "motion1," + str(boolflip3(motion1))
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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    mqttclient.subscribe(topic)
    mqttclient.on_message = on_message

def mqttrun():
    mqttclient = connect_mqtt()
    subscribe(mqttclient)
    mqttclient.loop_forever()
#==========================================================

#for testing only
def boolflip(value):
    global firestatus
    value = 1 - value
    firestatus = value
    return value

def boolflip2(value):
    global light1
    value = 1 - value
    light1 = value
    return value

def boolflip3(value):
    global motion1
    value = 1 - value
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


mqttThread()
socketThread()
while True:
    pass
