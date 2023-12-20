# 작은 몬스터 관련 클래스
import numpy as np

class Meat:
    def __init__(self, spawn_x, spawn_y):
        self.appearance = 'rectangle'
        self.state = 'cooked'
        self.position = np.array([spawn_x - 2, spawn_y - 2, spawn_x + 2, spawn_y + 2])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])



    def eat(self, user):
        collision = self.overlap(self.position, user.position)
        if collision:
            self.state = 'eaten'
            user.health += 1

    def overlap(self, this_position, object_position):
        if this_position[0] >= object_position[0] and this_position[1] >= object_position[1] and \
            this_position[2] <= object_position[2] and this_position[3] <= object_position[3]:
            return True