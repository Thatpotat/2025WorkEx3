import socket
import threading
import keyboard
import time
import sys
import math

import pygame

pygame.init()

class Paddle:
    def __init__(self, x, y, width, height, colour):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.score = 0
        self.speed = 3
        self.colour = colour

class Ball:
    def __init__(self, x, y, width, height, direction):
        self.starting_pos = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.direction = direction

player1 = Paddle(10, 150, 11, 100, (0, 255, 0))
player2 = Paddle(780, 150, 11, 100, (255, 0, 0))
ball = Ball(400, 200, 20, 20, 45)

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.stopflag = False

        # Get display info for scaling
        info = pygame.display.Info()
        self.display_width = info.current_w
        self.display_height = info.current_h

        # Reference game resolution
        self.ref_width = 800
        self.ref_height = 400

        # Calculate scale factors
        self.scale_x = self.display_width / self.ref_width
        self.scale_y = self.display_height / self.ref_height

        # Game state variables
        self.p1x = 10
        self.p1y = 150
        self.p2x = 780
        self.p2y = 150
        self.bx = 400
        self.by = 200
        self.s1 = 0
        self.s2 = 0

        # Pygame setup (borderless fullscreen)
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_width, self.display_height), pygame.NOFRAME)
        pygame.display.set_caption("Pong Client")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, int(50 * self.scale_y))

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
                # Parse and update game state
                try:
                    self.p1x, self.p1y, self.p2x, self.p2y, self.bx, self.by, self.s1, self.s2 = map(float, buffer.split(","))
                except Exception as e:
                    print(f"\nParse error: {e}")
                buffer = ""
            else:
                buffer += char

    def draw(self):
        self.screen.fill((3, 161, 252))
        # Draw Paddles
        pygame.draw.rect(
            self.screen, player1.colour,
            (self.p1x * self.scale_x, self.p1y * self.scale_y, player1.width * self.scale_x, player1.height * self.scale_y)
        )
        pygame.draw.rect(
            self.screen, player2.colour,
            (self.p2x * self.scale_x, self.p2y * self.scale_y, player2.width * self.scale_x, player2.height * self.scale_y)
        )
        # Draw ball
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (self.bx * self.scale_x, self.by * self.scale_y, ball.width * self.scale_x, ball.height * self.scale_y)
        )
        # Draw score
        text = self.font.render(f"{int(self.s1)} : {int(self.s2)}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.display_width // 2, int(20 * self.scale_y)))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def run(self):
        self.sock.connect((self.host, self.port))
        threading.Thread(target=self.receive_messages, daemon=True).start()
        print("Connected to server. Press Ctrl+C to stop.\n")
        try:
            while True:
                if self.stopflag:
                    sys.exit()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stopflag = True
                        pygame.quit()
                        sys.exit()
                if keyboard.is_pressed("up"):
                    self.sock.sendall("1;".encode())
                elif keyboard.is_pressed("down"):
                    self.sock.sendall("0;".encode())
                else:
                    self.sock.sendall("2;".encode())
                self.draw()
                self.clock.tick(60)
        except KeyboardInterrupt:
            print("\nClient stopped.")
            pygame.quit()

if __name__ == "__main__":
    client = Client(host="localhost")
    client.run()