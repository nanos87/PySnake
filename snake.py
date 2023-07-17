class Snake:

    def __init__(self, court, scale):
        self.head = list(map(lambda s: s/2, court))
        self.body = []
        self.is_alive = True
        self.__scale = scale
        self.__court = court
    
    def move(self, vector = [0, 0]):              
        # move body if exist
        if len(self.body) > 0:
            # shift each body position element one element up the list
            self.body.append(self.head.copy())
            self.body = self.body[-(len(self.body)-1):]

        # move head by given vector
        for i in range(0, len(vector)):
            self.head[i] += vector[i] * self.__scale


    def try_eat(self, food_position: [int]) -> bool:
        if self.head == food_position:
            self.grow()
            return True
        return False

    def grow(self):
        self.body.append(self.head.copy())

    def died(self) -> bool:
        # check collision with walls or with snake body
        self.is_alive = not (any([val >= ran - self.__scale or val < self.__scale for val, ran in zip(self.head, self.__court)]) 
                or self.head in self.body)
        return not self.is_alive