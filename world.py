from pygame.sprite import Group
from level import Level
import json
import player, enemy
from inspect import getargspec

from pygame.sprite import Sprite


ACTORS = {
    "Player": player.Player,
    "Enemy": enemy.Enemy
}

class World(object):

    level = None
    actors = None
    levelImage = ""
    background = None
    
    def __init__(self, game, eventMgr):
        self.game = game
        self.em = eventMgr
        self.actors = [ ]
        self.level = Level()

    def loadLevel(self, filename):
        self.loadConfFile(filename)
        self.level.load()
        
    def update(self, dt):
        #self.actors.update(dt)

        # draw...
        #self.game.screen.blit(self.background, (0,0))
        self.level.draw(self.game.screen, self.game.viewport.topleft)

        for actor in self.actors:
            actor.draw(self.game.screen, self.game.viewport)
        

    def setCameraPos(x,y):
        self.game.rect.topleft = (x,y)   
        
    def setCameraPos(x,y):
        self.game.rect.center = (x,y)
        
    def loadConfFile(self, filename):
        # ladataan json tiedosto
        try:
            f = file(filename, "r")
            data = json.load(f)
            f.close()
        except IOError:
            print "Failed to open file", filename
            return
        except ValueError as e:
            print "Failed to parse json-file:", e
            return
        
        # perustiedot
        self.name = data["Name"]
        self.width = data["Width"]
        self.height = data["Height"]
        self.level.levelImageFile = data["LevelImage"]
        
        print "Name:", data["Name"]
        print "Size:", data["Width"], "x", data["Height"]

        for actor in data["Actors"]:
            
            if actor["class"] not in ACTORS:
                print "Actor class '"+actor["class"]+"' doesn't exist!"
                continue

            # lisataan actor-tauluun lisaa arvoja joita voidaan tarjota actorin alustuksessa
            actor["pos"] = pos = (actor["x"], actor["y"])
            actor["eventMgr"] = self.em

            # karsitaan params listaan vain ne parametrit jotka tarvitaan
            actorClass = ACTORS[actor["class"]]
            initargs = getargspec(actorClass.__init__)[0]  # actorClass.__init__.func_code.co_varnames
            params = dict([(key, actor[key]) for key in actor.keys() if key in initargs])
            instance = None
            try:
                # luodaan uusi actor
                instance = actorClass(**params)
            except TypeError as e:
                print "Failed to construct a new actor '"+actor["class"]+"' with params:", params
                print e.message 
            
            # tallennetaan actor    
            instance.rect.center = pos
            self.actors.append( instance )
            
        

        
if __name__ == "__main__":
    import events
    w = World(None, events.EventManager())
    w.loadConfFile("levels/mappi.txt")
