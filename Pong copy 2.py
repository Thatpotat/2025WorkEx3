import pygame
import math
import  keyboard

pygame.init()

clock = pygame.time.Clock()

fps = 60

speed = 5

class paddle():
    def __init__(self, x, y, width ,height, colour):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.score = 0

    def move(self, direction):
        if direction == 0:
            self.y += speed
            self.y = min(400 - self.height, self.y)
        elif direction == 1:
            self.y -= speed
            self.y = max(0, self.y)
        self.rect.topleft = (self.x, self.y)

class Ball():
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.speed = 10
        self.direction = direction
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def move(self):
        self.x += math.sin(math.radians(self.direction)) * speed
        self.y += math.cos(math.radians(self.direction)) * speed
        self.rect.topleft = (self.x, self.y)
        if (self.y + self.width) >= 400 or self.y <= 0:
            self.direction = 180 - self.direction

        if self.rect.clipline((player1.x + player1.width, player1.y), (player1.x + player1.width, player1.y + player1.height)) or self.rect.clipline((player2.x, player2.y), (player2.x, player2.y + player2.height)):
            print("collision")
            self.direction = - self.direction          

player1 = paddle(10, 150, 10, 100, (0, 255, 0))
player2 = paddle(780, 150, 10, 100, (255, 0, 0))
ball = Ball(400, 200, 20, 20, 270)

run = True
while run:
    clock.tick(fps)
    if keyboard.is_pressed("esc"):
        run = False

    #player1.move()

    #player2.move()

    ball.move()

pygame.quit()