
from actor import *
from pygame.rect import Rect

#from imagecont import *

import pygame
import Box2D

B2SCALE = 0.1

class Block(Actor):

    image = None
    def __init__(self, b2World, image, x, y, width, height ):
        self.rect = Rect(x, y, width, height)
        self.image = pygame.image.load("media/Character.png")
        #self.image = ImageContainer.getImage(name)
        
        w = width * B2SCALE
        h = height * B2SCALE
        cx = (x + width / 2) * B2SCALE
        cy = (y + height / 2) * B2SCALE
        
        bodyDef = Box2D.b2BodyDef()
        bodyDef.type = Box2D.b2_staticBody
        bodyDef.position = (B2SCALE * self.rect.left, B2SCALE * self.rect.top)
        self.body = b2World.CreateBody(bodyDef)

        bshape = Box2D.b2PolygonShape( box=(w, h) )
        self.body.CreateFixture(shape=bshape, density=1)
        
        
    def update(self, dt):
        pass
        