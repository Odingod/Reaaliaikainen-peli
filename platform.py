
from actor import *
from pygame.rect import Rect

#from imagecont import *

import pygame
import Box2D


class Platform(Actor):

    image = None
    def __init__(self, image, x, y, dstx, dsty, speed, width, height ):
        self.rect = Rect(x, y, width, height)
        self.image = pygame.image.load("media/Character.png")
        
        self.speed = speed
        self.dst = (dstx, dsty)
        #self.image = ImageContainer.getImage(name)
        
    def update(self, dt):
        # update pos
        pass
        