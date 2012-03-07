from tile import Tile
import json


from pygame.sprite import Group



class Level(Group):

    width = 0
    height = 0
    camera = (0, 0)
    
    def __init__(self):
        Group.__init__(self)
        
    
    def loadLevelImage(self, ifile):
        print "LevelImage:", ifile

        """
        for x,y in :
            tile = Tile()
            self.add( tile )
        """

    # def update(self):
    # def draw(self):
    
if __name__ == "__main__":
    import events
    l = Level()
    l.loadLevelImage("levels/mappi.png")
