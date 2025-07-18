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
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill((colour))
        #self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.mask_surface = pygame.Surface((width +2, height + 2))
        self.mask_surface.fill((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.mask_surface)

    def move(self, direction):
        if direction == 0:
            self.y += self.speed
            self.y = min(400 - self.height, self.y)
        elif direction == 1:
            self.y -= self.speed
            self.y = max(0, self.y)

    def draw(self):
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
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player1 = player1 = paddle(10, 150, 10, 100, (0, 255, 0))
player2 = paddle(780, 150, 10, 100, (255, 0, 0))
ball = Ball(screen_width / 2, screen_height / 2, 45, 10)

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
