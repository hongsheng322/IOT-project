import threading
import socket

host = '127.0.0.1' #Running on localhost (no server)

port = 33333

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() #Start listening for incoming ports

clients = [] #List of clients
nicknames = [] #List of nicknames

def broadcast(message): #Pass in a message
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024) #Try to receive a message from client (up to 1024 bytes)
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

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()


