#총알 관련 클래스

from PIL import Image
import numpy as np

class Bullet:
    def __init__(self, position, command, toward):
        self.appearance = Image.open('/home/kau-esw/ESW_BB/image/bullet.png')
        self.speed = 10
        self.damage = 1
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.direction = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        self.state = 'shot'
        #최근에 바라본 방향으로 날아감
        if command['up_pressed']:
            self.direction['up'] = True
        if command['down_pressed']:
            self.direction['down'] = True
        if command['right_pressed']:
            self.direction['right'] = True
        if command['left_pressed']:
            self.direction['left'] = True
        #아무 방향도 입력되지 않으면 이전현재 toward 방향으로 총알 발사
        if not command['up_pressed'] and not command['down_pressed'] and not command['left_pressed'] and not command['right_pressed']:
            self.direction[toward] = True

    def move(self):
        if self.direction['up']:
            self.position[1] -= self.speed
            self.position[3] -= self.speed

        if self.direction['down']:
            self.position[1] += self.speed
            self.position[3] += self.speed

        if self.direction['left']:
            self.position[0] -= self.speed
            self.position[2] -= self.speed
            
        if self.direction['right']:
            self.position[0] += self.speed
            self.position[2] += self.speed
            
    def collision_check(self, list):
        for mob in list:
            collision = self.overlap(self.position, mob.position)
            
            if collision:
                mob.health -= self.damage
                self.state = 'hit'

    def overlap(self, this_position, object_position):
        return this_position[0] >= object_position[0] and this_position[1] >= object_position[1] \
                 and this_position[2] <= object_position[2] and this_position[3] <= object_position[3]

    def out_check(self):
        if self.position[0] == 0 or self.position[1] == 0 or self.position[2] == 240 or self.position[3] == 240:
            self.state = 'out'