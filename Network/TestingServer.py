import socket
import keyboard
import time
import threading

class server_connection_out():
    def __init__(self, port):
        self.connections = []
        self.s = socket.socket()
        self.p = port
        self.s.bind(('', port))
    
    def add_connection(self):
        self.s.listen(5)
        newconnection = self.s.accept()
        print(newconnection[1])
        if not newconnection[0] in self.connections:
            self.connections.append(newconnection[0])

    def send_data(self, dat):
        i:socket
        dat = str(dat).encode()
        for i in self.connections:
            i.send(dat)
    
    def get_connections(self):
        return self.connections

s = server_connection_out(12345)
i = 0
num_connections = int(input("How many connections wanted?\n>> "))
while len(s.get_connections()) < num_connections:
    s.add_connection()
while True:
    if keyboard.is_pressed("up_arrow"):
        i += 1
        s.send_data(i)
    if keyboard.is_pressed("down_arrow"):
        i -= 1
        s.send_data(i)
    time.sleep(0.1)