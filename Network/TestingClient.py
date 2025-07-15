import socket
import threading

def receive_messages(sock):
    buffer = ""
    while True:
        char = sock.recv(1).decode()
        if not char:
            break
        if char == ";":
            print(f"Server says: {buffer}")
            buffer = ""
        else:
            buffer += char

s = socket.socket()
s.connect(('localhost', 12345))

# Start receiver in background
threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

# Input loop to send data
print("You can now type messages to send to the server:")
while True:
    msg = input()
    s.sendall((msg + ";").encode())
