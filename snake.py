class Snake:

    def __init__(self, court, scale):
        self.head = list(map(lambda s: s/2, court))
        self.body = []
        self.is_alive = True
        self.__scale = scale
        self.__court = court

    def get_nose_to_tail(self):
        return [self.head, *self.body]
    
    def move(self, vector = [0, 0]):              
        # move body if exist
        bodyLength = len(self.body)
        if  bodyLength > 0:
            # shift each body position element one element up the list
            self.body.append(self.head.copy())
            self.body = self.body[-bodyLength:]

        # move head by given vector
        self.head = [pos + delta * self.__scale for pos, delta in zip(self.head, vector)]

    def try_eat(self, food_position: [int]) -> bool:
        can_eat = self.head == food_position
        if can_eat:
            self.__grow()
        return can_eat

    def died(self) -> bool:
        # check collision with walls
        died = any([pos >= border - self.__scale or pos < self.__scale for pos, border in zip(self.head, self.__court)])
        # or own body
        died = died or self.head in self.body
        self.is_alive = not died
        return died

    def __grow(self):
        self.body.append(self.head.copy())