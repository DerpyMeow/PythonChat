import socket

HOST = ''  # all available interfaces
PORT = 18705  # arbitrary non-privileged port

# create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# listen for incoming connections
server_socket.listen(1)
print(f'Chat server is running on port {PORT}')

# wait for a client to connect
client_socket, client_address = server_socket.accept()
print(f'Connected to {client_address[0]}:{client_address[1]}')

# receive and send messages
while True:
    message = client_socket.recv(1024).decode('utf-8')
    print(f'Received message: {message}')
    response = f'Received message: {message}'
    client_socket.sendall(response.encode('utf-8'))

# close the socket when finished
client_socket.close()
