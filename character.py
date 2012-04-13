
from actor import Actor

import Box2D
import pygame
from world import B2SCALE

class Character(Actor):

    def __init__(self):
        Actor.__init__(self)

    def update(self, dt):
        pos = self.body.position
        self.rect.topleft = ( pos.x / B2SCALE, pos.y / B2SCALE)

    def createBody(self, b2world, w, h):
        bodyDef = Box2D.b2BodyDef()
        bodyDef.type = Box2D.b2_dynamicBody
        bodyDef.fixedRotation = True
        bodyDef.position = (B2SCALE * self.rect.left, B2SCALE * self.rect.top)
        bodyDef.bullet = True
        bodyDef.linearDamping = 5.0
        bodyDef.angularDamping = 69
        self.body = b2world.CreateBody(bodyDef)
        w /= 2
        h /= 2
        poly = Box2D.b2PolygonShape( box=(B2SCALE*w, B2SCALE*h, (B2SCALE*w,B2SCALE*h), 0) )
        
        self.body.CreateFixture(shape=poly, density=1, friction=0)
            
        return self.body
        