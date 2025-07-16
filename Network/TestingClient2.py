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
                print("\x1b[1A\x1b[2K" + buffer)
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
                if keyboard.is_pressed("up"):
                    self.sock.sendall("0;".encode())
                if keyboard.is_pressed("down"):
                    self.sock.sendall("1;".encode())
                if not (keyboard.is_pressed("up") or keyboard.is_pressed("down")):
                    self.sock.sendall("2;".encode())
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nClient stopped.")

if __name__ == "__main__":
    client = Client()
    client.run()
