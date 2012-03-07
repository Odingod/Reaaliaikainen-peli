
from world import World

WIDTH = 800
HEIGHT = 600

import pygame

class Game(object):

    def __init__(self, eventMgr):
        self.em = eventMgr
        self.em.register(self)
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Game")
        
        try:
            self.world = World(self, eventMgr)
            self.world.loadLevel("levels/mappi.txt")
        except:
            pass
 
        self.em.tell("GameStart")
        

    def notify(self,event):
        if event.name == 'Tick':
            self.screen.fill((0,0,0))
             
            dt = event.time # deltatime

            # all the drawing stuff...
            self.world.update(dt)

            
            pygame.display.flip()

        elif event.name == 'Destroy':
            pygame.quit()
            return True




if __name__ == "__main__":
    import main
    main.main()
