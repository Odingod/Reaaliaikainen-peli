
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
        self.view = pygame.Surface( (WIDTH,HEIGHT) )
        self.viewport = self.view.get_rect()
        pygame.display.set_caption("Game")
        
        try:
            self.world = World(self, eventMgr)
            self.world.loadLevel("levels/mappi.txt")
        except:
            pygame.quit()
            raise # continue catched exception
            
        
        self.em.tell("GameStart")
        

    def notify(self,event):
        if event.name == 'Tick':
            self.screen.fill((0,0,0))
            self.view.fill((0,0,0))
            dt = event.time # deltatime
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.viewport.top -= 4
            elif keys[pygame.K_s]:
                self.viewport.top += 4
            if keys[pygame.K_d]:
                self.viewport.left += 4
            elif keys[pygame.K_a]:
                self.viewport.left -= 4
            
            #self.screen.blit(self.view, pygame.Rect(0,0,800,600))
            #self.viewport
            # all the drawing stuff...
            self.world.update(dt)

            pygame.display.flip()

        elif event.name == 'Destroy':
            pygame.quit()
            return True




if __name__ == "__main__":
    import main
    main.main()
