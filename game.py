from world import World
from events import *
from operator import itemgetter, attrgetter
from soundmanager import SoundManager
WIDTH = 800
HEIGHT = 600

import pygame

class Game(object):

    def __init__(self, eventMgr):
        self.em = eventMgr
        self.em.register(self)
        pygame.init()
        
        self.screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
        self.view = pygame.Surface( (WIDTH,HEIGHT) )
        self.viewport = self.view.get_rect()
        pygame.display.set_caption("Game")

        self.sm = SoundManager("media/skeptic.mp3")        

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
            #if dt != 0:
            #    print "FPS:",1000/dt
            
            speed = 0 if self.world.player.has_pickup("no_hurry") else 2
            self.viewport.center = ( 400, min(self.viewport.centery - speed * dt, self.world.player.rect.top))
            
            if self.viewport.center[1] < self.world.player.rect.top + self.world.player.rect.height - self.world.player.trampoline_height and self.world.player.has_pickup("trampoline"):
              self.world.player.jump()
            elif self.viewport.center[1] < self.world.player.rect.top - 300:
                self.em.tell(PointEvent(int(self.world.player.score+abs(self.world.player.max_height*0.1))))
            
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
            self.sm.update(dt)

            font = pygame.font.Font(None, 25)
            text = font.render("Score: "+str(int(self.world.player.score+abs(self.world.player.max_height*0.1))), True, (255,255,255))
            self.screen.blit(text, (70, 0))

            pygame.display.flip()

        elif event.name == 'Destroy':
            pygame.quit()
            return True
        if event.name == 'Point':
            self.sm.fadeout(3000)

            done = False
            scores = []
            name = ""
            get_name = False
            try:
                    f = open("scores", "r")
                    for line in f:
                        x = line.strip().split(',')
                        scores.append((x[0],int(x[1])))
                    f.close()
            except IOError:
                    pass
            scores.sort(key=itemgetter(1), reverse=True)
            if (len(scores) < 10) or (int(scores[9][1]) < int(event.points)):
                get_name = True
            while not done:
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        done = True
                    if events.type == pygame.KEYDOWN:
                        if events.key == pygame.K_ESCAPE:
                            done=True
                        if get_name and 126 > events.key > 64:
                            name += chr(events.key)
                        if get_name and events.key == 32:
                            name += " "
                        if get_name and events.key == 8:
                            name = name[0:-1]
                        if get_name and events.key == 13:
                            get_name = False
                            try:
                                f = open("scores", "a")
                                f.write(name+","+str(event.points)+"\n")
                                f.close()
                            except IOError:
                                pass
                            scores.append((name, event.points))
                            scores.sort(key=itemgetter(1), reverse=True)
                pygame.time.wait(1)
                self.screen.fill((0,0,0))

                if get_name:
                    font = pygame.font.Font(None, 50)
                    font2 = pygame.font.Font(None, 100)
                    text = font.render(name, True, (255,255,255))
                    text2 = font2.render("Game over", True, (255,255,255))
                    text3 = font.render("Please enter your name:", True, (255,255,255))
                    self.screen.blit(text, (20,300))
                    self.screen.blit(text3, (20,150))
                    self.screen.blit(text2, (20,20))

                else:
                    
                    font = pygame.font.Font(None, 100)
                    font2 = pygame.font.Font(None, 50)
                    text = font.render("High scores", True, (255,255,255))
                    self.screen.blit(text, (20,20))
                    for i in range(len(scores)):
                        if i >= 10:
                            break
                        text2 = font2.render(str(i+1)+". " +scores[i][0][0:20], True, (255,255,255))
                        text3 = font2.render(str(scores[i][1]), True, (255,255,255))
                        self.screen.blit(text2, (20, 100+50*i))
                        self.screen.blit(text3, (600, 100+50*i))


                pygame.display.flip()

            self.em.tell('Quit')

if __name__ == "__main__":
    import main
    main.main()
