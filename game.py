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
        self.done = False

    def reset(train = True):
        if train:
            selected_test = random.choice(self.all_trains)
        else:
            selected_test = random.choice(self.all_tests)

        self.set_game(selected_test)
        return self.to_state()

    def step(angle, thrust):
        if self.done:
            raise RuntimeError("game is over")

        # update et output
        target_point = game.pod.angle_to_point(angle=angle)
        self.done, reward = game.pod.applyMove2(target_point, thrust=thrust)

        output_str = f"{target_point.x} {target_point.y} {thrust}"
        
        self.to_state(), reward, self.done, output_str

    def to_state(self):
        target_chkpt = game.pod.checkPointList[game.pod.nextCheckPointId]

        if game.pod.nextCheckPointId < len(game.pod.checkPointList)-1:
            futur_chkpt = game.pod.checkPointList[game.pod.nextCheckPointId+1]
        else:
            futur_chkpt = game.pod.checkPointList[game.pod.nextCheckPointId]

        return [
            game.pod.x, 
            game.pod.y, 
            game.pod.vx, 
            game.pod.vy, 
            game.pod.angle, 
            game.pod.diffAngle(target_chkpt), 
            game.pod.distance(target_chkpt), 
            game.pod.diffAngle(futur_chkpt), 
            game.pod.distance(futur_chkpt), 
        ]

    def set_game(self, test):
        self.pod = Pod(test[-1].x, test[-1].y, 0, 0, 0, 0, test)
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
        
        return ans
        

if __name__ == "__main__":
    game = Game()
    game.set_game(game.all_trains[0])
    loop = 0
    while loop < 1000:
        checkpt = game.pod.checkPointList[game.pod.nextCheckPointId]

        # partie a remplacer par un vrai algo
        angle = game.pod.diffAngle(checkpt)
        thrust = 50
        # update et output
        pt = game.pod.angle_to_point(angle=angle)
        isOver, _ = game.pod.applyMove2(pt, thrust=thrust)

        #print(f"{pt.x} {pt.y} {thrust}")
        if isOver:
            print(game.pod.score)  # should be 235.732
            break
        
        loop += 1 