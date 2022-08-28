import glob
import random
import json
import math

from checkpoint import CheckPoint
from pod import Pod

class Game:
    def __init__(self):
        self.pod = None
        self.all_tests = [] 
        self.all_trains = []
        self.load_test()

    def reset(train = True):
        if train:
            selected_test = random.choice(self.all_trains)
        else:
            selected_test = random.choice(self.all_tests)

        return self.set_game(selected_test)

    def set_game(self, test):
        self.pod = Pod(test[-2].x, test[-2].y, 0, 0, 0, 0, test)
        checkpt = self.pod.checkPointList[self.pod.nextCheckPointId]
        angle = self.pod.getAngle(checkpt)
        self.pod.angle = angle
        return self.pod
    
    def load_test(self):
        for file in glob.glob("datasets/*.json"):
            with open(file, "r") as f:
                data = json.load(f)
            
            chkpt = self.createCheckpoints(data["testIn"])

            if data["isValidator"]:
                self.all_trains.append(chkpt)

            if data["isTest"]:
                self.all_tests.append(chkpt)

    def createCheckpoints(self, s: str) -> CheckPoint:
        ans = []
        chkpt_pos = s.split(";")
        chkpt_pos = chkpt_pos[1:] + chkpt_pos[:1]  # au depart al voiture est sur le dernier checkpoint car on vise le 0 eme
        for sub_str in chkpt_pos * 3:
            ptx, pty = [int(x) for x in sub_str.split(" ")]
            ans.append(CheckPoint(ptx, pty))
        
        # on créer un dernier point aligné avec les 2 derniers pour eviter tout freinage dans la derniere ligne droite
        # on s'assure que la distance est inf a 50000 pour le scoring
        dx = ans[-1].x - ans[-2].x
        dy = ans[-1].y - ans[-2].y
        r = 30000 / math.sqrt(dx*dx + dy*dy)
        ans.append(CheckPoint(ans[-1].x + r * dx, ans[-1].y + r * dy))
        return ans

    def default_test(self, thrust):
        self.set_game(self.all_trains[0])
        loop = 0
        while loop < 1000:
            checkpt = self.pod.checkPointList[self.pod.nextCheckPointId]

            # partie a remplacer par un vrai algo
            angle = self.pod.diffAngle(checkpt)
            #thrust = 50

            # update et output
            pt = self.pod.angle_to_point(angle=angle)
            isOver = self.pod.applyMove2(pt, thrust=thrust)

            #print(f"{pt.x} {pt.y} {thrust}")
            if isOver:
                print(self.pod.score)
                break
            
            loop += 1 

if __name__ == "__main__":
    game = Game()
    for i in range(10):
        game.default_test(30 + 10 * i)
