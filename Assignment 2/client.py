# Python program to implement client side of chat room.
import socket
import threading

nickname = input("Please enter your nickname: ")

server = input("Please enter IP address and port: ")

server_arr = server.split(" ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IP, SOCK_STREAM = TCP
client.connect((server_arr[0], int(server_arr[1]))) #localhost

BUFFER_SIZE = 1024

def receive():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('ascii')

            if message == 'NICK':
                client.send(nickname.encode('ascii'))

            if message == 'SENDINGCHUNKS':
                number_chunks = int(client.recv(1024).decode('ascii')) #Convert the number of chunks to integer from String
                file = open('downloaded/downloaded_image.png', 'wb')

                # This is because TCP/IP transfers in streams

                while number_chunks > 0:
                    image_chunk = client.recv(BUFFER_SIZE)

                    file.write(image_chunk)
                    number_chunks -= 1

                print("Image Downloaded Successfully")

                file.close()

            else:
                print(message)


        except:
            print("An error has occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname} > {input("")}' #Constantly waiting for new messages
        client.send(message.encode('ascii'))






receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
