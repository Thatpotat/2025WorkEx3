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
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = 3

    def move(self, direction):
        if direction == 0:
            self.pos += pygame.math.Vector2(0, self.speed)
            self.pos[1] = min(400 - self.height, self.pos[1])
        elif direction == 1:
            self.pos -= pygame.math.Vector2(0, self.speed)
            self.pos[1] = max(0, self.pos[1])

    def draw(self):
        screen.blit(self.image, self.rect)

class Ball():
    def __init__(self, pos, direction, radius):
        self.pos = pygame.math.Vector2(pos[0] - radius, pos[1] - radius)
        self.radius = radius
        self.image = pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] + self.radius, self.pos[1] + self.radius), self.radius)
        self.direction = direction
        self.speed = 5

    def move(self):
        previous_topleft, previous_bottomright = self.pos, pygame.math.Vector2(self.pos[0] + self.radius * 2, self.pos[1] + self.radius * 2)
        self.pos = pygame.math.Vector2(self.pos[0] + math.sin(math.radians(self.direction)) * self.speed, self.pos[1] + math.cos(math.radians(self.direction)) * self.speed)
        current_topleft, current_bottomright = self.pos, pygame.math.Vector2(self.pos[0] + self.radius * 2, self.pos[1] + self.radius * 2)
        topleft_trajectory = (previous_topleft, current_topleft)
        bottomright_trajectory = (previous_bottomright, current_bottomright)
        players = [player1, player2]
        for player in players:
            collision_point = self.check_collision(topleft_trajectory, bottomright_trajectory, player.rect)
            print(collision_point)

    def draw(self):
        self.image = pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] + self.radius, self.pos[1] + self.radius), self.radius)

    def check_collision(self, ball_topleft_trajectory, ball_bottomright_trajectory, paddle_rect):
        clipped_line = paddle_rect.clipline(ball_topleft_trajectory)
        if clipped_line:
            collision_point = clipped_line[0]
            return collision_point
        else:
            clipped_line = paddle_rect.clipline(ball_bottomright_trajectory)
            if clipped_line:
                collision_point = clipped_line[0]
                return collision_point
        

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
    player1.move(0)

    player2.draw()

    ball.draw()
    ball.move()

    pygame.display.update()
pygame.quit()
