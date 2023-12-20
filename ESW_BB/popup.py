from PIL import ImageDraw, ImageFont

class Popup:
    def __init__(self, spawn_position, kinds, score):
        self.position = spawn_position
        self.score = score
        self.duration = 5
        self.state = 'write'
        self.kinds = kinds

    def show(self, draw, font):
        if self.duration > 0:
            draw.text((self.position), '%s +%d' %(self.kinds, self.score), (255, 255, 255), font = font)
            self.duration -= 1
            if self.duration == 0:
                self.state = 'erase'