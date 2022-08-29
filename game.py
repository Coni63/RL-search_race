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

    def reset(self, train = True):
        if train:
            selected_test = random.choice(self.all_trains)
        else:
            selected_test = random.choice(self.all_tests)

        return self.set_game(selected_test)

    def step(self, angle, thrust):
        if self.done:
            return self.to_state(), 0, self.done, ""

        if game.pod.turn >= 600:
            self.done = True
            return self.to_state(), 0, self.done, ""

        # update et output
        target_point = game.pod.angle_to_point(angle=angle)
        self.done, reward = game.pod.applyMove2(target_point, thrust=thrust)

        output_str = f"{target_point.x} {target_point.y} {thrust}"
        
        return self.to_state(), reward, self.done, output_str

    def to_state(self):
        if self.done:
            target_chkpt = game.pod.checkPointList[-1]
            futur_chkpt = game.pod.checkPointList[-1]
        elif game.pod.nextCheckPointId <= len(game.pod.checkPointList)-2:
            target_chkpt = game.pod.checkPointList[game.pod.nextCheckPointId]
            futur_chkpt = game.pod.checkPointList[game.pod.nextCheckPointId+1]
        else:
            target_chkpt = game.pod.checkPointList[game.pod.nextCheckPointId]
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
        checkpt = self.pod.checkPointList[0]
        self.pod.angle = self.pod.getAngle(checkpt)
        return self.to_state()
    
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
    state = game.set_game(game.all_trains[0]) # x, y, vx, vy, pod_angle, diff_angle_chkpt1, dist_chkpt1, diff_angle_chkpt2 dist_chkpt2 
    while True:        
        # partie a remplacer par un vrai algo
        angle = state[5]
        thrust = 50

        # update et output
        state, reward, done, output = game.step(angle, thrust)

        #print(f"{pt.x} {pt.y} {thrust}")
        if done:
            print("Final score = ", game.pod.score)  # should be 235.732
            break        