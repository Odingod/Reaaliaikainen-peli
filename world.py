B2SCALE = 0.01

from tile import TILESIZE

import Box2D
import random
import threading

from chunk import *
from tileset import *
from settings import Settings
from pickup_orb import PickupOrb

import player
import game

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
        
        self.b2World = Box2D.b2World( gravity=(0,40), doSleep=True)
        
        self.player = player.Player( self.b2World, self.em, (100,100) )
        self.createRandomChunks(2)
        #self.chunks.append( self.createChunk("StartChunk") )
        
        self.player = player.Player( self.b2World, self.em, (game.WIDTH /2,game.HEIGHT - 100) )
        
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
        
        for chunk in self.chunks:
            chunk.update(dt)
            chunk.draw(self.game.screen, self.game.viewport)
        
        self.player.draw(self.game.screen, self.game.viewport)

        if self.chunks[-1].rect.colliderect(self.game.viewport):
            # Spawn a new chunk creating thread, this needs to be handled in its own
            # thread so that the game doesn't jam while we're creating the yet unseen
            # parts of the world
            ChunkCreationThread(self).start()
            
            if len(self.chunks) > 3:
                self.chunks.remove(self.chunks[0])
            

    def setCameraPos(self, x,y):
        self.game.viewport.topleft = (x,y)   
        
    def setCameraCenter(self, x,y):
        self.game.viewport.center = (x,y)
    
    def createRandomChunks(self, num = 1):
        pickup_probability = [10.0, 20.0]
        pickup_type = ["double_jump", "jumping_power"]
        
        # 1. Calculate the maximum velocity the player can reach : (delta)velocity = I / m
        velocity = (-self.player.default_jumping_power * Settings.B2SCALE) / self.player.body.mass
        
        # 2. Calculate the maximum Y distance with the calculated velocity
        Y_DIST_MAX = (((velocity*velocity)/(2*self.b2World.gravity.y))/Settings.B2SCALE)/2.5 #TODO: REMOVE DIVISION BY 4, JUST TESTING
        Y_DIST_MAX *= -1 
        Y_DIST_MIN = Y_DIST_MAX/2.0
        
        for i in range(num):
            if len(self.chunks) > 0:
                chunk_pos = (0, self.chunks[-1].rect.top - Settings.CHUNK_HEIGHT)
            else:
                chunk_pos = (0, 0)
            
            left_wall = Block((0, chunk_pos[1]), self, 0, 1, 19)
            right_wall = Block((768, chunk_pos[1]), self, 0, 1, 19)
            
            blocks = []
            pickups = []
            
            # If there are no other chunks, create a start chunk with a floor
            if (len(self.chunks) == 0):
                floor = Block((32, 544), self, 0, 23, 2)
                blocks.append(floor)
            
            reachable_height = 0.0
            
            while (abs(reachable_height) < abs(chunk_pos[1]) + abs(Settings.CHUNK_HEIGHT)): 
                # Block width and height (tile units)
                BLOCK_WIDTH = random.randint(3, 8)
                BLOCK_HEIGHT = 1
                BLOCK_TILE = 1
                
                # 3. Determine an interval [Y_MIN, Y_MAX]
                
                # If this chunk has blocks the interval is relative to the other
                # blocks of the chunk
                if (len(blocks) > 0):
                    Y_MIN = Y_DIST_MIN + blocks[-1].rect.top + blocks[-1].rect.height
                    Y_MAX = Y_DIST_MAX + blocks[-1].rect.top + blocks[-1].rect.height
                # If there were no blocks and there are other chunks the interval is relative
                # to the last chunk of the other block
                elif (len(self.chunks) > 0):
                    Y_MIN = Y_DIST_MIN + self.chunks[-1].objects[-3].rect.top + self.chunks[-1].objects[-3].rect.height
                    Y_MAX = Y_DIST_MAX + self.chunks[-1].objects[-3].rect.top + self.chunks[-1].objects[-3].rect.height
                # In case there were no chunks nor blocks, the interval is only relative to
                # the maximum distance the player can jump.
                else:
                    Y_MIN = Y_DIST_MIN + chunk_pos[1] + Settings.CHUNK_HEIGHT
                    Y_MAX = Y_DIST_MAX + chunk_pos[1] + Settings.CHUNK_HEIGHT
                
                # 4. Get a random coordinate for Y from the interval
                block_y = random.uniform(Y_MIN, Y_MAX)
                
                # 5. Calculate the maximum X distance for the given Y distance
                k = 4.0
                temp = k * (Y_MAX - block_y)
                
                # 6. Determine an interval [X_MIN, X_MAX]
                if (len(blocks) > 0):
                    X_MIN = blocks[-1].rect.right - blocks[-1].rect.width - abs(temp)
                    X_MAX = blocks[-1].rect.left + blocks[-1].rect.width + abs(temp)
                elif (len(self.chunks) > 0):
                    X_MIN = self.chunks[-1].objects[-3].rect.right - self.chunks[-1].objects[-3].rect.width - abs(temp)
                    X_MAX = self.chunks[-1].objects[-3].rect.left - self.chunks[-1].objects[-3].rect.width - abs(temp)
                else:
                    X_MIN = 0
                    X_MAX = Settings.CHUNK_WIDTH - BLOCK_WIDTH * TILESIZE
                
                if (X_MIN < 0):
                    X_MIN = 0
                if (X_MAX + (BLOCK_WIDTH * TILESIZE) > Settings.CHUNK_WIDTH):
                    X_MAX = Settings.CHUNK_WIDTH - BLOCK_WIDTH * TILESIZE
                                
                # 7. Get a random coordinate for X from the interval 
                block_x = random.uniform(X_MIN, X_MAX)
                
                # 8. Create a block at coordinates and append in to the blocks array 
                blocks.append(Block((block_x, block_y), self, BLOCK_TILE, BLOCK_WIDTH, BLOCK_HEIGHT))
                
                
                pup = random.randint(0, len(pickup_type)-1)
                if (100.0 - random.uniform(0.0, 100.0) < pickup_probability[pup]):
                    pickups.append(PickupOrb((blocks[-1].rect.centerx, blocks[-1].rect.centery - 34), self, self.em, pickup_type[pup], 500))

                reachable_height = block_y + Y_DIST_MAX 
        
            # Append the walls
            blocks.append(left_wall)
            blocks.append(right_wall)
        
            pickups.extend(blocks)
        
            objects = []
            objects.extend(pickups)
            objects.extend(blocks)
        
            # 9. Create the chunk with the blocks
            self.chunks.append(Chunk(self, chunk_pos, Settings.CHUNK_WIDTH, Settings.CHUNK_HEIGHT, objects, self.em))
        
class ChunkCreationThread(threading.Thread):

    def __init__(self, world):
        self.world = world
        threading.Thread.__init__(self)

    def run(self):
        self.world.createRandomChunks()
        

if __name__ == "__main__":
    pass
