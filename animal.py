import pygame


class bot():
    def __init__(self, center_position=[0, 0], r=3):
        self.r = r
        self.center_position = center_position
        self.effect_list = []
        self.direction = 0

    def set_position(self, center_position):
        pass
    
    def set_direction(self, direction):
        self.direction = direction

    def set_speed(self, speed):
        self.speed = speed

    def next_step(self):
        pass

    def get_center_position(self):
        return self.center_position

    def get_graphic_position(self):
        return [self.center_position[0] - (self.r / 2), self.center_position[1] - (self.r / 2)]
    
    def get_r(self):
        return self.r

    def show(self, screen, type="predator"):
        if type == "predator":
            color = (255, 0, 0)
        elif type == "pray":
            color = (0, 255, 0)
        pygame.draw.circle(screen, color, (int(self.get_graphic_position()[0]), int(self.get_graphic_position()[1])), self.r, self.r)


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


class cornivore(animal):
    pass


class herbivore(animal):
    pass
