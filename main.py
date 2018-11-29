import pygame, sys, random, threading, math
from pygame.locals import *

from animal import *

pygame.init()

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("AI_playground")

game_clock = pygame.time.Clock()
game_continue = True
physics_clock = pygame.time.Clock()
physics_continue = True
graphics_clock = pygame.time.Clock()
graphics_continue = True

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

start = bot(center_position=[50, 50])
target = bot(center_position=[300, 200])

def draw_triangle(Surface, color, position, direction):
    # direction is an Eular angle
    point_distance = 50
    pygame.draw.polygon(
        Surface, 
        color, 
        [(position[0] + point_distance * math.sin(direction), position[1] + point_distance * math.cos(direction)),
         (position[0] + point_distance * math.sin(direction + 120), position[1] + point_distance * math.cos(direction + 120)),
         (position[0] + point_distance * math.sin(direction - 120), position[1] + point_distance * math.cos(direction - 120))], 
        1)
    pygame.draw.rect(Surface, RED, (position[0], position[1], 3,3), 2)

    # pygame.draw.polygon(Surface, color, [(50, 50),(55,55),(52, 54)], 10)

def graphics_thread():
    d = 0.0
    global start, target
    while graphics_continue:
        pygame.draw.rect(screen, BLACK, (0, 0, 400, 400))
        pygame.draw.rect(screen, RED, (int(start.get_graphic_position()[0]), int(start.get_graphic_position()[1]), start.get_size()[0], start.get_size()[1]))
        pygame.draw.circle(screen, GREEN, (int(target.get_graphic_position()[0]), int(target.get_graphic_position()[1])), target.get_size()[0], target.get_size()[1])
        # draw_triangle(screen, GREEN, [100, 100], d)
        # d += 0.02
        pygame.display.flip()
        graphics_clock.tick(60)

def physics_thread():
    global start, target
    while physics_continue:
        start.set_direction(0)


gTarget = threading.Thread(target=graphics_thread)

gTarget.start()

while game_continue:
    # basic event control
    for event in pygame.event.get():
        # window exit
        if event.type == pygame.QUIT:
            graphics_continue = False
            physics_continue = False
            game_continue = False
            pygame.quit()
            sys.exit()
    
    game_clock.tick(100)