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
        self.threadLock = threading.Lock()
        
    def loadLevel(self, filename):
        self.tileset = Tileset()
        self.tileset.load("media/Tiles.png")
        
        self.b2World = Box2D.b2World( gravity=(0,40), doSleep=True)
        
        #self.player = player.Player( self.b2World, self.em, (100,100) )
        self.player = player.Player( self.b2World, self.em, (game.WIDTH /2, game.HEIGHT - 100))
        self.createChunks(2)
        
        
    def update(self, dt):

        self.b2World.Step( 1 / 60.0, 6, 3)
        self.b2World.ClearForces()
        
        self.player.update(dt)
        
        for chunk in self.chunks:
            self.game.screen.blit(chunk.background, (0, chunk.rect.top-self.game.viewport.top))
        for chunk in self.chunks:
            chunk.update(dt)
            chunk.draw(self.game.screen, self.game.viewport)
        
        self.player.draw(self.game.screen, self.game.viewport)

        if self.chunks[-1].rect.colliderect(self.game.viewport):
            # Spawn a new chunk creating thread, this needs to be handled in its own
            # thread so that the game doesn't jam while we're creating the yet unseen
            # parts of the world
            ChunkCreationThread(self, 1).start()
            
            if len(self.chunks) > 10:
                self.chunks.remove(self.chunks[0])
            

    def setCameraPos(self, x,y):
        self.game.viewport.topleft = (x,y)   
        
    def setCameraCenter(self, x,y):
        self.game.viewport.center = (x,y)
    

    def createChunks(self, num =1):
        pickup_probability = [10.0, 20.0, 10.0, 0.05, 20.0]
        pickup_type = ["double_jump", "jumping_power", "trampoline", "no_hurry", "double_points"]
        
        # Calculate the maximum velocity the player can reach : dv = I / m
        velocity = (self.player.default_jumping_power * Settings.B2SCALE) / self.player.body.mass
        
        # Calculate the maximum Y distance with the calculated velocity: v^2/2g
        Y_DIST_MAX = ((((velocity*velocity)/(2*self.b2World.gravity.y))/Settings.B2SCALE) * -1)/2.5
        
        # Minimum Y distance will be the player's height + TILESIZE + tolerance of 5, this ensures
        # that the player can always fit between the blocks
        Y_DIST_MIN = ((self.player.rect.height)*-1) - TILESIZE - 5
        
        for i in range(num):
            # Determine the position of the new chunk
            if (len(self.chunks) > 0):
                chunk_pos = (0, self.chunks[-1].rect.top - Settings.CHUNK_HEIGHT)
            else:
                chunk_pos = (0, 0)
            
            # Initialize the block and pickup arrays
            blocks = []
            pickups = []
            
            # If this is the first block of the first chunk then create the floor
            if (len(self.chunks) == 0):
                floor = Block((32, 544), self, 0, 23, 2)
                blocks.append(floor)
            
            # Initialize reachable height, describes the height the player can reach
            # with the current blocks and jump power
            reachable_height = 0.0
            
            while (abs(reachable_height) < abs(chunk_pos[1]) + abs(Settings.CHUNK_HEIGHT)):
                # Initialize block parameters, can be randomized if necessary
                BLOCK_WIDTH = random.randint(3, 12)
                BLOCK_HEIGHT = 1
                BLOCK_TILE = 1
                
                # Determine an interval [Y_MIN, Y_MAX]
                
                # If this chunk has blocks, the Y interval is relative to the previous
                # block in this chunk
                if (len(blocks) > 0):
                    Y_MIN = Y_DIST_MIN + blocks[-1].rect.top 
                    Y_MAX = Y_DIST_MAX + blocks[-1].rect.top
                # If there were no blocks and there are other chunks the interval is relative
                # to the last block of the previous chunk
                elif (len(self.chunks) > 0):
                    Y_MIN = Y_DIST_MIN + self.chunks[-1].objects[-3].rect.top
                    Y_MAX = Y_DIST_MAX + self.chunks[-1].objects[-3].rect.top
                # In case we're talking about the first block of the first chunk the position is
                # relative to the chunk's position
                else:
                    Y_MIN = Y_DIST_MIN + chunk_pos[1]
                    Y_MAX = Y_DIST_MAX + chunk_pos[1]
                
                # Get a random coordinate from the interval [Y_MIN, Y_MAX]
                block_y = random.uniform(Y_MIN, Y_MAX)
                
                # Calculate the maximum X distance for the given Y coordinate
                #time = velocity / self.b2World.gravity.y
                #horDistPeak = time * self.player.xspeed
                #horDistLevel = 2 * horDistPeak
                #r = (Y_MAX - block_y) / Y_DIST_MAX
                #X_DIST_MAX = horDistLevel * (1+r)
                X_DIST_MAX = self.player.xspeed * velocity / self.b2World.gravity.y * (1 + (Y_MAX -block_y)/Y_DIST_MAX)
                
                # Determine an interval [X_MIN, X_MAX]
                if (len(blocks) > 0):
                    X_MIN = blocks[-1].rect.right - blocks[-1].rect.width - X_DIST_MAX
                    X_MAX = blocks[-1].rect.left + blocks[-1].rect.width + X_DIST_MAX
                elif (len(self.chunks) > 0):
                    X_MIN = self.chunks[-1].objects[-3].rect.right - self.chunks[-1].objects[-3].rect.width - X_DIST_MAX
                    X_MAX = self.chunks[-1].objects[-3].rect.left + self.chunks[-1].objects[-3].rect.width + X_DIST_MAX
                else:
                    X_MIN = TILESIZE
                    X_MAX = Settings.CHUNK_WIDTH - (BLOCK_WIDTH * (TILESIZE+1))
                   
                # Sanity check for the X interval
                if (X_MIN < TILESIZE):
                    X_MIN = TILESIZE
                if (X_MAX + (BLOCK_WIDTH * (TILESIZE+1)) > Settings.CHUNK_WIDTH):
                    X_MAX = Settings.CHUNK_WIDTH - (BLOCK_WIDTH * (TILESIZE+1))
                    
                # Get a random coordinate for X from the interval [X_MIN, X_MAX]
                block_x = random.uniform(X_MIN, X_MAX)
                
                # Create a block at the coordinates and append it into the blocks array
                blocks.append(Block((block_x, block_y), self, BLOCK_TILE, BLOCK_WIDTH, BLOCK_HEIGHT))
                
                # Check whether this block contains a pick up
                pup = random.randint(0, len(pickup_type)-1)
                if (100.0 - random.uniform(0, 100.0) < pickup_probability[pup]):
                    pickups.append(PickupOrb((blocks[-1].rect.centerx, blocks[-1].rect.centery - 34), self, self.em, pickup_type[pup], 500))

                # Update the reachable height
                reachable_height = block_y + Y_DIST_MAX
            
            # Create and append the walls of the chunk
            left_wall = Block((0, chunk_pos[1]), self, 0, 1, 19)
            right_wall = Block((768, chunk_pos[1]), self, 0, 1, 19)

            blocks.append(left_wall)
            blocks.append(right_wall)
            
            objects = []
            objects.extend(pickups)
            objects.extend(blocks)
            
            # Create the chunk with all the objects
            self.chunks.append(Chunk(self, chunk_pos, Settings.CHUNK_WIDTH, Settings.CHUNK_HEIGHT, objects, self.em))
            

# This thread is used to specifically create chunks so that the playing experience is not
# affected by the creation process
class ChunkCreationThread(threading.Thread):

    def __init__(self, world, num =1):
        self.world = world
        self.num = num
        threading.Thread.__init__(self)

    def run(self):
        self.world.threadLock.acquire()
        try:
            self.world.createChunks(self.num)
        finally:
            self.world.threadLock.release()

if __name__ == "__main__":
    pass
