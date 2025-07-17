import pygame
import math
import random

pygame.init()

font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

fps = 60

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))

class paddle():
    def __init__(self, pos, width, height, colour):
        self.pos = pygame.math.Vector2(pos)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill((colour))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3

    def move(self, direction):
        if direction == 0:
            self.pos += pygame.math.Vector2(0, self.speed)
            self.pos[1] = min(400 - self.height, self.pos[1])
        elif direction == 1:
            self.pos -= pygame.math.Vector2(0, self.speed)
            self.pos[1] = max(0, self.pos[1])

    def draw(self):
        screen.blit(self.image, self.pos)

class Ball():
    def __init__(self, pos, direction, radius):
        self.pos = pygame.math.Vector2(pos[0] - radius, pos[1] - radius)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (radius, radius), radius)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction
        self.speed = 5

    def move(self):
        previous_pos = self.pos
        new_x = math.sin(math.radians(self.direction)) * self.speed + self.pos[0]
        new_y = -math.cos(math.radians(self.direction)) * self.speed + self.pos[1]
        self.pos = pygame.math.Vector2(new_x, new_y)
        current_pos = self.pos
        players = [player1, player2]
        for player in players:
            self.pos, collision_point, offset = self.correct_exact_overlap(self.mask, current_pos, previous_pos, player.mask, player.pos)

    def draw(self):
        screen.blit(self.image, self.pos)

    def correct_exact_overlap(self, ball_mask, ball_current_pos, ball_previous_pos, paddle_mask, paddle_pos):

        print(ball_current_pos)
        print(ball_previous_pos)

        steps = max(abs(ball_current_pos[0] - ball_previous_pos[0]), abs(ball_current_pos[1] - ball_previous_pos[1]))

        dx = (ball_current_pos[0] - ball_previous_pos[0]) / steps
        dy = (ball_current_pos[1] - ball_previous_pos[1]) / steps

        for i in range(math.ceil(steps + 1)):
            x = ball_previous_pos[0] + dx * i
            y = ball_previous_pos[1] + dy * i
            offset = (int(paddle_pos[0] - x), int(paddle_pos[1] - y))
            print(offset)
            print(ball_current_pos)
            print(paddle_pos)
            collision_point = ball_mask.overlap(paddle_mask, offset)
            if collision_point is not None:
                escape_offset = 1
                x -= dx * escape_offset
                y -= dy * escape_offset
                return pygame.math.Vector2(int(x), int(y)), collision_point, offset
            
        return ball_current_pos, None, None

    def deflect_ball_from_paddle(self, collision_point, paddle_height, base_angle=180, max_deflection=60):

        relative_y = (collision_point[1] / paddle_height) * 2 - 1

        angle_offset = relative_y * max_deflection

        new_angle = base_angle + angle_offset
        return new_angle

player1 = player1 = paddle((10, 150), 10, 100, (0, 255, 0))
player2 = paddle((780, 150), 10, 100, (255, 0, 0))
ball = Ball((screen_width / 2, screen_height / 2), -90, 10)

run = True
while run:
    screen.fill((3, 161, 252))
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player1.draw()

    player2.draw()

    ball.draw()
    ball.move()

    pygame.display.update()
pygame.quit()
