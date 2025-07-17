import socket
import threading
import keyboard
import time
import sys
import math

import pygame

pygame.init()

font = pygame.font.Font(None, 50)

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

class paddle:
    def __init__(self, x, y, width, height, colour):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.score = 0
        self.speed = 3
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.colour = colour

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Ball:
    def __init__(self, x, y, width, height, direction):
        self.starting_pos = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.direction = direction
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player1 = paddle(10, 150, 11, 100, (0, 255, 0))
player2 = paddle(780, 150, 11, 100, (255, 0, 0))
ball = Ball(400, 200, 20, 20, 45)

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.stopflag = False

        # Game state variables
        self.p1x = 10
        self.p1y = 150
        self.p2x = 780
        self.p2y = 150
        self.bx = 400
        self.by = 200
        self.s1 = 0
        self.s2 = 0

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Pong Client")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)

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
        # Draw paddles
        pygame.draw.rect(self.screen, (0, 255, 0), (self.p1x, self.p1y, 11, 100))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.p2x, self.p2y, 11, 100))
        # Draw ball
        pygame.draw.rect(self.screen, (255, 255, 255), (self.bx, self.by, 20, 20))
        # Draw score
        text = self.font.render(f"{int(self.s1)} : {int(self.s2)}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 20))
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
                # Handle quit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stopflag = True
                        pygame.quit()
                        sys.exit()
                # 0 = down, 1 = up, 2 = none
                if keyboard.is_pressed("up"):
                    self.sock.sendall("1;".encode())
                elif keyboard.is_pressed("down"):
                    self.sock.sendall("0;".encode())
                else:
                    self.sock.sendall("2;".encode())
                #self.draw()
                screen.fill((3, 161, 252))

                player1.x = self.p1x
                player1.y = self.p1y
                player2.x = self.p2x
                player2.y = self.p2y
                ball.x = self.bx
                ball.y = self.by
                player1.score = self.s1
                player2.score = self.s2

                player1.draw()

                player2.draw()

                ball.draw()

                text = self.font.render(f"{int(player1.score)} : {int(player2.score)}", True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, 20))
                self.screen.blit(text, text_rect)

                self.clock.tick(60)
                pygame.display.update()
        except KeyboardInterrupt:
            print("\nClient stopped.")
            pygame.quit()

if __name__ == "__main__":
    client = Client(host="192.168.55.8")
    client.run()