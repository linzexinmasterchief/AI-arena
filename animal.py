import pygame
import random

class bot():
    def __init__(self, center_position=[0, 0]):
        self.__center_position = center_position
        self.__move_duration = random.randint(5, 20)
        self.field_of_view = random.randint(5, 180)
        self.range_of_view = random.randint(1, 30)
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