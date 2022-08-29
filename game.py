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

        if self.pod.turn >= 600:
            self.pod.score = 1000
            self.done = True
            return self.to_state(), 0, self.done, ""

        # update et output
        target_point = self.pod.angle_to_point(angle=angle)
        self.done, reward = self.pod.applyMove2(target_point, thrust=thrust)

        output_str = f"{target_point.x} {target_point.y} {thrust}"
        
        return self.to_state(), reward, self.done, output_str

    def to_state(self):
        if self.done:
            target_chkpt = self.pod.checkPointList[-1]
            futur_chkpt = self.pod.checkPointList[-1]
        elif self.pod.nextCheckPointId <= len(self.pod.checkPointList)-2:
            target_chkpt = self.pod.checkPointList[self.pod.nextCheckPointId]
            futur_chkpt = self.pod.checkPointList[self.pod.nextCheckPointId+1]
        else:
            target_chkpt = self.pod.checkPointList[self.pod.nextCheckPointId]
            futur_chkpt = self.pod.checkPointList[self.pod.nextCheckPointId]

        return [
            self.pod.x, 
            self.pod.y, 
            self.pod.vx, 
            self.pod.vy, 
            self.pod.angle, 
            self.pod.diffAngle(target_chkpt), 
            self.pod.distance(target_chkpt), 
            self.pod.diffAngle(futur_chkpt), 
            self.pod.distance(futur_chkpt), 
        ]

    def set_game(self, test_set):
        self.done = False
        self.pod = Pod(test_set[-1].x, test_set[-1].y, 0, 0, 0, 0, test_set)
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
    """
    Simulation d'une seule game
    """
    env = Game()
    state = env.set_game(env.all_trains[0]) # x, y, vx, vy, pod_angle, diff_angle_chkpt1, dist_chkpt1, diff_angle_chkpt2 dist_chkpt2 
    while True:        
        # partie a remplacer par un vrai algo
        angle = state[5]
        thrust = 50

        # update et output
        state, reward, done, output = env.step(angle, thrust)

        #print(f"{pt.x} {pt.y} {thrust}")
        if done:
            print("Test 1 - Final score = ", env.pod.score)  # should be 235.732
            break        
    print("\n\n")
    
    """
    Simulation d'un submit avec basic algo
    """
    env = Game()

    total_score = 0
    for test_set in env.all_tests:
        state = env.set_game(test_set)
        while True:        
            angle = state[5]
            thrust = 50

            state, reward, done, output = env.step(angle, thrust)

            if done:
                print("Final score = ", env.pod.score)
                total_score += env.pod.score
                break     
                
    print("Total Test score = ", total_score)  # should be 42415.8