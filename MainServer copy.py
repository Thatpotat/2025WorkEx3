import socket
import threading
import time
import random
import math

# Optional: Enable display for debugging
ENABLE_DISPLAY = False
if ENABLE_DISPLAY:
    import pygame

class Paddle:
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
        previous_pos  = (self.x, self.y)
        self.x += math.sin(math.radians(self.direction)) * self.speed
        self.y += math.cos(math.radians(self.direction)) * self.speed
        faces = [
            ((player1.x + player1.width, player1.y), (player1.x + player1.width, player1.y + player1.height)), # player1 front
            ((player1.x, player1.y), (player1.x, player1.y + player1.height)), # player1 back
            ((player2.x + player2.width, player2.y), (player2.x + player2.width, player2.y + player2.height)), # player2 back
            ((player2.x, player2.y), (player2.x, player2.y + player2.height)),  # player2 front
        ]
        vertices = [
            (self.x, self.y), 
            (self.x + self.width, self.y),
            (self.x, self.y + self.height), 
            (self.x + self.width, self.y + self.height)
        ]
        for face in faces:
            for vertice in vertices:
                intersection = self.line_intersection(previous_pos, vertice, face[0], face[1])
                if intersection is not None:
                    break
            if intersection:
                if face == faces[0]:
                    self.x, self.y = intersection[0] + 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player1.y                  
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  angle_offset + 90
                elif face == faces[1]:
                    self.x, self.y = intersection[0] + player1.width + 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player1.y                   
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  angle_offset + 90
                elif face == faces[2]:
                    self.x, self.y = intersection[0] - self.width - player2.width  - 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player2.y                   
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  - angle_offset - 90 
                else:
                    self.x, self.y = intersection[0] - self.width - 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player2.y
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  - angle_offset - 90
                player1.speed += 0.125
                player2.speed += 0.125
                player1.speed = min(player1.speed, 5)
                player2.speed = min(player2.speed, 5)
                self.speed += 0.25
                self.speed = min(9, self.speed)

        if self.y <= 0 or self.y + self.height >= 400:
            self.direction = 180 - self.direction
            if self.y <= 0:
                self.y = 1
            else:
                self.y = 400 - self.height - 1

        # point detection
        
        player1_scored = self.x >= 800
        player2_scored = self.x + self.width <= 0

        if player1_scored:
            player1.score += 1
        elif player2_scored:
            player2.score += 1
        if player1_scored or player2_scored:
            self.x, self.y = self.starting_pos
            self.direction = random.randint(1, 4) * 90 + 45
            self.speed = 5
            player1.speed = 3
            player2.speed = 3

    def line_intersection(self, p1, p2, p3, p4):
        x1, y1, x2, y2 = *p1, *p2
        x3, y3, x4, y4 = *p3, *p4

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None  # Lines are parallel or coincident

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and \
        min(x3, x4) <= px <= max(x3, x4) and min(y3, y4) <= py <= max(y3, y4):
            return px, py, x1, y1, x2, y2, x3, y3, x4, y4  # Intersection point

        return None  # No intersection within the segments

    def draw(self, screen):
        if ENABLE_DISPLAY:
            screen.blit(self.image, (self.x, self.y))

class PongServer:
    def __init__(self, port=12345, limit=2):
        self.limit = limit
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(limit)
        self.connections = []
        self.inputs = [2, 2]  # 0=down, 1=up, 2=none for each player
        self.inputs_lock = threading.Lock()
        self.running = True

        # Game objects
        global player1, player2
        player1 = Paddle(10, 150, 11, 100, (0, 255, 0))
        player2 = Paddle(780, 150, 11, 100, (255, 0, 0))
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
            player2.move(p2_input)
            player1.move(p1_input)
            self.ball.move()
            self.broadcast_state()
            #print(f"\rP1:({player1.x:.0f},{player1.y:.0f})  P2:({player2.x:.0f},{player2.y:.0f})  Ball:({self.ball.x:.0f},{self.ball.y:.0f})  Score:{int(player1.score)}:{int(player2.score)}           ", end="", flush=True)

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
        print(f"Waiting for {self.limit} clients...")

        def accept_clients():
            while len(self.connections) < self.limit:
                conn, addr = self.sock.accept()
                print(f"Connected by {addr}")
                self.connections.append(conn)
                threading.Thread(target=self.handle_client, args=(conn, len(self.connections)-1), daemon=True).start()

        accept_thread = threading.Thread(target=accept_clients, daemon=True)
        accept_thread.start()

        # Wait for both clients to connect before starting the game loop
        while len(self.connections) < self.limit:
            if ENABLE_DISPLAY:
                pygame.event.pump()
            time.sleep(0.1)
        print(f"{self.limit} clients connected. Starting game.")

        # Run the game loop in the main thread (fixes display freezing)
        try:
            self.game_loop()
        except KeyboardInterrupt:
            self.running = False
            print("\nServer stopped.")
        if ENABLE_DISPLAY:
            pygame.quit()

if __name__ == "__main__":
    server = PongServer(limit=1)
    server.run()