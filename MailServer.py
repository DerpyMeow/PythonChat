import socket
import threading


class MailServer:
    def __init__(self, port=18706):
        self.clients = {}  # dictionary to store connected clients
        self.messages = {}  # dictionary to store unsent messages
        self.lock = threading.Lock()  # lock to ensure thread safety
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('136.56.138.137', port))
        self.server.listen()
        print(f'Server started on port {port}')

    def start(self):
        while True:
            client_socket, address = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        # receive the client's user id
        user_id = client_socket.recv(1024).decode()

        # check if the user is already connected
        with self.lock:
            if user_id in self.clients:
                print(f'{user_id} is already connected')
                self.clients[user_id].close()

            # store the new client socket
            self.clients[user_id] = client_socket

        # handle any unsent messages for this user
        with self.lock:
            if user_id in self.messages:
                for message in self.messages[user_id]:
                    self.send_message(client_socket, message, 'old')
                del self.messages[user_id]

        # continuously receive and handle messages from this client
        while True:
            try:
                recipient_id, message = client_socket.recv(1024).decode().split(':')
            except:
                # client has disconnected
                with self.lock:
                    print(f'{user_id} disconnected')
                    del self.clients[user_id]
                break

            if recipient_id in self.clients:
                # recipient is connected, send the message
                with self.lock:
                    self.send_message(self.clients[recipient_id], f'{user_id}:{message}', 'new')
            else:
                # recipient is not connected, store the message
                with self.lock:
                    if recipient_id not in self.messages:
                        self.messages[recipient_id] = []
                    self.messages[recipient_id].append(f'{user_id}:{message}')

    def send_message(self, client_socket, message, tag):
        client_socket.send(f'{tag}:{message}'.encode())


if __name__ == '__main__':
    MailServer().start()
