import socket
import threading

testing = False
password =input("Please input the password: ")

if password == "SongOfAnatomy":

    nickname = input("Choose a nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('136.56.138.137', 18705))


    def receive():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print("An Error Occurred!")
                client.close()
                break


    def write():
        while True:
            message = input("")
            message_with_nick = f'{nickname}: {message}'
            client.send(message_with_nick.encode('ascii'))


    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


elif password == "1234" and testing == True:

    nickname = input("Choose a nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('136.56.138.137', 18705))


    def receive():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message+" \n")
            except:
                print("An Error Occurred!")
                client.close()
                break


    def write():
        while True:
            message = input("")
            message_with_nick = f'{nickname}: {message}'
            client.send(message_with_nick.encode('ascii'))


    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


else:
    input("Incorrect Password. Please close and try again. Press any key to exit: ")
