import socket
import threading

class ClientListener(threading.Thread):
    def init(self, client, addr):
        threading.Thread.init(self)
        self.client = client
        self.addr = addr

    def run(self):
        try:
            while True:
                data = self.client.recv(1024).decode()
                if not data:
                    break

                print(f'{self.addr}: {data}')

                # Check if the username is unique
                if data.startswith('USERNAME: '):
                    username = data[10:]

                    # Check if the username is already in use
                    if username in usernames:
                        self.client.send('ERROR: Username already in use\n'.encode())
                    else:
                        usernames.add(username)
                        self.client.send('USERNAME ACCEPTED\n'.encode())
                        print(f'User {username} has joined the chat')

                # Check if the phone number is unique
                elif data.startswith('PHONE NUMBER: '):
                    phone_number = data[14:]

                    # Check if the phone number is already in use
                    if phone_number in phone_numbers:
                        self.client.send('ERROR: Phone number already in use\n'.encode())
                    else:
                        phone_numbers.add(phone_number)
                        self.client.send('PHONE NUMBER ACCEPTED\n'.encode())
                        print(f'User with phone number {phone_number} has joined the chat')

                else:
                    for client in clients:
                        if client != self.client:
                            client.send(f'{self.addr}: {data}'.encode())

        finally:
            self.client.close()

def main():
    host = 'localhost'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)

    clients = []
    usernames = set()
    phone_numbers = set()

    try:
        while True:
            client, addr = server.accept()
            clients.append(client)
            print(f'Client connected: {addr}')

            listener = ClientListener(client, addr)
            listener.start()

    finally:
        server.close()

if _name_ == '_main_':
    main()