
from pygame.rect import Rect
import pygame
from tile import TILESIZE

class Actor():

    def __init__(self):
        self.upsidedown = False
        
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
        left = self.rect.left - viewport.left
        top = self.rect.top - viewport.top
        width = self.image.get_rect().width
        height = self.image.get_rect().height

        if not self.upsidedown:
            screen.blit(self.image, (left, top))
        else:
            screen.blit(pygame.transform.flip(self.image, False, True), (left, top))
    
