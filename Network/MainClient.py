import socket
import threading
import keyboard
import time
import sys

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.stopflag = False

    def receive_messages(self):
        buffer = ""
        while not self.stopflag:
            try:
                char = self.sock.recv(1).decode()
            except ConnectionResetError:
                print("\nServer closed.")
                self.stopflag = True
                sys.exit()
            if not char:
                break
            if char == ";":
                # Parse and display game state
                try:
                    p1x, p1y, p2x, p2y, bx, by, s1, s2 = map(float, buffer.split(","))
                    print(f"\rP1:({p1x:.0f},{p1y:.0f})  P2:({p2x:.0f},{p2y:.0f})  Ball:({bx:.0f},{by:.0f})  Score:{int(s1)}:{int(s2)}           ", end="")
                except Exception as e:
                    print(f"\nParse error: {e}")
                buffer = ""
            else:
                buffer += char

    def run(self):
        self.sock.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages, daemon=True).start()
        print("Connected to server. Press Ctrl+C to stop.\n")
        try:
            while True:
                if self.stopflag:
                    sys.exit()
                # 0 = down, 1 = up, 2 = none
                if keyboard.is_pressed("up"):
                    self.sock.sendall("1;".encode())
                elif keyboard.is_pressed("down"):
                    self.sock.sendall("0;".encode())
                else:
                    self.sock.sendall("2;".encode())
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nClient stopped.")

if __name__ == "__main__":
    client = Client()
    client.run()