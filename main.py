import pygame, sys, random, threading, math
from pygame.locals import *

from animal import *
from find_path import *
from maps import *

from find_path import *
from picToMap import *


pygame.init()

map_size = (100, 100)

screen = pygame.display.set_mode((map_size[0] * 10, map_size[1] * 10))
pygame.display.set_caption("AI_playground")

game_clock = pygame.time.Clock()
game_continue = True
physics_clock = pygame.time.Clock()
physics_continue = True
graphics_clock = pygame.time.Clock()
graphics_continue = True

ORANGE = (255, 200, 0)
BLUE = (50, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

start = bot(center_position=[1, 1])
target = bot(center_position=[99, 99])



# the size of each grid is 10x10 -> map cordinate = pixel cordinate / 10
m = GridWithWeights(map_size[0], map_size[1])
# produce map from grey scale picture, contains walls
mapArray = generateMap("map.bmp")
m.walls = []
for y in range(len(mapArray)):
    for x in range(len(mapArray[y])):
        if mapArray[x][y] != 255:
            m.walls.append((x, y))
path = a_star_search(m, (start.get_pos()[0], start.get_pos()[1]), (target.get_pos()[0], target.get_pos()[1]))

def graphics_thread():
    global start, target, m
    while graphics_continue:
        for row in range(m.height):
            for col in range(m.width):
                if (row, col) in path:
                    # path color
                    c = BLUE
                elif m.passable((row, col)):
                    # ground color
                    c = GREY
                else:
                    # wall color
                    c = ORANGE
                # draw map block
                pygame.draw.rect(screen, c, (row * 10, col * 10, 8, 8))

        # predator
        pygame.draw.rect(screen, RED, (start.get_pos()[0] * 10, start.get_pos()[1] * 10, 8, 8))
        # prey
        pygame.draw.rect(screen, GREEN, (target.get_pos()[0] * 10, target.get_pos()[1] * 10, 8, 8))

        pygame.display.flip()
        graphics_clock.tick(60)

def physics_thread():
    global start, target, path, m
    while physics_continue:
        mpx, mpy = pygame.mouse.get_pos()
        mouse_pos_x = mpx // 10
        mouse_pos_y = mpy // 10
        if (mouse_pos_x, mouse_pos_y) in m.walls:
            pass
        else:
            target.set_pos((mouse_pos_x, mouse_pos_y))

        path = a_star_search(m, (start.get_pos()[0], start.get_pos()[1]), (target.get_pos()[0], target.get_pos()[1]))

        # physics_clock.tick(60)


# physics thread start
pTarget = threading.Thread(target=physics_thread)
pTarget.start()

# graphics thread start
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
    
    game_clock.tick(60)