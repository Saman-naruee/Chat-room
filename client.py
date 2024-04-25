import socket
import threading
class ChatClient:
    def __init__(self, server_ip:str, server_port:int):
        self.server_socket_address = (server_ip, server_port)
        
    def connect(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(self.server_socket_address)

    def sending_loop(self):
        self.name = input('enter your name: ')
        while True:
            try:
                message = input()
                if message == 'leave':
                    print('You are left!')
                    self.server_socket.send(f"{self.name}: {'Good bye everyone:)'}".encode())
                    break
                self.server_socket.send(f'{self.name}:{message}'.encode())
            except:
                self.server_socket.close()
    def receiving_loop(self):   
        while True:   
            try:    
                data = self.server_socket.recv(1024)
                if not data:
                    break
                name, data = data.decode().split(': ')[0], data.decode().split(': ')[1]
                print(f'{name}: {data}')
            except ConnectionResetError:
                print('server lost!')
                self.server_socket.close()
                break
            

    def start(self):
        self.connect()
        sending_loop = threading.Thread(target=self.sending_loop)
        sending_loop.start()
        self.receiving_loop()

IP_Address = socket.gethostbyname(socket.gethostname())
client = ChatClient(IP_Address, 54321)
client.start()

"""
import socket
import threading

class Client:
    def __init__(self, ip: str, port: int, name: str):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.name = name
        self.connected = False

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            print(f"Connected to the server as {self.name}")
            # Send the client's name to the server
            self.client_socket.send(self.name.encode())
        except Exception as e:
            print(f"Failed to connect to the server: {e}")

    def send_message(self, message: str):
        if self.connected:
            try:
                self.client_socket.send(message.encode())
            except Exception as e:
                print(f"Failed to send message: {e}")

    def receive_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(data.decode())
            except Exception as e:
                print(f"Failed to receive messages: {e}")
                self.connected = False

    def start_receiving(self):
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

# Example usage:
if __name__ == "__main__":
    # Replace 'localhost' and 'YourName' with the server IP and your name
    client = Client('localhost', 54321, 'YourName')
    client.connect()
    client.start_receiving()
    while True:
        msg = input("Enter message: ")
        if msg.lower() == 'exit':
            break
        client.send_message(msg)

"""