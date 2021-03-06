import pygame
import threading
import time
from bot import *
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
AI_PAUSED = False
graphics_clock = pygame.time.Clock()
graphics_continue = True

# preset color set
ORANGE = (255, 125, 30)
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

# initialize prey position
prey = bot(center_position=[49, 49], move_duration=5, field_of_view=math.pi / 2, range_of_view=15)

# the size of each grid is 10x10 -> map coordinate = pixel coordinate / 10
m = GridWithWeights(map_size[0], map_size[1])
# produce map from grey scale picture, contains walls
mapArray = generateMap("map50_02.bmp", map_size[0], map_size[1])
m.walls = []
for x in range(len(mapArray)):
    for y in range(len(mapArray[x])):
        if mapArray[x][y] < 255:
            # map direction correction
            m.walls.append((x, y))


def draw_view_field(bot, color=(0, 0, 0)):
    # calculate the left top corner coordinate for the range of view arc
    arc_posx = bot.get_pos()[0] * 10 - bot.range_of_view * 10
    arc_posy = bot.get_pos()[1] * 10 - bot.range_of_view * 10
    # draw arc of view field
    pygame.draw.arc(screen,
                    color,
                    (arc_posx, arc_posy, bot.range_of_view * 20, bot.range_of_view * 20),
                    -bot.direction_of_view - bot.field_of_view / 2,
                    -bot.direction_of_view + bot.field_of_view / 2, 1)
    # draw left line of view field
    pygame.draw.line(screen,
                     color,
                     (bot.get_pos()[0] * 10 + 5, bot.get_pos()[1] * 10 + 5),
                     (bot.get_pos()[0] * 10 + bot.range_of_view * 10 * math.cos(
                         bot.direction_of_view + bot.field_of_view / 2),
                      bot.get_pos()[1] * 10 + bot.range_of_view * 10 * math.sin(
                          bot.direction_of_view + bot.field_of_view / 2)),
                     1)
    # draw right line of view field
    pygame.draw.line(screen,
                     color,
                     (bot.get_pos()[0] * 10 + 5, bot.get_pos()[1] * 10 + 5),
                     (bot.get_pos()[0] * 10 + bot.range_of_view * 10 * math.cos(
                         bot.direction_of_view - bot.field_of_view / 2),
                      bot.get_pos()[1] * 10 + bot.range_of_view * 10 * math.sin(
                          bot.direction_of_view - bot.field_of_view / 2)),
                     1)


def draw_planned_path(bot, color=(0, 0, 0)):
    for (row, col) in bot.pathToTarget:
        pygame.draw.rect(screen, color, (row * 10, col * 10, 8, 8))


def graphics_thread():
    global prey, m, predatorList
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

        # prey
        # draw range of view for prey
        draw_view_field(prey, GREEN)
        # draw planned path
        draw_planned_path(prey, BLUE)

        # predator
        for predator in predatorList:
            # draw range of view for each predator
            draw_view_field(predator, RED)

            # draw planned path
            draw_planned_path(predator, ORANGE)

        # prey
        pygame.draw.rect(screen, GREEN, (prey.get_pos()[0] * 10, prey.get_pos()[1] * 10, 8, 8))

        # draw predator them self (to prevent the blue path block cover the predators)
        for predator in predatorList:
            pygame.draw.rect(screen, RED, (predator.get_pos()[0] * 10, predator.get_pos()[1] * 10, 8, 8))
        pygame.display.flip()
        graphics_clock.tick(60)


def set_auto_cruise_target(bot, range):
    while True:
        bot_x = bot.get_pos()[0] + random.randint(-range, range)
        bot_y = bot.get_pos()[1] + random.randint(-range, range)
        if m.passable((bot_x, bot_y)) and m.in_bounds((bot_x, bot_y)):
            break
    bot.set_target_pos(bot_x, bot_y)
    bot.pathToTarget = a_star_search(m, (bot.get_pos()[0], bot.get_pos()[1]), bot.get_target_pos())


def is_line_blocked_by_wall(x_start=0, y_start=0, x_end=0, y_end=0,):
    x, y = 0, 0
    diff_x = x_end - x_start
    diff_y = y_end - y_start
    if diff_x == 0:
        for y in range(y_start, y_end):
            if not m.passable((x_start, y)):
                return True
        return False
    elif diff_y == 0:
        for x in range(x_start, x_end):
            if not m.passable((x, y_start)):
                return True
        return False


