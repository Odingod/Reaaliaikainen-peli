from character import Character

import pygame

from world import B2SCALE

class Player(Character):

    def __init__(self, b2World, eventMgr, pos):
        Character.__init__(self)
        
        self.em = eventMgr
        eventMgr.register(self)
        
        self.keys = [False] * 5
        self.image = pygame.image.load("media/Character.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.width = 47
        self.rect.height = 64
        self.jumped = False
        self.createBody(b2World, self.rect.width, self.rect.height )
        
    def canJump(self):
        if abs(self.body.linearVelocity[1] ) > 0.1:
            return False
        for contact_edge in self.body.contacts:
            c = contact_edge.contact
            if c.manifold.localNormal[1] < -0.9:
                return True
        return False
        
    def update(self, dt):
        Character.update(self, dt)
        if self.keys[2]:
            self.body.linearVelocity = (-400 * B2SCALE, self.body.linearVelocity[1] )
        if self.keys[3]:
            self.body.linearVelocity = (400 * B2SCALE, self.body.linearVelocity[1] )
        if self.keys[1]:
            if abs(self.body.linearVelocity[1] ) < 0.01:
                self.body.ApplyLinearImpulse(impulse=(0, -480 * B2SCALE), point=(0,0))
                self.jumped = True
        else:
            self.jumped = False
            
    def notify(self, event):
        if event.name == 'Keyboard':
            key = event.key
            if key == pygame.K_DOWN:
                self.keys[0] = event.up
            elif key == pygame.K_UP:
                self.keys[1] = event.up
            elif key == pygame.K_LEFT:
                self.keys[2] = event.up
            elif key == pygame.K_RIGHT:
                self.keys[3] = event.up
            elif key == pygame.K_SPACE and event.up:
                pass
            elif key == pygame.K_SPACE:
                self.keys[4]=event.up
