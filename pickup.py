import Box2D
import pygame
from actor import Actor
from world import B2SCALE

class Pickup(Actor):
    def __init__(self, pos, world, eventMgr):
        Actor.__init__(self)
        self.em = eventMgr
        eventMgr.register(self)
        self.world = world
        
        self.picked = False
        
        self.image = pygame.image.load("media/orb.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.width = 32
        self.rect.height = 32
        
        bodyDef = Box2D.b2BodyDef()
        bodyDef.type = Box2D.b2_staticBody
        bodyDef.position = (B2SCALE * (self.rect.left + 0.5 * self.rect.width), B2SCALE * (self.rect.top + 0.5 * self.rect.height))
        self.body = world.b2World.CreateBody(bodyDef)
        r = B2SCALE * self.rect.width * 0.5
        self.body.CreateCircleFixture(radius=r)
        
    def notify(self, event):
        pass

    def update(self, dt):
        if self.body.contacts and self.body.contacts[0].contact.touching:
            self.picked = True
            if self.body.fixtures:
                self.body.DestroyFixture(self.body.fixtures[0])

    def draw(self, screen, viewport):
        if not self.picked:
            Actor.draw(self, screen, viewport)
    def __del__(self):
        self.world.b2World.DestroyBody(self.body)
