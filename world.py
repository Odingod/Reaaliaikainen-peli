
import json

from chunk import *

import Box2D

from tileset import *

class World(object):

    chunks = [ ]
    background = None
    chunkdata = None
    b2World = None
    tileset = None
    
    def __init__(self, game, eventMgr):
        self.game = game
        self.em = eventMgr

    def loadLevel(self, filename):
        self.tileset = Tileset()
        self.tileset.load("media/Tiles.png")
        self.loadChunkFile(filename)
        
        self.b2World = Box2D.b2World( gravity=(0,10), doSleep=True)
        
        self.chunks.append( self.createChunk("StartBlock") )
        
    def createChunk(self, name):
        return Chunk( self, (0,0), self.chunkdata[name] )
        
    def update(self, dt):

        self.b2World.Step(dt/1000, 6, 2)
        self.b2World.ClearForces()
        
        for chunk in self.chunks:
            chunk.update(dt)
            chunk.draw(self.game.screen, self.game.viewport)
        

    def setCameraPos(x,y):
        self.game.rect.topleft = (x,y)   
        
    def setCameraCenter(x,y):
        self.game.rect.center = (x,y)
                
    def loadChunkFile(self, filename):
        # ladataan json tiedosto
        try:
            f = file(filename, "r")
            self.chunkdata = json.load(f)
            f.close()
        except IOError:
            print "Failed to open file", filename
            return
        except ValueError as e:
            print "Failed to parse json-file:", e
            raise
            
if __name__ == "__main__":
    pass
    