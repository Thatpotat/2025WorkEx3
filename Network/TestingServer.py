import socket
import threading
import time

class ServerConnection:
    do_recv:bool
    def __init__(self, port, limit = 2):
        self.do_recv = False
        self.lim = limit
        self.connections = []
        self.sock = socket.socket()
        self.port = port
        self.sock.bind(('', port))
        while len(self.connections) < self.lim:
            self.add_connection()

    def add_connection(self):
        self.sock.listen(5)
        conn, addr = self.sock.accept()
        if len(self.connections) >= self.lim:
            print("Connection limit reached. Ignoring new connection.")
            conn.close()
            return
        print(f"Connected by {addr}")

        if conn not in self.connections:
            self.connections.append(conn)
            threading.Thread(target=self.receive_data, args=(conn,), daemon=True).start()
        else:
            print("Connection already exists. Ignored.")
            conn.close()
        
        if len(self.connections) == self.lim:
            self.do_recv = True

    def send_data(self, data):
        message = (str(data) + ";").encode()
        for conn in self.connections:
            try:
                conn.sendall(message)
            except:
                print(f"\x1b[2K\rClient{self.connections.index(conn)} connection failed to send. Skipping.")

    def receive_data(self, conn):
        connid = self.connections.index(conn)
        buffer = ""
        while not self.do_recv:
            pass
        while True:
            try:
                char = conn.recv(1).decode()
                if not char:
                    break
                if char == ";":
                    print(f"\r\x1b[2K{connid},{buffer}", end="", flush=True)
                    buffer = ""
                else:
                    buffer += char
            except:
                break
        print(f"\r\x1b[2K", end="")
        print(f"Client{connid} has disconnected.")
        try:
            self.connections.remove(conn)
        except ValueError:
            pass
        conn.close()

server = ServerConnection(12345, 2)
print("Connections established. Server started. Ctrl+C to stop.\n")
time.sleep(0.1)
if __name__ == "__main__":
    try:
        while True:
            server.send_data("0,0,1,1,2,2")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nServer stopped.")