import socket
import threading

# Chat Server
# Broadcast every message to others.
# S ---- c1
# S ---- c2
class ChatServer:
    def __init__(self, ip:str, port:int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.clients = []

    def accept(self):
        conn, addr = self.server_socket.accept()
        print(f"client {addr} is connected")
        return conn
    
    def clientHandler(self, conn:socket):
        left = False
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                self.broadcast(data, conn)
                '''
                print(data.decode())
                '''
            except ConnectionResetError:
                self.clients.remove(conn)
                conn.close()
                print(f"A Client disconnected and information: {conn}")
                self.broadcast('someone:left!'.encode())
                break

    def broadcast(self, data:bytes, conect = None)->None:
        name, data= data.decode().split(':')[0], data.decode().split(':')[1]
        m = name + ': ' + data
        m = m.encode()
        for client in self.clients:
            if client != conect:
                try:
                    client.send(m)
                except:
                    pass
    def start(self)->None:
        while True:
            client = self.accept()
            self.clients.append(client)
            clientHandlerThead =threading.Thread(target=self.clientHandler, args=(client,))
            clientHandlerThead.start()
        
            

IP_Address = socket.gethostbyname(socket.gethostname())
server = ChatServer(IP_Address, 54321)
server.start()
