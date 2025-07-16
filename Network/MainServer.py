import socket
import threading
import time
import random
import math

# Optional: Enable display for debugging
ENABLE_DISPLAY = False
if ENABLE_DISPLAY:
    import pygame

class paddle:
    def __init__(self, x, y, width, height, colour):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.score = 0
        self.speed = 3
        if ENABLE_DISPLAY:
            self.image = pygame.Surface((width, height))
            self.image.fill(colour)
            self.colour = colour

    def move(self, direction):
        if direction == 0:  # down
            self.y += self.speed
            self.y = min(400 - self.height, self.y)
        elif direction == 1:  # up
            self.y -= self.speed
            self.y = max(0, self.y)

    def draw(self, screen):
        if ENABLE_DISPLAY:
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
        if ENABLE_DISPLAY:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 255, 255))

    def move(self):
        global player1, player2
        prev_x, prev_y = self.x, self.y
        self.x += math.sin(math.radians(self.direction)) * self.speed
        self.y += math.cos(math.radians(self.direction)) * self.speed

        # Paddle collision
        # Player 1
        if (self.x <= player1.x + player1.width and
            player1.y < self.y + self.height and
            self.y < player1.y + player1.height):
            self.x = player1.x + player1.width
            relative_y = (self.y + (self.width / 2)) - player1.y
            deflection_weight = relative_y / player1.height * 2 - 1
            angle_offset = deflection_weight * 45
            self.direction = -angle_offset - 90
            self.direction = 360 - self.direction

        # Player 2
        if (self.x + self.width >= player2.x and
            player2.y < self.y + self.height and
            self.y < player2.y + player2.height):
            self.x = player2.x - self.width
            relative_y = (self.y + (self.width / 2)) - player2.y
            deflection_weight = relative_y / player2.height * 2 - 1
            angle_offset = deflection_weight * 45
            self.direction = angle_offset + 90
            self.direction = 360 - self.direction

        # Wall collision
        if self.y <= 0 or self.y + self.width >= 400:
            self.direction = 180 - self.direction

        # Point detection
        if self.x + self.width <= 0:
            player2.score += 1
            self.x, self.y = self.starting_pos
            self.direction = random.choice([45, 135, 225, 315])
        elif self.x >= 800:
            player1.score += 1
            self.x, self.y = self.starting_pos
            self.direction = random.choice([45, 135, 225, 315])

    def draw(self, screen):
        if ENABLE_DISPLAY:
            screen.blit(self.image, (self.x, self.y))

class PongServer:
    def __init__(self, port=12345, limit=2):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(limit)
        self.connections = []
        self.inputs = [2, 2]  # 0=down, 1=up, 2=none for each player
        self.inputs_lock = threading.Lock()
        self.running = True

        # Game objects
        global player1, player2
        player1 = paddle(10, 150, 10, 100, (0, 255, 0))
        player2 = paddle(780, 150, 10, 100, (255, 0, 0))
        self.ball = Ball(400, 200, 20, 20, 45)

        if ENABLE_DISPLAY:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 400))
            pygame.display.set_caption("Pong Server Debug")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 50)

    def handle_client(self, conn, player_id):
        buffer = ""
        while self.running:
            try:
                char = conn.recv(1).decode()
                if not char:
                    break
                if char == ";":
                    try:
                        val = int(buffer)
                        with self.inputs_lock:
                            self.inputs[player_id] = val
                    except:
                        with self.inputs_lock:
                            self.inputs[player_id] = 2
                    buffer = ""
                else:
                    buffer += char
            except:
                break
        conn.close()

    def broadcast_state(self):
        state = f"{player1.x},{player1.y},{player2.x},{player2.y},{self.ball.x},{self.ball.y},{player1.score},{player2.score};"
        for conn in self.connections:
            try:
                conn.sendall(state.encode())
            except:
                pass

    def game_loop(self):
        fps = 60
        while self.running:
            with self.inputs_lock:
                p1_input = self.inputs[0]
                p2_input = self.inputs[1]
            player1.move(p1_input)
            player2.move(p2_input)
            self.ball.move()
            self.broadcast_state()
            print(f"\rP1:({player1.x:.0f},{player1.y:.0f})  P2:({player2.x:.0f},{player2.y:.0f})  Ball:({self.ball.x:.0f},{self.ball.y:.0f})  Score:{int(player1.score)}:{int(player2.score)}           ", end="")

            if ENABLE_DISPLAY:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        return
                self.screen.fill((3, 161, 252))
                player1.draw(self.screen)
                player2.draw(self.screen)
                self.ball.draw(self.screen)
                text = self.font.render(f"{player1.score} : {player2.score}", True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, 20))
                self.screen.blit(text, text_rect)
                pygame.display.update()
                self.clock.tick(fps)
            else:
                time.sleep(1/fps)

    def run(self):
        print("Waiting for 2 clients...")
        while len(self.connections) < 2:
            conn, addr = self.sock.accept()
            print(f"Connected by {addr}")
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, len(self.connections)-1), daemon=True).start()
        print("Both clients connected. Starting game.")

        game_thread = threading.Thread(target=self.game_loop, daemon=True)
        game_thread.start()

        try:
            while game_thread.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("Server stopped.")
        if ENABLE_DISPLAY:
            pygame.quit()

if __name__ == "__main__":
    server = PongServer()
    server.run()