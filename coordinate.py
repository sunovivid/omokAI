class c:
    def __init__(self, tuple):
        self.x = tuple[0]
        self.y = tuple[1]

    def __add__(self, coordinate):
        return (self.x + coordinate.x, self.y + coordinate.y)

    def __str__(self):
        return f"({self.x},{self.y})"

print(c((3,4)) + c((1,2)))