from tile import Tile

from pygame.sprite import Group
from pygame.color import Color
from pygame.surface import Surface

import pygame

TILESIZE = 32

from tileset import TileSet

from math import ceil

class Level():

    width = 0
    height = 0
    tileset = None
    
    def __init__(self):

        self.tileSetFile = "media/Tiles.png"
        self.levelImageFile = ""
        
    def load(self):
        print "loading level"
        image = None
        
        try:
            image = pygame.image.load(self.levelImageFile).convert()
        except pygame.error as e:
            raise Exception("Failed to load level image!\n" + str(e))
        
        self.tileset = TileSet()
        self.tileset.load(self.tileSetFile)

        width, height = image.get_size()
        self.iwidth = width
        self.iheight = height
        self.width = TILESIZE * width
        self.height = TILESIZE * height
        
        self.tiles = [ None ] * width
        for x in range(width):
            self.tiles[x] = [ None ] * height
            for y in range(height):
                pixel = image.get_at((x,y))

                if pixel == (0,0,0):
                    tileimage = self.tileset.getTileImage(0)
                elif pixel == (237,28,36):
                    tileimage = self.tileset.getTileImage(1)
                elif pixel == (185,122,87):
                    tileimage = self.tileset.getTileImage(2)
                else:
                    continue
                self.tiles[x][y] = Tile(tileimage)
                
                
    def draw(self, screen, camera = (0,0) ):

        xi = max(0, camera[0] // TILESIZE)
        yi = max(0, camera[1] // TILESIZE)
        ox = TILESIZE * xi - camera[0]
        oy = TILESIZE * yi - camera[1]
        
        for x in range(0, int(ceil(800 / TILESIZE))+2 ):
            for y in range(0, int(ceil(600 / TILESIZE))+2 ):
                if xi+x >= self.iwidth or yi+y >= self.iheight or not self.tiles[xi+x][yi+y]:
                    continue
                screen.blit(self.tiles[xi+x][yi+y].image, pygame.Rect(x * TILESIZE + ox, y * TILESIZE + oy, TILESIZE, TILESIZE) )
                
    def update(self, scale):
        pass
if __name__ == "__main__":
    import main
    main.main()