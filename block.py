
import pygame
import Box2D

from tile import TILESIZE
from world import B2SCALE
from actor import *

class Block(Actor):

    image = None
    def __init__(self, pos, world, tile, width, height, tilew=1, tileh=1 ):
        self.rect = pygame.Rect(pos[0], pos[1], width, height) # HUOM: width ja height tileissa
        print self.rect
        
        self.tilew = tilew
        self.tileh = tileh
         
        self.image = world.tileset.getTile(tile, tilew, tileh)
        
        w = width * TILESIZE * B2SCALE * 0.5
        h = height * TILESIZE * B2SCALE * 0.5
        
        bodyDef = Box2D.b2BodyDef()
        bodyDef.type = Box2D.b2_staticBody
        bodyDef.position = (B2SCALE * self.rect.left, B2SCALE * self.rect.top)
        self.body = world.b2World.CreateBody(bodyDef)

        bshape = Box2D.b2PolygonShape( box=(w, h, (w, h), 0) )
        self.body.CreateFixture(shape=bshape, density=1)
        
    def draw(self, screen, viewport):
        Actor.drawTiled(self, screen, viewport)
        