
from pygame.rect import Rect
from tile import TILESIZE

class Actor():

    def __init__(self):
        pass
        
    def update(self, dt):
        pass

    def drawTiled(self, screen, viewport):
        for i in range(0, self.rect.width, self.tilew):
            for j in range(0, self.rect.height, self.tileh):
                
                screen.blit(self.image, Rect( \
                    TILESIZE*i + self.rect.left - viewport.left, \
                    TILESIZE*j + self.rect.top - viewport.top, \
                    self.image.get_rect().width, self.image.get_rect().height) ) 

    def draw(self, screen, viewport):
        screen.blit(self.image, Rect( \
            self.rect.left - viewport.left, \
            self.rect.top - viewport.top, \
            self.image.get_rect().width, self.image.get_rect().height) )