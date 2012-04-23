from settings import Settings
from world import World
import pygame

class Game(object):

    def __init__(self, eventMgr):
        self.em = eventMgr
        self.em.register(self)
        pygame.init()
        self.game_over = False
        self.screen = pygame.display.set_mode( (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT) )
        self.view = pygame.Surface( (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT) )
        self.viewport = self.view.get_rect()
        pygame.display.set_caption("Game")
        
        try:
            self.world = World(self, eventMgr)
            self.world.loadLevel("levels/mappi.txt")
        except:
            pygame.quit()
            raise # continue catched exception
        
        self.em.tell("GameStart")


    def notify(self, event):
        if event.name == 'Tick':
            if not self.game_over:
                self.screen.fill((0,0,0))
                self.view.fill((0,0,0))
                dt = event.time # deltatime
                #if dt != 0:
                #    print "FPS:",1000/dt
                
                self.viewport.center = ( 400, self.viewport.centery - 1 * dt)
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.viewport.top -= 10
                elif keys[pygame.K_s]:
                    self.viewport.top += 10
                if keys[pygame.K_d]:
                    self.viewport.left += 4
                elif keys[pygame.K_a]:
                    self.viewport.left -= 4
                
                #self.viewport
                # all the drawing stuff...
                self.world.update(dt)
                
                # The player is considered dead if the players y-coordinate is bigger
                # than the y-coordinate of the bottom of the view            
                #if (self.world.player.rect.topleft[1] > self.viewport.bottomleft[1]):
                    #self.endGame()
            
            pygame.display.flip()

        elif event.name == 'Destroy':
            pygame.quit()
            return True


    def endGame(self):        
        menu = pygame.Surface((Settings.MENU_WIDTH, Settings.MENU_HEIGHT))
        menu.fill((0, 0, 255, 0))
        font = pygame.font.Font("media/FreeSansBold.ttf", 30)
        txt = font.render("Game over", 1, (255, 255, 255, 0))
        menu.blit(txt, ((Settings.MENU_WIDTH - txt.get_width())/2, (Settings.MENU_WIDTH - txt.get_height())/2))
        
        self.screen.blit( menu, ((Settings.SCREEN_WIDTH - Settings.MENU_WIDTH)/2, (Settings.SCREEN_HEIGHT-Settings.MENU_HEIGHT)/2) )
        self.game_over = True
        print "Game over!"

if __name__ == "__main__":
    import main
    main.main()
