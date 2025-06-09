FIELD = [
    ['EMPTY', 'WALL',  'EMPTY', 'BOX' ],
    ['EMPTY', 'EMPTY', 'WALL',  'EXIT'],
    ['BOX',   'EMPTY', 'EMPTY', 'EMPTY']
]



class Robot:
    def __init__(self, field, x=0, y=0):
        self.field = field
        self.x = x
        self.y = y
        self.history = []
    def move_forward(self, steps=1):
        # Для простоты — всегда вправо (x + steps), потом добавим направление
        for _ in range(steps):
            nx, ny = self.x + 1, self.y
            if nx < len(self.field[0]) and self.field[self.y][nx] != 'WALL':
                self.x = nx
                self.history.append((self.x, self.y))
                print(f"Robot moved to ({self.x},{self.y})")
            else:
                print(f"Robot can't move forward from ({self.x},{self.y})")
                break
    def __str__(self):
        return f"Robot at ({self.x},{self.y})"
