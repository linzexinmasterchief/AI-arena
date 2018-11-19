class bot():
    def __init__(self, center_position = [0, 0], size = (10, 10), color = (255, 0, 0)):
        self.size = size
        self.color = color
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
        return [self.center_position[0] - (self.size[0] / 2), self.center_position[1] - (self.size[1] / 2)]
    
    def get_size(self):
        return self.size

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
