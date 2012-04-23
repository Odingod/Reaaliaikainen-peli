
from actor import Actor

import Box2D
import pygame
from settings import Settings

class Character(Actor):

    def __init__(self):
        Actor.__init__(self)

    def update(self, dt):
        pos = self.body.position
        self.rect.topleft = ( pos.x / Settings.B2SCALE, pos.y / Settings.B2SCALE)

    def createBody(self, b2world, w, h):
        bodyDef = Box2D.b2BodyDef()
        bodyDef.type = Box2D.b2_dynamicBody
        bodyDef.fixedRotation = True
        bodyDef.position = (Settings.B2SCALE * self.rect.left, Settings.B2SCALE * self.rect.top)
        bodyDef.bullet = True
        bodyDef.linearDamping = 6.0
        self.body = b2world.CreateBody(bodyDef)
        w /= 2
        h /= 2
        poly = Box2D.b2PolygonShape( box=(Settings.B2SCALE*w, Settings.B2SCALE*h, (Settings.B2SCALE*w,Settings.B2SCALE*h), 0) )
        
        self.body.CreateFixture(shape=poly, density=1, friction=0)
        return self.body
        