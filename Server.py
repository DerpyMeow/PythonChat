import socket
import threading
import time

HOST = ''  # all available interfaces
PORT = 18705  # arbitrary non-privileged port
PASSWORD = "1234" # set your server password here


# create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# listen for incoming connections
server_socket.listen()
print(f'Chat server is running on port {PORT}')

# list to keep track of all connected clients
clients = []

def handle_client(client_socket, client_address):
    # ask for password
    client_socket.sendall("PASSWORD".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8')
    if password != PASSWORD:
        print(f"Wrong password entered by {client_address[0]}:{client_address[1]}")
        client_socket.close()
        return


    # add the client to the list of connected clients
    clients.append(client_socket)
    print(f'Connected to {client_address[0]}:{client_address[1]}')

    # receive and send messages
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(f'Received message: {message}')

        # send the message to all other clients
        for c in clients:
            if c != client_socket:
                c.sendall(message.encode('utf-8'))

# wait for clients to connect
while True:
    client_socket, client_address = server_socket.accept()

    # start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()

# close the socket when finished
server_socket.close()
