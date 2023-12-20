#메인 캐릭터(user) 관련 클래스

from PIL import Image
import numpy as np

class Character:
    def __init__(self, width, height):
        self.appearance = Image.open('/home/kau-esw/ESW_BB/image/character.png')
        self.state = 'alive'
        self.health = 10
        self.speed = 4
        self.moving_gauge = 0
        self.position = np.array([width/2 - 7, height/2 - 7, width/2 + 7, height/2 + 7])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"
        self.hit = 0

    def move(self, command = None):
        if command['move'] == False:
            if self.moving_gauge < 100:
                self.moving_gauge += 0.5
            self.outline = "#FFFFFF" #가만히 있을 때 테두리 흰색
        
        else:
            self.outline = "#000000" #움직일 때 테두리 검정색!

            if command['up_pressed'] and self.position[1] > 0:
                self.position[1] -= self.speed
                self.position[3] -= self.speed
                
            if command['down_pressed'] and self.position[3] < 240:
                self.position[1] += self.speed
                self.position[3] += self.speed

            if command['left_pressed'] and self.position[0] > 0:
                self.position[0] -= self.speed
                self.position[2] -= self.speed
                
            if command['right_pressed'] and self.position[2] < 240:
                self.position[0] += self.speed
                self.position[2] += self.speed

        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])

    def live_check(self):
        if self.health == 0:
            self.state = 'dead'

    def set_image(self):
        if self.state == 'strong':
            self.appearance = Image.open('/home/kau-esw/ESW_BB/image/character_strong.png')
        elif self.state == 'hit':
            self.appearance = Image.open('/home/kau-esw/ESW_BB/image/character_hit.png')
        else:
            self.appearance = Image.open('/home/kau-esw/ESW_BB/image/character.png')

    def hitcheck(self):
        if self.hit > 0 and self.hit <= 3:
            self.state = 'hit'
            self.hit -= 1
            if self.hit == 0:
                self.state = 'alive'