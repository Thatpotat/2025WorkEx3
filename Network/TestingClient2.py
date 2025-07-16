import socket
import threading
import keyboard
import time

stopflag = False

def receive_messages(sock):
    global stopflag
    buffer = ""
    while not stopflag:
        try:
            char = sock.recv(1).decode()
        except ConnectionResetError:
            print("\nServer closed.")
            stopflag = True
            exit()
        if not char:
            break
        if char == ";":
            print("\x1b[1A\x1b[2K"+buffer)
            buffer = ""
        else:
            buffer += char

s = socket.socket()
s.connect(('localhost', 12345))

# Start receiver in background
threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

# Input loop to send data
print("You can now type messages to send to the server:")
try:
    while True:
        if stopflag:
            exit()
        if keyboard.is_pressed("="):
            s.sendall("0;".encode())
        if keyboard.is_pressed("-"):
            s.sendall("1;".encode())
        if not (keyboard.is_pressed("=") or keyboard.is_pressed("-")):
            s.sendall("2;".encode()) 
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nClient stopped.")
