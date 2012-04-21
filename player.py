from character import Character

import pygame

from world import B2SCALE

class Player(Character):

    def __init__(self, b2World, eventMgr, pos):
        Character.__init__(self)
        
        self.em = eventMgr
        eventMgr.register(self)
        
        self.keys = [False] * 5
        self.animation_frames = map(pygame.image.load, ["media/nja2_lf1.png", "media/nja2_lf2.png", "media/nja2_rt1.png", "media/nja2_rt2.png", "media/nja2_fr1.png"])
        self.frame_count = 2
        self.image = self.animation_frames[0]
        self.animation_step = 0
        self.frame_interval = 10
        self.frame = 0
        self.going_left = False
        self.going_right = False
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.width = 32
        self.rect.height = 32
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
                self.body.ApplyLinearImpulse(impulse=(0, -200 * B2SCALE), point=(0,0))
                self.jumped = True
        else:
            self.jumped = False
        
        self.going_left = self.body.linearVelocity[0] < -0.1
        self.going_right = self.body.linearVelocity[0] > 0.1
        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation_step += dt
        self.frame = (self.animation_step / self.frame_interval) % self.frame_count
        if self.going_left:
            self.image = self.animation_frames[self.frame]
        elif self.going_right:
            self.image = self.animation_frames[self.frame + self.frame_count]
        else:
            self.image = self.animation_frames[-1]

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
