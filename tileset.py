import pygame

TILESIZE = 32

class TileSet(object):

    tiles = { }
    image = None
    
    def __init__(self):
        pass

    def getTileImage(self, i):
        try:
            return self.tiles[i]
        except ValueError:
            return None
    
    def load(self, filename):
        print "loading tileset"
        try:
            self.image = pygame.image.load(filename) #.convert()
        except pygame.error as e:
            raise Exception("Failed to load tileset-image\n" + str(e))

        width, height = self.image.get_size()
        width //= TILESIZE
        height //= TILESIZE
        print "tiles:",  width, height

        for x in range(width):
            for y in range(height):
                r = pygame.Rect(x*(TILESIZE+1), y*(TILESIZE+1), TILESIZE, TILESIZE)
                self.tiles[x+width*y] = self.image.subsurface( r )
