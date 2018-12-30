import pygame, sys, random, threading, math
from pygame.locals import *
import math

from animal import *
from find_path import *
from maps import *

from find_path import *
from picToMap import *


pygame.init()

# set map size
map_size = (50, 50)

# create paint screen
screen = pygame.display.set_mode((map_size[0] * 10, map_size[1] * 10))
# set window title
pygame.display.set_caption("AI_playground")

# create thread clocks and continue flags
game_clock = pygame.time.Clock()
game_continue = True
physics_clock = pygame.time.Clock()
physics_continue = True
graphics_clock = pygame.time.Clock()
graphics_continue = True

# preset color set
ORANGE = (255, 200, 0)
BLUE = (50, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# initialize predator positions
predator1 = bot(center_position=[1, 1])
predator2 = bot(center_position=[20, 10])
predator3 = bot(center_position=[30, 10])
# organize predators into a predator list
predatorList = [predator1, predator2, predator3]
# predatorList = [predator1]

# initialize target position
target = bot(center_position=[49, 49])


# the size of each grid is 10x10 -> map cordinate = pixel cordinate / 10
m = GridWithWeights(map_size[0], map_size[1])
# produce map from grey scale picture, contains walls
mapArray = generateMap("map100.bmp", map_size[0], map_size[1])
m.walls = []
for y in range(len(mapArray)):
    for x in range(len(mapArray[y])):
        if mapArray[x][y] < 255:
            # map direction correction
            m.walls.append((x, y))

def graphics_thread():
    global target, m, predatorList
    while graphics_continue:
        pygame.draw.rect(screen, BLACK, (0,0,500,500))
        for row in range(m.height):
            for col in range(m.width):
                if m.passable((row, col)):
                    # ground color
                    c = BLACK
                    for predator in predatorList:
                        dx = row - predator.get_pos()[0]
                        dy = col - predator.get_pos()[1]
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance == 0:
                            distance = 0.0001
                        sine = dy / distance
                        cosine = dx / distance
                        if math.asin(sine) < predator.direction_of_view + 1 and math.asin(sine) > predator.direction_of_view - 1:
                            
                            if math.acos(cosine) < predator.direction_of_view + 1 and math.acos(cosine) > predator.direction_of_view - 1:

                                if dx**2 + dy ** 2 < predator.range_of_view ** 2 + 0.1:
                                    c = ORANGE
                        
                        if (row, col) in predator.pathToTarget:
                            c = BLUE
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

        # for each predator
        for predator in predatorList:
            # find path to target
            path = a_star_search(m, (predator.get_pos()[0], predator.get_pos()[1]), (target.get_pos()[0], target.get_pos()[1]), predator.range_of_view)
            predator.pathToTarget = path
            # if didn't reach target and allow to move
            if len(predator.pathToTarget) > 1 and predator.timer > predator.get_move_duration():
                # set direction based on next node
                dx = predator.pathToTarget[1][0] - predator.get_pos()[0]
                dy = predator.pathToTarget[1][1] - predator.get_pos()[1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance == 0:
                    distance = 0.0001
                sine = dy / distance
                # cosine = dx / distance
                predator.direction_of_view = math.asin(sine)
                # print(predator.direction_of_view)

                # move to the next node on path
                predator.set_pos(predator.pathToTarget[1])
                
                # reset timer
                predator.timer = 0
            else:
                # wait for timer to reach move duration limit
                predator.timer += 1
            if predator.get_pos() == target.get_pos():
                print("catched!")

        # print(str(predator1.timer) + " | " + str(predator2.timer))
        physics_clock.tick(60)


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
            # exit all threads
            graphics_continue = False
            physics_continue = False
            game_continue = False
    
    game_clock.tick(60)

# quit window
pygame.quit()
sys.exit()