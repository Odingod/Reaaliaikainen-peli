B2SCALE = 0.01

import json
import Box2D

from chunk import *
from tileset import *

import player

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
        
        self.b2World = Box2D.b2World( gravity=(0,40), doSleep=True)
        
        self.chunks.append( self.createChunk("StartChunk") )
        
        self.player = player.Player( self.b2World, self.em, (100,100) )
        
    def createChunk(self, name):
        if len(self.chunks) > 0:
            pos = (0, self.chunks[-1].rect.top-self.chunkdata[name]['Height'])
        else:
            pos = (0,0)
        return Chunk( self, pos, self.chunkdata[name], self.em)
        
    def update(self, dt):

        self.b2World.Step( 1 / 60.0, 6, 3)
        self.b2World.ClearForces()
        
        self.player.update(dt)
        self.player.draw(self.game.screen, self.game.viewport)
        
        for chunk in self.chunks:
            chunk.update(dt)
            chunk.draw(self.game.screen, self.game.viewport)
        
        
        if self.chunks[-1].rect.colliderect(self.game.viewport):
            print 'new chunk created'
            self.chunks.append(self.createChunk(self.chunks[-1].getNext()))
            if len(self.chunks) > 3:
                self.chunks.remove(self.chunks[0])
            

    def setCameraPos(self, x,y):
        self.game.viewport.topleft = (x,y)   
        
    def setCameraCenter(self, x,y):
        self.game.viewport.center = (x,y)
                
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
    
