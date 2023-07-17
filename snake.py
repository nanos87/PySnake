class Snake:

    def __init__(self, x_range, y_range):
        self.head = [x_range / 2, y_range / 2]
        self.body = []
        self.length = 0
        self.is_grown = False
    
    def move(self, scale, vector = [0, 0]):
        # save former head position 'copy method is needed to copy values not reference'
        former_position = self.head.copy()
        # move head by vector
        for i in range(0,2,1):
            self.head[i] += vector[i] * scale
        # move body if exist
        if self.length > 0:
            if self.is_grown:
                self.body.append(former_position)
                self.is_grown = False
            # shift each body position element one element up the list
            for i in range(0, self.length, 1):
                if i < self.length - 1:
                    self.body[i] = self.body[i + 1]
                else:
                    self.body[i] = former_position

    def eat(self, x_target, y_target):
        if self.head == [x_target, y_target]:
            self.length += 1
            self.is_grown = True
            return True
        else:
            return False

    def die(self, x_range, y_range, scale):
        # check collision with walls
        if self.head[0] >= x_range - scale or self.head[0] < scale:
            return True
        elif self.head[1] >= y_range - scale or self.head[1] < scale:
            return True
        # check collision with snake body
        for position in self.body:
            if self.head[0] == position[0] and self.head[1] == position[1]:
                return True
        return False