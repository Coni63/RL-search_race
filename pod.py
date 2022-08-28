import sys
import math
from point import Point
from checkpoint import CheckPoint

class Pod(Point):
    def __init__(self, x, y, vx, vy, angle, nextCheckPointId, checkPointList):
        Point.__init__(self, x, y)
        self.vx = vx
        self.vy = vy
        self.nextCheckPointId = nextCheckPointId
        self.checkPointList = checkPointList
        self.angle = round(self.getAngle(self.checkPointList[self.nextCheckPointId]))
        self.points = 0
        self.turn = 0
    
    def __repr__(self):
        return f"{self.nextCheckPointId} {self.x} {self.y} {self.vx} {self.vy} {self.angle}"

    def rotate(self, angle):
        #rotate le pod de X deg (positif = clockwise)

        # On ne peut pas tourner de plus de 18° en un seul tour
        self.angle += max(min(angle, 18), -18)
        self.angle = self.angle % 360
    
    def boost(self, thrust):
        # Conversion de l'angle en radian
        ra = math.radians(self.angle)

        self.vx += math.cos(ra) * thrust
        self.vy += math.sin(ra) * thrust

    def checkCrossCheckPoint(self):
        checkpoint = self.checkPointList[self.nextCheckPointId]
        
        t = self.tCollision(checkpoint)

        if 0 <= t < 1:
            # print(f"Simulated Collision Time: {t}", file=sys.stderr, flush=True)
            self.nextCheckPointId += 1
            self.score = self.turn + t

    def tCollision(self, checkpoint):
        if (self.distance2(checkpoint) <= checkpoint.r2):
            return -1

        x2 = self.x - checkpoint.x
        y2 = self.y - checkpoint.y
        r2 = checkpoint.r

        # Both units are motionless
        a = self.vx * self.vx + self.vy * self.vy

        if a <= 0.0:
            return -1

        b = 2 * (x2 * self.vx + y2 * self.vy)
        c = (x2 * x2) + (y2 * y2) - (r2 * r2)
        delta = b * b - 4 * a * c

        if delta < 0.0:
            return -1

        t = (-b - math.sqrt(delta)) / (2.0 * a)

        if t <= 0.0:
            return -1

        return t

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def end(self):
        self.x = math.trunc(self.x)
        self.y = math.trunc(self.y)
        self.vx = math.trunc(self.vx * 0.85)
        self.vy = math.trunc(self.vy * 0.85)
        self.angle = round(self.angle)

    def applyMoves(self, actions):
        for angle, thrust in actions:
            self.applyMove(angle, thrust)

    def applyMove(self, angle, thrust):
        self.rotate(angle)
        self.boost(thrust)
        self.checkCrossCheckPoint(); # il faut ajouter le checkpoint
        self.move()
        self.end()
        return self.nextCheckPointId == len(self.checkPointList)-1

    def applyMove2(self, pt, thrust):
        angle = self.diffAngle(pt)
        self.rotate(angle)
        self.boost(thrust)
        self.checkCrossCheckPoint(); # il faut ajouter le checkpoint
        self.move()
        self.end()
        self.turn += 1
        return self.nextCheckPointId == len(self.checkPointList)-1
    
    def angle_to_point(self, angle):
        a = math.radians(self.angle + angle)
        px = self.x + math.cos(a) * 10000
        py = self.y + math.sin(a) * 10000

        return Point(round(px), round(py))

    def getAngle(self, pt : Point) -> float:
        # Retourne l'angle entre le pod to p par rapport à l'axe X
        
        d = self.distance(pt)
        dx = (pt.x - self.x) / d
        dy = (pt.y - self.y) / d

        # Trigonométrie simple. On multiplie par 180.0 / PI pour convertir en degré.
        a = math.degrees(math.acos(dx))

        # Si le point qu'on veut est en dessus de nous, il faut décaler l'angle pour qu'il soit correct.
        if (dy < 0):
            return 360 - a
        else:
            return a

    def diffAngle(self, pt: Point) -> float:
        a = self.getAngle(pt)

        # Pour connaitre le sens le plus proche, il suffit de regarder dans les 2 sens et on garde le plus petit
        # Les opérateurs ternaires sont la uniquement pour éviter l'utilisation d'un operateur % qui serait plus lent
        if self.angle <= a:
            right = a - self.angle
            left = self.angle + 360 - a
        else:
            right = 360 - self.angle + a
            left = self.angle - a

        if right < left:
            return right
        else:
            return -left