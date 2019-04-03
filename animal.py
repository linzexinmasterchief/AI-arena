import random
import math

class bot():
    def __init__(self, center_position=[0, 0]):
        self.__center_position = center_position
        self.__move_duration = random.randint(5, 20)
        self.field_of_view = random.random() * math.pi
        self.range_of_view = random.random() * 10 + 5
        self.direction_of_view = 0 # Radians 0 right, pi/2 up, pi left, 3pi/4 down
        self.timer = 0
        self.__target_x = center_position[0]
        self.__target_y = center_position[1]
        self.pathToTarget = []

    def get_pos(self):
        return self.__center_position

    def set_pos(self, center_position):
        self.__center_position = center_position
        pass

    def set_target_pos(self, x, y):
        self.__target_x = x
        self.__target_y = y

    def get_target_pos(self):
        return self.__target_x, self.__target_y

    def set_move_duration(self, move_duration):
        self.__move_duration = move_duration

    def get_move_duration(self):
        return self.__move_duration