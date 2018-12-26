import pygame

class bot():
    def __init__(self, center_position=[0, 0]):
        self.__center_position = center_position
        self.__effect_list = []
        self.__direction = 0

    def set_pos(self, center_position):
        self.__center_position = center_position
        pass
    
    def set_direction(self, direction):
        self.__direction = direction

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def next_step(self):
        pass

    def get_pos(self):
        return self.__center_position

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
