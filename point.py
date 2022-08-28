class Point:
    pass

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, pt: Point) -> float:
        return self.distance2(pt)**0.5

    def distance2(self, pt: Point) -> float:
        return (self.x-pt.x)**2 + (self.y-pt.y)**2

    def closest(self, a: Point, b: Point) -> Point:
        da = b.y - a.y
        db = a.x - b.x
        c1 = da*a.x + db*a.y
        c2 = -db*self.x + da*self.y
        det = da*da + db*db
        cx = 0
        cy = 0

        if det != 0 :
            cx = (da*c1 - db*c2) / det
            cy = (da*c2 + db*c1) / det
        else:
            cx = self.x
            cy = self.y

        return Point(cx, cy)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"