def AI_thread():
    global predatorList, prey, path, m, AI_PAUSED
    while AI_continue:
        # pause the simulation
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            AI_PAUSED = not AI_PAUSED
            time.sleep(0.5)

        if AI_PAUSED:
            continue
        # prey AI
        # calculate if the prey is in the field range of the predator
        # find the closest predator
        min_dist = 10000000
        escape_vector = [0, 0]
        for predator in predatorList:
            if (predator.get_pos()[0] - prey.get_pos()[0]) ** 2 + (predator.get_pos()[1] - prey.get_pos()[1]) ** 2 < prey.range_of_view ** 2:
                prey_dx = prey.get_pos()[0] - predator.get_pos()[0]
                prey_dy = prey.get_pos()[1] - predator.get_pos()[1]
                d = prey_dx ** 2 + prey_dy ** 2
                if d < min_dist:
                    d = min_dist
                    if prey.get_pos()[0] - predator.get_pos()[0] > 0:
                        escape_vector[0] = 1
                    elif prey.get_pos()[0] - predator.get_pos()[0] < 0:
                        escape_vector[0] = -1

                    if prey.get_pos()[1] - predator.get_pos()[1] > 0:
                        escape_vector[1] = 1
                    elif prey.get_pos()[1] - predator.get_pos()[1] < 0:
                        escape_vector[1] = -1
                    # print(escape_vector)
                    if m.passable(escape_vector) and m.in_bounds(escape_vector):
                        prey.set_target_pos(prey.get_pos()[0] + escape_vector[0], prey.get_pos()[1] + escape_vector[1])
                        prey.pathToTarget = a_star_search(m, (prey.get_pos()[0], prey.get_pos()[1]), prey.get_target_pos())

        if len(prey.pathToTarget) > 1 and prey.timer > prey.get_move_duration():
            # set direction to prey
            if len(prey.pathToTarget) > 4:
                lookingAt = 3
            else:
                lookingAt = len(prey.pathToTarget) - 1
            dx = prey.pathToTarget[lookingAt][0] - prey.get_pos()[0]
            dy = prey.pathToTarget[lookingAt][1] - prey.get_pos()[1]
            d = math.sqrt(dx ** 2 + dy ** 2)
            if d != 0:
                if dy > 0:
                    prey.direction_of_view = math.acos(dx / d)
                else:
                    prey.direction_of_view = math.pi * 2 - math.acos(dx / d)

            # move to the next node on path
            prey.move_to_next()

            # reset timer
            prey.timer = 0
        elif len(prey.pathToTarget) <= 1:
            # plan a new route if the no further nodes left
            # a star search
            set_auto_cruise_target(prey, prey.range_of_view)
            prey.pathToTarget = a_star_search(m, (prey.get_pos()[0], prey.get_pos()[1]), prey.get_target_pos())
        else:
            # wait for timer to reach move duration limit
            prey.timer += 1

        # mouse override prey pos
        if pygame.key.get_pressed()[pygame.K_a]:
            mpx, mpy = pygame.mouse.get_pos()
            # translate screen pixel mouse pos to world pos
            mouse_pos_x = mpx // 10
            mouse_pos_y = mpy // 10
            if (mouse_pos_x, mouse_pos_y) in m.walls:
                pass
            else:
                prey.set_pos((mouse_pos_x, mouse_pos_y))
                prey.pathToTarget = a_star_search(m, (prey.get_pos()[0], prey.get_pos()[1]), prey.get_target_pos())



        # for each predator
        for predator in predatorList:
            # print(is_line_blocked_by_wall(predator.get_pos()[0], predator.get_pos()[1], prey.get_pos()[0], prey.get_pos()[1]))
            # calculate if the prey is in the field range of the predator
            if (predator.get_pos()[0] - prey.get_pos()[0])**2 + (predator.get_pos()[1] - prey.get_pos()[1])**2 < predator.range_of_view ** 2:
                prey_dx = prey.get_pos()[0] - predator.get_pos()[0]
                prey_dy = prey.get_pos()[1] - predator.get_pos()[1]
                d = math.sqrt(prey_dx ** 2 + prey_dy ** 2)
                if d != 0:
                    # initialize temp local var angle
                    angle = 0
                    if prey_dy > 0:
                        angle = math.acos(prey_dx / d)
                    else:
                        angle = math.pi * 2 - math.acos(prey_dx / d)
                    # check if the angular position of the prey is in range
                    if predator.direction_of_view + predator.field_of_view / 2 > angle > predator.direction_of_view - predator.field_of_view / 2:
                        predator.set_target_pos(prey.get_pos()[0], prey.get_pos()[1])
                        # recalculate route
                        predator.pathToTarget = a_star_search(m, (predator.get_pos()[0], predator.get_pos()[1]), predator.get_target_pos())
                    else:
                        # if the prey is in range but out of view field angle, enter auto cruise mode
                        # if the predator reaches prey last sighted spot and found nothing
                        if predator.get_pos()[0] == predator.get_target_pos()[0] and predator.get_pos()[1] == predator.get_target_pos()[1]:
                            # randomly generate new prey pos until it is neither in the wall or out of the map
                            set_auto_cruise_target(predator, predator.range_of_view // 1)
            else:
                # if the predator reaches prey last sighted spot and found nothing
                if predator.get_pos()[0] == predator.get_target_pos()[0] and predator.get_pos()[1] == predator.get_target_pos()[1]:
                    # randomly generate new prey pos until it is neither in the wall or out of the map
                    set_auto_cruise_target(predator, predator.range_of_view // 1)
            ''' find path to prey
                without the range of view (max search depth parameter)
                the find path algorithm will use 100 as default
            '''

            # if didn't reach prey and allow to move
            if len(predator.pathToTarget) > 1 and predator.timer > predator.get_move_duration():
                # set direction to prey
                if len(predator.pathToTarget) > 4:
                    lookingAt = 3
                else:
                    lookingAt = len(predator.pathToTarget) - 1
                dx = predator.pathToTarget[lookingAt][0] - predator.get_pos()[0]
                dy = predator.pathToTarget[lookingAt][1] - predator.get_pos()[1]
                d = math.sqrt(dx**2 + dy**2)
                if d != 0:
                    if dy > 0:
                        predator.direction_of_view = math.acos(dx / d)
                    else:
                        predator.direction_of_view = math.pi * 2 - math.acos(dx / d)

                predator.move_to_next()

                # reset timer
                predator.timer = 0
            elif len(predator.pathToTarget) <= 1:
                # plan a new route if the no further nodes left
                # a star search
                predator.pathToTarget = a_star_search(m, (predator.get_pos()[0], predator.get_pos()[1]), predator.get_target_pos())
            else:
                # wait for timer to reach move duration limit
                predator.timer += 1

            if predator.get_pos() == prey.get_pos():
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
        # if event.type == pygame.KEYDOWN:
        #     if
    
    game_clock.tick(60)

# quit window
exit()