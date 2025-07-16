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
    def __init__(self, x, y, width ,height, colour):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.score = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3

    def move(self, direction):
        if direction == 0:
            self.y += self.speed
            self.y = min(400 - self.height, self.y)
        elif direction == 1:
            self.y -= self.speed
            self.y = max(0, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player1:paddle
player2:paddle

class Ball():
    def __init__(self, x, y, width, height, direction):
        self.starting_pos = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.speed = 5
        self.direction = direction
        self.image.fill((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.image)

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
                    print(relative_y)
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  angle_offset + 90
                elif face == faces[1]:
                    self.x, self.y = intersection[0] + self.width + 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player1.y
                    print(relative_y)
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  angle_offset + 90
                elif face == faces[2]:
                    self.x, self.y = intersection[0] - 2 * self.width - 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player2.y
                    print(relative_y)
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  - angle_offset - 90 
                else:
                    self.x, self.y = intersection[0] - self.width - 1, intersection[1]
                    relative_y = (self.y + (self.width / 2)) - player2.y
                    deflection_weight = relative_y / player1.height * 2 - 1
                    angle_offset = deflection_weight * 45
                    self.direction =  - angle_offset - 90
                self.speed += 0.25
                self.speed = min(10, self.speed)

        if self.y <= 0 or self.y + self.height >= 400:
            self.direction = 180 - self.direction
            if self.y <= 0:
                self.y = 1
            else:
                self.y = 400 - self.height - 1

        # point detection
        if self.x + self.width <= 0 or self.x + self.width >= 800:
            if self.x + self.width <= 0:
                player2.score += 1
            else:
                player1.score += 1
            self.x, self.y = self.starting_pos
            self.direction = random.randint(1, 4) * 90 + 45
            self.speed = 5

    def correct_exact_overlap(self, ball_previous_pos, ball_current_pos, paddle):
        """
        steps = max(abs(ball_current_pos[0] - ball_previous_pos[0]), abs(ball_current_pos[1] - ball_previous_pos[1]))   

        dx = (ball_current_pos[0] - ball_previous_pos[0]) / steps
        dy = (ball_current_pos[1] - ball_previous_pos[1]) / steps 

        for i in range(math.ceil(steps + 1)):
            x = ball_previous_pos[0] + dx * i
            y = ball_previous_pos[1] + dy * i
            offset = (int(x - paddle_pos[0]), int(y - paddle_pos[1]))
            collision_point = ball_mask.overlap(paddle_mask, offset)
            print(offset, ball_mask, paddle_mask)
            if collision_point:
                escape_offset = 1
                x -= dx * escape_offset
                y -= dy * escape_offset
                return int(x), int(y), collision_point, offset
            
        return ball_current_pos[0], ball_current_pos[1],  None, None 
        """

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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def main():
    global player1
    global player2
    global ball
    player1 = paddle(10, 150, 10, 100, (0, 255, 0))
    player2 = paddle(780, 150, 10, 100, (255, 0, 0))
    ball = Ball(400, 200, 20, 20, random.randint(1, 4) * 90 + 45)

    run = True
    while run:
        screen.fill((3, 161, 252))
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        text = font.render(f"{player1.score} : {player2.score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 20))
        screen.blit(text, text_rect)

        # temporary controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player2.move(1)
        if keys[pygame.K_DOWN]:
            player2.move(0)
        if keys[pygame.K_w]:
            player1.move(1)
        if keys[pygame.K_s]:
            player1.move(0)

        player1.draw()

        player2.draw()

        ball.draw()
        ball.move()

        pygame.display.update()
    pygame.quit()

def parseInput(input:str):
    input = input.split(",")
    if input[0] == "0":
        player1.move(input[1])
    elif input[0] == "1":
        player2.move(input[1])
main()