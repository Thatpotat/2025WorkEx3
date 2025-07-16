import pygame
import math

pygame.init()

font = pygame.font.Font(None, 50)

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))

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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    #def send_input():

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
          
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player1 = paddle(10, 150, 10, 100, (0, 255, 0))
player2 = paddle(780, 150, 10, 100, (255, 0, 0))
ball = Ball(400, 200, 20, 20, 270)

run = True
while run:
    screen.fill((3, 161, 252))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        print("up")
    if keys[pygame.K_DOWN]:
       print("down")

    text = font.render(f"{player1.score} : {player2.score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 20))
    screen.blit(text, text_rect)

    player1.draw()

    player2.draw()

    ball.draw()

    pygame.display.update()
pygame.quit()