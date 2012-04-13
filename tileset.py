import pygame

from tile import TILESIZE

class Tileset(object):

    height = 0
    width = 0
    image = None
    
    def __init__(self):
        pass

    def getTile(self, i, w = 1, h = 1):
        x = i % self.width
        y = i // self.width
        return self.image.subsurface( pygame.Rect( TILESIZE * x, TILESIZE * y , TILESIZE * w, TILESIZE * h ) )
    
    def load(self, filename):
        try:
            self.image = pygame.image.load(filename) #.convert()
        except pygame.error as e:
            raise Exception("Failed to load tileset-image\n" + str(e))

        self.width, self.height = self.image.get_size()
        self.width //= TILESIZE
        self.height //= TILESIZE
        