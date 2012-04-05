import player, enemy
from pygame.rect import Rect

from block import *
from platform import *
from inspect import getargspec

OBJECTS = {
    "Enemy": enemy.Enemy,
    "Block": Block,
    "Platform": Platform
}

class Chunk(object):

    next = { }
    objects = [ ]
    em = None
    def __init__(self, world, pos, data):
        self.rect = Rect(pos[0], pos[1], data["Height"], 800)
        self.world = world
        self.next = data["Next"]
        self._buildObjects(data["Objects"])
        
        
    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def draw(self, screen, viewport):
        for obj in self.objects:
            obj.draw(screen, viewport)
    
    def getNext(r):
        return None
        
    def _buildObjects(self, objects):
        for obj in objects:
            if obj["class"] not in OBJECTS:
                print "Object class '"+obj["class"]+"' doesn't exist!"
                continue

            # lisataan objects-tauluun lisaa arvoja joita voidaan tarjota objektin alustuksessa
            obj["pos"] = pos = (self.rect.left - obj["x"], self.rect.top - obj["y"])
            obj["eventMgr"] = self.em
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
            
