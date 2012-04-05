
from pygame.rect import Rect

class Actor():

    def __init__(self):
        pass
        
    def update(self, dt):
        pass

    def draw(self, screen, viewport):
        screen.blit(self.image, Rect(-viewport.left-self.rect.left, -self.rect.top-viewport.top, \
                    self.rect.width, self.rect.height) )