from point import Point

class CheckPoint(Point):
    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.r = 600
        self.r2 = 360000