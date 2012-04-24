from character import Character
from settings import Settings

import pygame
from world import B2SCALE

HEIGHT = 600
WIDTH =  800

from pickup import PICKUP_NAMES, Pickup
class Player(Character):

    def __init__(self, b2World, eventMgr, pos):
        Character.__init__(self)
        
        self.em = eventMgr
        eventMgr.register(self)
        
        self.keys = [False] * 5
        self.pickups = []
        self.pickups.append(Pickup("no_hurry", 200))
        
        self.animation_frames = map(pygame.image.load, ["media/nja2_lf1.png", "media/nja2_lf2.png", "media/nja2_rt1.png", "media/nja2_rt2.png", "media/nja2_fr1.png"])
        self.frame_count = 2
        self.image = self.animation_frames[0]
        self.animation_step = 0
        self.frame_interval = 10
        self.frame = 0
        self.font = pygame.font.Font(None, 20)
        
        self.going_left = False
        self.going_right = False
        self.upsidedown = False
        self.midair = True        
        self.can_double_jump = True
        self.time_since_jump = 0
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.width = 32
        self.rect.height = 32

        self.xspeed = 400
        self.jumping_power = 200
        self.default_jumping_power = 200

        self.score = 0.0
        self.max_height = 0
        self.trampoline_height = 250

        self.createBody(b2World, self.rect.width, self.rect.height )

        
    def canJump(self):
        if abs(self.body.linearVelocity[1] ) > 0.1:
            return False
        for contact_edge in self.body.contacts:
            c = contact_edge.contact
            if c.manifold.localNormal[1] < -0.9:
                return True
        return False
    
    
    def jump(self):
        self.jumping_power = 300 if self.has_pickup("jumping_power") else 200
        self.body.ApplyLinearImpulse(impulse=(0, -self.jumping_power * Settings.B2SCALE), point=(0,0))
        

    def update(self, dt):
        Character.update(self, dt)
        self.midair = abs(self.body.linearVelocity[1]) > 0.01
        self.time_since_jump += dt
        if self.keys[2]:
            self.body.linearVelocity = (-self.xspeed * Settings.B2SCALE, self.body.linearVelocity[1] )
        if self.keys[3]:
            self.body.linearVelocity = (self.xspeed * Settings.B2SCALE, self.body.linearVelocity[1] )
        if self.keys[1]:
            if not self.midair:
                self.jump()
                self.can_double_jump = True
                self.time_since_jump = 0
            elif self.can_double_jump and self.has_pickup("double_jump") and self.time_since_jump > 10:
                self.jump()
                self.can_double_jump = False

        self.upsidedown = False        
        for contact_edge in self.body.contacts:
            if contact_edge.contact.touching:
                if contact_edge.other.position[1] - self.body.position[1] < 0:
                    self.upsidedown = True
            
        self.going_left = self.body.linearVelocity[0] < -0.1
        self.going_right = self.body.linearVelocity[0] > 0.1

        self.update_animation(dt)
        self.update_pickups(dt)

        self.score += 0.01*(2**self.pickup_count("double_points"))
        if self.rect.top < self.max_height:
            self.max_height = self.rect.top

    def update_animation(self, dt):
        self.animation_step += dt
        self.frame = (self.animation_step / self.frame_interval) % self.frame_count
        if self.going_left:
            self.image = self.animation_frames[self.frame]
        elif self.going_right:
            self.image = self.animation_frames[self.frame + self.frame_count]
        else:
            self.image = self.animation_frames[-1]

    def draw(self,screen,viewport):
        if self.has_pickup("trampoline"):
            pygame.draw.line(screen, (0,255,255), (0, HEIGHT/2 + self.trampoline_height),(WIDTH, HEIGHT/2 + self.trampoline_height))
        Character.draw(self, screen, viewport)
        h = 0
        for pickup in self.pickups:
            text = PICKUP_NAMES[pickup.pickup_type] + " " + str(pickup.duration)
            text_render = self.font.render(text, True, (255, 255, 255))
            screen.blit(text_render, (600, h))
            h += 20

    def update_pickups(self, dt):
        for pickup in self.pickups:
            pickup.update(dt)
        i = 0
        while i < len(self.pickups):
            if not self.pickups[i].alive():
                self.pickups.pop(i)
            else:
                i += 1

    def has_pickup(self, pickup_type):
        return pickup_type in [pickup.pickup_type for pickup in self.pickups]
    def pickup_count(self, pickup_type):
        return reduce(lambda y,x: y + 1 if x == pickup_type else y,[pickup.pickup_type for pickup in self.pickups], 0)
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
        elif event.name == 'Pickup':
            self.pickups.append(event.pickup)
            self.score += 10*(2**self.pickup_count("double_points"))
