import socket
import threading
import time

class ServerConnection:
    def __init__(self, port):
        self.connections = []
        self.sock = socket.socket()
        self.port = port
        self.sock.bind(('', port))

    def add_connection(self):
        self.sock.listen(5)
        conn, addr = self.sock.accept()
        print(f"Connected by {addr}")

        # Only add if not already in list
        if conn not in self.connections:
            self.connections.append(conn)
            threading.Thread(target=self.receive_data, args=(conn,), daemon=True).start()
        else:
            print("Connection already exists. Ignored.")

    def send_data(self, data):
        message = (str(data) + ";").encode()
        for conn in self.connections:
            try:
                conn.sendall(message)
            except:
                print(f"Client{self.connections.index(conn)} connection failed to send. Skipping.")

    def receive_data(self, conn):
        connid = self.connections.index(conn)
        buffer = ""
        while True:
            try:
                char = conn.recv(1).decode()
                if not char:
                    break
                if char == ";":
                    print(f"\x1b[1A\x1b[2K{connid},{buffer}")
                    buffer = ""
                else:
                    buffer += char
            except:
                break

server = ServerConnection(12345)
num_clients = 2 #int(input("How many connections wanted?\n>> "))
while len(server.connections) < num_clients:
    server.add_connection()
print("Connections established. Server started. Ctrl+C to stop.\n")

'''
try:
    while True:
        server.send_data("0,0,1,1,2,2")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nServer stopped.")
    '''