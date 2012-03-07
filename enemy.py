
from character import Character
from pygame.rect import Rect

class Enemy(Character):

    def __init__(self):
        Character.__init__(self)
        self.image = None
        self.rect = Rect(0,0,0,0)

    def update(self, dt):
        pass

    def runAI(self):
        pass
