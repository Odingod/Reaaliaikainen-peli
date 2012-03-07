from character import Character
from pygame.rect import Rect

class Player(Character):

    def __init__(self, eventMgr, name="default"):
        Character.__init__(self)
        print "Init Player! name:", name
        self.em = eventMgr
        eventMgr.register(self)
        
        self.keys = [False] * 5
        #self.image, self.rect =load_image('ship.png',-1)
        self.image = None
        self.rect = Rect(0,0,0,0)
        
    def update(self, dt):
        pass
 
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
