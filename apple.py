import random

class Apple:
    def __init__(self, x_range, y_range, scale):
        self.x_position = random.randrange(scale, x_range - scale, scale)
        self.y_position = random.randrange(scale, y_range - scale, scale)
        self.position = [self.x_position, self.y_position]