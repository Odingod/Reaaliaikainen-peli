import pygame.mixer as mixer
class SoundManager:
    def __init__(self, filename):
        mixer.music.load(filename)
    def play(self):
        mixer.music.play()
    def fadeout(self, time):
        mixer.music.fadeout(time)
    def alive(self):
        return mixer.music.get_busy()
    def update(self, dt):
        if not self.alive():
            self.play()

