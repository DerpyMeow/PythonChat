import tkinter as tk
import socket

SERVER_IP = "136.56.138.137"
SERVER_PORT = 18705

class ChatApp:

    def __init__(self, master, password):
        self.master = master
        master.title("Chat App")

        self.message_listbox = tk.Listbox(master, width=50, height=10)
        self.message_listbox.pack()

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack()

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        self.password = password

        # connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))

        # authenticate with the server
        self.authenticate()

    def authenticate(self):
        # send password to the server
        self.client_socket.sendall(self.password.encode('utf-8'))

        # receive response from the server
        response = self.client_socket.recv(1024).decode('utf-8')
        print(response)

        if response == 'Incorrect password':
            self.master.quit()

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.message_listbox.insert(tk.END, message)

        # send message to the server
        self.client_socket.sendall(message.encode('utf-8'))

        # receive response from the server
        response = self.client_socket.recv(1024).decode('utf-8')
        print(response)

    def __del__(self):
        # close the socket when finished
        self.client_socket.close()

# prompt for password
password = input("Enter the password for the chat: ")
if password != "1234":
    print("Incorrect password")
else:
    # start the chat app
    root = tk.Tk()
    app = ChatApp(root, password)
    root.mainloop()
