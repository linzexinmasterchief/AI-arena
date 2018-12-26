import pygame, sys, random, threading, math
from pygame.locals import *

from animal import *
from find_path import *
from maps import *

from find_path import *
from picToMap import *


pygame.init()

map_size = (30, 30)

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

predator1 = bot(center_position=[1, 1])
predator2 = bot(center_position=[29, 1])
predator3 = bot(center_position=[20, 20])
predatorList = [predator1, predator2, predator3]

target = bot(center_position=[29, 29])



# the size of each grid is 10x10 -> map cordinate = pixel cordinate / 10
m = GridWithWeights(map_size[0], map_size[1])
# produce map from grey scale picture, contains walls
mapArray = generateMap("map.bmp", map_size[0], map_size[1])
m.walls = []
for y in range(len(mapArray)):
    for x in range(len(mapArray[y])):
        if mapArray[x][y] < 255:
            # map correction
            m.walls.append((29 - y, x))
path = a_star_search(m, (predator1.get_pos()[0], predator1.get_pos()[1]), (target.get_pos()[0], target.get_pos()[1]))

def graphics_thread():
    global target, m, predatorList
    while graphics_continue:
        for row in range(m.height):
            for col in range(m.width):
                if m.passable((row, col)):
                    # ground color
                    c = BLACK
                else:
                    # wall color
                    c = GREY
                # draw map block
                pygame.draw.rect(screen, c, (row * 10, col * 10, 8, 8))

        # predator
        for predator in predatorList:
            pygame.draw.rect(screen, RED, (predator.get_pos()[0] * 10, predator.get_pos()[1] * 10, 8, 8))
        # prey
        pygame.draw.rect(screen, GREEN, (target.get_pos()[0] * 10, target.get_pos()[1] * 10, 8, 8))

        pygame.display.flip()
        graphics_clock.tick(60)

def physics_thread():
    global predatorList, target, path, m
    while physics_continue:
        mpx, mpy = pygame.mouse.get_pos()
        mouse_pos_x = mpx // 10
        mouse_pos_y = mpy // 10
        if (mouse_pos_x, mouse_pos_y) in m.walls:
            pass
        else:
            target.set_pos((mouse_pos_x, mouse_pos_y))

    
        for predator in predatorList:
            
            path = a_star_search(m, (predator.get_pos()[0], predator.get_pos()[1]), (target.get_pos()[0], target.get_pos()[1]))
            predator.pathToTarget = path
            if len(predator.pathToTarget) > 1 and predator.timer > predator.get_move_duration():
                predator.set_pos(predator.pathToTarget[1])
                predator.timer = 0
            else:
                predator.timer += 1
            if predator.get_pos() == target.get_pos():
                print("catched!")

        # print(str(predator1.timer) + " | " + str(predator2.timer))
        physics_clock.tick(100)


# physics thread predator1
pTarget = threading.Thread(target=physics_thread)
pTarget.start()

# graphics thread predator1
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