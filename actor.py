
from pygame.rect import Rect

TILESIZE = 32

class Actor():

    def __init__(self):
        pass
        
    def update(self, dt):
        pass

    def draw(self, screen, viewport):
    
        for i in range(0, self.rect.width, self.tilew):
            for j in range(0, self.rect.height, self.tileh):
                
                screen.blit(self.image, Rect( \
                    TILESIZE*i - viewport.left + self.rect.left, \
                    TILESIZE*j - viewport.top + self.rect.top, \
                    self.image.get_rect().width, self.image.get_rect().height) )