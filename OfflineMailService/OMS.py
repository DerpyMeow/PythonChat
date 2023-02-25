import socket
import os.path

# Define server IP and port'
SERVER_IP = "136.56.138.137"
SERVER_PORT = 18706

# Define the path to the user ID file
USERID_FILE = "userid.txt"

# Define the maximum message size in bytes
MAX_MSG_SIZE = 1024

# Define the encoding to use for sending and receiving messages
ENCODING = "utf-8"

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Check if the user ID file exists and read the user ID from it
if os.path.isfile(USERID_FILE):
    with open(USERID_FILE, "r") as f:
        user_id = f.read().strip()
else:
    user_id = None

# Try to connect to the server
try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
except ConnectionRefusedError:
    print("Error: Could not connect to server.")
    exit()

# If the user does not have a user ID, request one from the server
if user_id is None:
    # Send a message to the server requesting a new user ID
    request_message = "NEW_USER_ID"
    client_socket.send(request_message.encode(ENCODING))

    # Receive the new user ID from the server
    response = client_socket.recv(MAX_MSG_SIZE).decode(ENCODING)

    if response.startswith("USER_ID"):
        # Save the new user ID to the user ID file
        user_id = response.split()[1]
        with open(USERID_FILE, "w") as f:
            f.write(user_id)

        # Print the new user ID to the user
        print(f"Your user ID is {user_id}.")
    else:
        print("Error: Invalid response from server.")
        exit()

# If the user already has a user ID, send it to the server
else:
    # Send a message to the server with the user ID and the client's IP address
    request_message = f"EXISTING_USER_ID {user_id}"
    client_socket.send(request_message.encode(ENCODING))

# Loop to send and receive messages
while True:
    # Get the recipient and message from the user
    recipient = input("Enter recipient's user ID (or 'q' to quit): ")
    if recipient == "q":
        break
    message = input("Enter message: ")

    # Send the message to the server
    send_message = f"SEND_MESSAGE {user_id} {recipient} {message}"
    client_socket.send(send_message.encode(ENCODING))

    # Receive a response from the server
    response = client_socket.recv(MAX_MSG_SIZE).decode(ENCODING)

    # If the message was successfully sent, print a confirmation message
    if response == "MESSAGE_SENT":
        print("Message sent!")
    else:
        print(f"Error: {response}")

# Close the socket
client_socket.close()
