import socket
import threading
import time
import random
import math

# Optional: Enable display for debugging
ENABLE_DISPLAY = False
import pygame

class Paddle:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill((colour))
        #self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.mask_surface = pygame.Surface((width + 2, height + 2))
        self.mask_surface.fill((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.mask_surface)
        self.score = 0
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

class Ball():
    def __init__(self, x, y, direction, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.diameter = self.radius * 2
        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (radius, radius), radius)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.speed = 5

    def move(self):
        previous_pos = (self.x, self.y)
        self.x += math.sin(math.radians(self.direction)) * self.speed
        self.y -= math.cos(math.radians(self.direction)) * self.speed
        current_pos = (self.x, self.y)
        players = [player1, player2]
        for player in players:
            self.x, self.y, collision_point  = self.correct_exact_overlap(self.mask, current_pos, previous_pos, player.mask, (player.x, player.y))
            current_pos = (self.x, self.y)
            print(self.x, self.y)
            if collision_point:
                if self.y + self.radius >= player.y and self.y <= player.y + player.height:
                    if player == players[0]:
                        self.direction = self.deflect_ball_from_paddle(player1.height, player1.y, max_deflection=-45)
                    else:
                        self.direction = self.deflect_ball_from_paddle(player2.height, player2.y, base_angle=270)
                else:
                    self.direction = 180 - self.direction
        
        hit_top = self.y <= 0
        hit_bottom = self.y + self.radius * 2 >= 400

        if hit_top or hit_bottom:
            self.direction = 180 - self.direction

    def correct_exact_overlap(self, ball_mask, ball_current_pos, ball_previous_pos, paddle_mask, paddle_pos):

        steps = max(abs(ball_current_pos[0] - ball_previous_pos[0]), abs(ball_current_pos[1] - ball_previous_pos[1]))

        if steps == 0:
            return ball_current_pos[0], ball_current_pos[1], None, None

        dx = (ball_current_pos[0] - ball_previous_pos[0]) / steps
        dy = (ball_current_pos[1] - ball_previous_pos[1]) / steps

        for i in range(math.ceil(steps + 1)):
            x = ball_previous_pos[0] + dx * i
            y = ball_previous_pos[1] + dy * i
            offset = ((int(paddle_pos[0] - 1) - x), int((paddle_pos[1] - 1) - y))
            collision_point = ball_mask.overlap(paddle_mask, offset) # offset is the vector from the calling mask to the other mask
            if collision_point:
                #breakpoint()  # Triggers debugger if collision occurs
                print("collision detected")
                escape_offset = 1
                x -= dx * escape_offset
                y -= dy * escape_offset
                return int(x), int(y), collision_point
            
        return ball_current_pos[0], ball_current_pos[1], None

    def deflect_ball_from_paddle(self, paddle_height, paddle_y, base_angle=90, max_deflection=45):

        angle_offset_weight = ((self.y + self.radius - paddle_y) / paddle_height) * 2 - 1

        angle_offset = angle_offset_weight * max_deflection

        print(angle_offset)
        #breakpoint()

        new_angle = base_angle + angle_offset

        return new_angle

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
        self.ball = Ball(400, 200, 20, 45)

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