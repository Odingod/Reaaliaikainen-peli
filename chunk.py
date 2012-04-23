import player, enemy, pickup_orb
#from pygame.rect import Rect
from pygame import *

from block import *
from platform import *
from inspect import getargspec
import random
import sys
OBJECTS = {
    "Enemy": enemy.Enemy,
    "Block": Block,
    "Platform": Platform,
    "Pickup": pickup_orb.PickupOrb
}

class Chunk(object):

    em = None
    def __init__(self, world, pos, width, height, objects, eventMgr):
        self.rect = Rect(pos[0], pos[1], width, height)
        self.em = eventMgr
        self.world = world
        self.objects = objects
        self.background = pygame.image.load("media/background.jpg").convert()

        
    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def draw(self, screen, viewport):
        
        for obj in self.objects:
            obj.draw(screen, viewport)
        #pygame.draw.rect(screen, pygame.color.Color('red'), (self.rect.left - viewport.left, \
        #    self.rect.top - viewport.top, \
        #    self.rect.width, self.rect.height), 2)

    def getNext(self):
        if len(self.next.keys()) == 1:
            nextone = self.next.keys()[0]
        return nextone
        
    def _buildObjects(self, objects):
        for obj in objects:
            if obj["class"] not in OBJECTS:
                print "Object class '"+obj["class"]+"' doesn't exist!"
                continue

            # lisataan objects-tauluun lisaa arvoja joita voidaan tarjota objektin alustuksessa
            obj["pos"] = (self.rect.left + obj["x"], self.rect.top + obj["y"])
            obj["eventMgr"] = self.em
            obj["world"] = self.world
            obj["b2World"] = self.world.b2World

            # karsitaan params listaan vain ne parametrit jotka tarvitaan
            objClass = OBJECTS[obj["class"]]
            initargs = getargspec(objClass.__init__)[0]  # objClass.__init__.func_code.co_varnames
            params = dict([(key, obj[key]) for key in obj.keys() if key in initargs])
            instance = None
            try:
                # luodaan uusi objecti
                instance = objClass(**params)
            except TypeError as e:
                print "Failed to construct a new object '"+obj["class"]+"' with params:", params
                raise
            
            # tallennetaan objekti   
            self.objects.append( instance )
            
