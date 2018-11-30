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

def graphics_thread():
    d = 0.0
    global start, target
    while graphics_continue:
        start.show(screen, type="predator")
        target.show(screen, type="pray")
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