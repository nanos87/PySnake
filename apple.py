import random

class Apple:
    def __init__(self, x_range, y_range, scale, pass_places):
        self.__x = x_range
        self.__y = y_range
        self.__scale = scale
        self.__to_pass = pass_places  # there could be places an apple shouldn't fall down - e.g. we have a snake there
        self.position = self.__get_random_position()
    
    def __get_random_position(self):
        x_position = random.randrange(self.__scale, self.__x - self.__scale, self.__scale)
        y_position = random.randrange(self.__scale, self.__y - self.__scale, self.__scale)
        position = [x_position, y_position]

        return position if position not in self.__to_pass else self.__get_random_position()