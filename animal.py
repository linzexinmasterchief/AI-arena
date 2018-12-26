import pygame
import random

class bot():
    def __init__(self, center_position=[0, 0]):
        self.__center_position = center_position
        self.__move_duration = random.randint(1, 10)
        self.timer = 0
        self.pathToTarget = []

    def get_pos(self):
        return self.__center_position

    def set_pos(self, center_position):
        self.__center_position = center_position
        pass

    def set_move_duration(self, move_duration):
        self.__move_duration = move_duration

    def get_move_duration(self):
        return self.__move_duration

class animal(bot):
    
    def __init__(self, gender, x = 0, y = 0):
        self.x = x
        self.y = y
        self.gender = gender

    def move(self):
        pass

    def attack(self):
        pass

    def eat(self):
        pass

    def rest(self):
        pass
    
    def reproduce(self):
        pass


class predator(animal):
    # hunt pray
    pass


class pray(animal):
    # escape from predator
    pass
