import pygame, sys, threading, math

from animal import *
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
AI_continue = True
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
predator1 = bot(center_position=[40, 30])
predator2 = bot(center_position=[16, 9])
predator3 = bot(center_position=[30, 10])
# organize predators into a predator list
predatorList = [predator1, predator2, predator3]

# initialize target position
target = bot(center_position=[49, 49])

# the size of each grid is 10x10 -> map cordinate = pixel cordinate / 10
m = GridWithWeights(map_size[0], map_size[1])
# produce map from grey scale picture, contains walls
mapArray = generateMap("map50.bmp", map_size[0], map_size[1])
m.walls = []
for x in range(len(mapArray)):
    for y in range(len(mapArray[x])):
        if mapArray[x][y] < 255:
            # map direction correction
            m.walls.append((x, y))


def graphics_thread():
    global target, m, predatorList
    while graphics_continue:
        pygame.draw.rect(screen, BLACK, (0, 0, 500, 500))

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
            # calculate the left top corner coordinate for the range of view arc
            arc_posx = predator.get_pos()[0] * 10 - predator.range_of_view * 10
            arc_posy = predator.get_pos()[1] * 10 - predator.range_of_view * 10

            # draw range of view for each predator
            pygame.draw.arc(screen,
                            RED,
                            (arc_posx, arc_posy, predator.range_of_view * 20, predator.range_of_view * 20),
                            -predator.direction_of_view - predator.field_of_view / 2, -predator.direction_of_view + predator.field_of_view / 2, 2)
            for (row, col) in predator.pathToTarget:
                c = BLUE
                pygame.draw.rect(screen, c, (row * 10, col * 10, 8, 8))
        # prey
        pygame.draw.rect(screen, GREEN, (target.get_pos()[0] * 10, target.get_pos()[1] * 10, 8, 8))

        # draw predator them self (to prevent the blue path block cover the predators)
        for predator in predatorList:
            pygame.draw.rect(screen, RED, (predator.get_pos()[0] * 10, predator.get_pos()[1] * 10, 8, 8))
        pygame.display.flip()
        graphics_clock.tick(100)


def AI_thread():
    global predatorList, target, path, m
    while AI_continue:
        mpx, mpy = pygame.mouse.get_pos()
        # translate screen pixel mouse pos to world pos
        mouse_pos_x = mpx // 10
        mouse_pos_y = mpy // 10
        if (mouse_pos_x, mouse_pos_y) in m.walls:
            pass
        else:
            target.set_pos((mouse_pos_x, mouse_pos_y))

        # for each predator
        for predator in predatorList:
            # calculate if the target is in the field range of the predator
            if (predator.get_pos()[0] - target.get_pos()[0])**2 + (predator.get_pos()[1] - target.get_pos()[1])**2 < predator.range_of_view ** 2:
                predator.set_target_pos(target.get_pos()[0], target.get_pos()[1])
            else:
                # if the predator reaches target last sighted spot and found nothing
                if predator.get_pos()[0] == predator.get_target_pos()[0] and predator.get_pos()[1] == predator.get_target_pos()[1]:
                    # randomly generate new target pos until it is neither in the wall or out of the map
                    while True:
                        random_new_target_x = predator.get_pos()[0] + random.randint(-5, 5)
                        random_new_target_y = predator.get_pos()[1] + random.randint(-5, 5)
                        if m.passable((random_new_target_x, random_new_target_y)) and m.in_bounds((random_new_target_x, random_new_target_y)):
                            break
                    predator.set_target_pos(random_new_target_x, random_new_target_y)

            ''' find path to target
                without the range of view (max search depth parameter)
                the find path algorithm will use 100 as default
            '''
            path = a_star_search(m, (predator.get_pos()[0], predator.get_pos()[1]), predator.get_target_pos())
            predator.pathToTarget = path
            # if didn't reach target and allow to move
            if len(predator.pathToTarget) > 1 and predator.timer > predator.get_move_duration():
                # set direction to target
                seen_target_x, seen_target_y = predator.get_target_pos()
                dx = seen_target_x - predator.get_pos()[0]
                dy = seen_target_y - predator.get_pos()[1]
                d = math.sqrt(dx**2 + dy**2)
                if d != 0:
                    if dy > 0:
                        predator.direction_of_view = math.acos(dx / d)
                    else:
                        predator.direction_of_view = math.pi * 2 - math.acos(dx / d)

                # move to the next node on path
                predator.set_pos(predator.pathToTarget[1])

                # reset timer
                predator.timer = 0
            else:
                # wait for timer to reach move duration limit
                predator.timer += 1
            if predator.get_pos() == target.get_pos():
                print("catches!")

        physics_clock.tick(60)


# physics thread predator1
pTarget = threading.Thread(target=AI_thread)
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
            AI_continue = False
            game_continue = False
            break
    
    game_clock.tick(60)

# quit window
pygame.quit()
sys.exit()
exit()