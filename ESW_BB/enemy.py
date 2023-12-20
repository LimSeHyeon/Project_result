# 작은 몬스터 관련 클래스

from PIL import Image
import numpy as np

class Enemy:
    def __init__(self, spawn_position):
        self.appearance = Image.open('/home/kau-esw/ESW_BB/image/smallmob.png')
        self.state = 'alive'
        self.health = 1
        self.position = np.array([spawn_position[0] - 10, spawn_position[1] - 10, spawn_position[0] + 10, spawn_position[1] + 10])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#000000"

    def move(self,usercenter):
        if self.center[0] > usercenter[0]:
            self.position[0] -= 1
            self.position[2] -= 1
        else:
            self.position[0] += 1
            self.position[2] += 1
        
        if self.center[1] > usercenter[1]:
            self.position[1] -= 1
            self.position[3] -= 1
        else:
            self.position[1] += 1
            self.position[3] += 1

        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])

    def check(self):
        if self.health == 0:
            self.state = 'dead'

    def kiss(self, user):
        collision = self.overlap(self.position, user.position)
        if collision:
            self.health = 0
            if user.state != 'strong' and user.health > 0:
                    user.health -= 1
                    user.hit = 3

    def overlap(self, this_position, object_position):
        if (((this_position[0]+3 >= object_position[2]  and object_position[2] >= this_position[0]) and \
                ((object_position[1] > this_position[1] and object_position[1] < this_position[3]) or \
                (object_position[3] > this_position[1] and object_position[3] < this_position[3]))) or \
            ((this_position[2]-3 <= object_position[0] and object_position[0] <= this_position[2])and \
                ((object_position[1] > this_position[1] and object_position[1] < this_position[3] or \
                object_position[3] > this_position[1] and object_position[3] < this_position[3]))) or \
            ((this_position[1]+3 >= object_position[3] and object_position[3] >= this_position[1])and \
                ((object_position[0] > this_position[0] and object_position[0] < this_position[2]) or \
                (object_position[2] > this_position[0] and object_position[2] < this_position[2]))) or \
            (this_position[3]-3 <= object_position[1] and object_position[1] <= this_position[3])and \
                ((object_position[0] > this_position[0] and object_position[0] < this_position[2]) or \
                (object_position[2] > this_position[0] and object_position[2] < this_position[2]))):    
            return True