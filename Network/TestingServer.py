import socket
import threading
import keyboard

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
                print("A connection failed to send. Skipping.")

    def receive_data(self, conn):
        buffer = ""
        while True:
            try:
                char = conn.recv(1).decode()
                if not char:
                    break
                if char == ";":
                    print(f"Client says: {buffer}")
                    buffer = ""
                else:
                    buffer += char
            except:
                break

server = ServerConnection(12345)
num_clients = int(input("How many connections wanted?\n>> "))
while len(server.connections) < num_clients:
    server.add_connection()

print("Use ↑ or ↓ arrow keys to send messages. Ctrl+C to stop.")
counter = 0
try:
    while True:
        if keyboard.is_pressed("up"):
            counter += 1
            server.send_data(f"UP {counter}")
            while keyboard.is_pressed("up"):
                pass

        if keyboard.is_pressed("down"):
            counter -= 1
            server.send_data(f"DOWN {counter}")
            while keyboard.is_pressed("down"):
                pass
except KeyboardInterrupt:
    print("\nServer stopped.")