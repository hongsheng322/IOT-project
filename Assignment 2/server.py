import threading
import socket
import os
import time

host = '127.0.0.1' #Running on localhost (no server)

server = input("Please enter the listening port: ")
#127.0.0.1 33333

server_arr = server.split(" ")

nickname = "Server"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, int(server_arr[1])))
server.listen() #Start listening for incoming ports

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IP, SOCK_STREAM = TCP
client.connect((server_arr[0], int(server_arr[1]))) #localhost

BUFFER_SIZE = 1024 #Buffer size of 1024 bytes

clients = [] #List of clients
nicknames = [] #List of nicknames

def broadcast(message): #Pass in a message
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024) #Try to receive a message from client (up to 1024 bytes)
            temp = message.decode('ascii') #Decode message
            index = clients.index(client)
            nickname = nicknames[index]
            if "LIST images" in temp and nickname != "Server": 
                arr = os.listdir('./images')
                for i in arr:
                    time.sleep(0.05)
                    client.send(i.encode('ascii'))

            elif "DOWNLOAD" in temp and nickname != "Server":
                split_arr = temp.split(' ') #Split up the message with space delimiter

                file_name = './images/' + split_arr[3] #Concatenate file name into string
                file = open(file_name, 'rb')  # rb is read-binary

                chunks = 0
                l = file.read(BUFFER_SIZE)
                while l:
                    l = file.read(BUFFER_SIZE)
                    chunks += 1 #To get the number of chunks required to send the image file
                file.close()

                message = 'SENDINGCHUNKS'.encode('ascii')
                client.send(message)

                message_chunks = str(chunks).encode('ascii')
                client.send(message_chunks) #Send the number of chunks to the client

                file = open(file_name, 'rb')
                image_data = file.read(BUFFER_SIZE)

                while image_data: #Send image_data in chunks
                    client.send(image_data)
                    image_data = file.read(BUFFER_SIZE)

                file.close()


            else:
                broadcast(message) #If received, then broadcast this message to all other clients

        except:
            index = clients.index(client) #Obtain the index of the client
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break #Break out of the loop

def receive():
    while True:
        client, address = server.accept(); #Accept incoming client at any given time
        print(f"Connected with {str(address)}") #When a new client has connected to the server
        client.send('NICK'.encode('ascii')) #Prompt client for the nickname
        nickname = client.recv(1024).decode('ascii') #Server receive the nickname from the client

        nicknames.append(nickname) #Add it to the list of nicknames
        clients.append(client) #Add it to the list of clients

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} has joined the chat!'.encode('ascii'))
        #To broadcast to the rest of the clients that a new client has joined the server
        client.send('Connected to the server! Start chatting. '.encode('ascii')) #Let the client know that they are connected

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

def write():
    while True:
        message = f'{nickname} > {input("")}' #Constantly waiting for new messages
        client.send(message.encode('ascii'))

def receive_message():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error has occurred!")
            client.close()
            break

print("Server is listening...")


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

receive()









