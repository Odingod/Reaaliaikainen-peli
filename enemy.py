
from character import Character
import pygame

class Enemy(Character):

    def __init__(self):
        Character.__init__(self)
        self.image = pygame.image.load("media/character.png")
        self.rect = self.image.get_rect()

    def update(self, dt):
        pass

    def runAI(self):
        pass
