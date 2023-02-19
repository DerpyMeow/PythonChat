import socket
import threading
import time

SERVER_HOST = '136.56.138.137'  # The server's hostname or IP address
SERVER_PORT = 18705        # The port used by the server


def receive_messages(sock):
    while True:
        message = sock.recv(1024).decode('utf-8')
        print(message)


def send_message(sock, message):
    sock.sendall(message.encode('utf-8'))


def connect_to_server(password):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect((SERVER_HOST, SERVER_PORT))

    # Send the password to the server
    sock.sendall(password.encode('utf-8'))

    # Start a separate thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()

    return sock


def main():
    # Get the password from the user
    password = input('Enter password: ')

    # Connect to the server
    sock = connect_to_server(password)

    # Send messages to the server
    while True:
        message = input('> ')
        send_message(sock, message)


if __name__ == '__main__':
    main()
