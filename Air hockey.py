import pygame
pygame.init

import math

clock = pygame.time.Clock()

fps = 60

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

mallet1 = pygame.image.load("mallet.png").convert_alpha()
puck_img = pygame.image.load("Puck.png").convert_alpha()

class mallet():
    def __init__(self, x, y, image):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.x = x
        self.y = y
        self.speed = 0

    def draw(self):
        screen.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        delta_x = self.x - mouse_pos[0]
        delta_y = self.y - mouse_pos[1]
        self.speed = math.sqrt(delta_x ** 2 + delta_y ** 2)
        self.speed = min(self.speed, 20)
        direction = math.degrees(math.atan2(math.radians(delta_x), math.radians(delta_y))) + 180
        print(direction)
        self.x += math.sin(math.radians(direction)) * self.speed
        self.y += math.cos(math.radians(direction)) * self.speed

class Puck():
    def __init__(self, x ,y, image):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        

player1 = mallet(500, 300, mallet1)
puck = Puck(100, 100, puck_img)

run = True
while run:
    screen.fill((0, 0, 0))
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player1.draw()
    player1.move()

    puck.draw()
    puck.move()
    
    pygame.display.update()
pygame.quit()