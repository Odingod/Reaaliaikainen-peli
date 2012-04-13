
from game import Game
from events import *

import pygame

class Keyboard:
    def __init__(self, eventmanager):
        self.em = eventmanager
        self.em.register(self)
    
    
    def notify(self,event):
        if event.name == 'Tick':
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.em.tell('Quit')
                elif e.type == pygame.KEYDOWN:
                    self.em.tell(KeyboardEvent(e.key,True))
                elif e.type == pygame.KEYUP:
                    self.em.tell(KeyboardEvent(e.key,False))
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.em.tell(MouseEvent(e.button,True))
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.em.tell(MouseEvent(e.button,False))


class Mainloop:
    def __init__(self, eventMgr):
        self.em = eventMgr
        
        self.clock = pygame.time.Clock()
        self.em.register(self)

        self.running = True
    
    def run(self):
        try:
            self.running = True
            while self.running: 
                scale = self.clock.tick(60) * 60 / 1000
                self.em.tell(TickEvent(scale))
        finally:
            self.em.tell('Destroy')
            
    def notify(self,event):
        if event.name == 'Quit':
            self.running = False
            return True
        elif event.name == 'Tick':
             pass

def main():
    em = EventManager()
    gw = Game(em)
    kb = Keyboard(em)
    ml = Mainloop(em)
    ml.run()

if __name__ == "__main__":
    main()
    
