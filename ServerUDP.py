from multiprocessing.sharedctypes import Value
import socket
import time

host, port = "127.0.0.1", 25001
BUFFER_SIZE = 1024 #Buffer size of 1024 bytes

# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
sock.bind((host, port))
print("listening")

#variables for sensors to update gpio values
firestatus = 1
light1 = 0
light2 = 1
motion1 = 0
motion2 = 0

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

while True:
   
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

