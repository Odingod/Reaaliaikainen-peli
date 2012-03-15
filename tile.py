from pygame.sprite import Sprite

TILESIZE = 16


class Tile(Sprite):

    F_VISIBLE = 0
    F_SOLID = 1
    F_FIRE = 2
    F_AWESOME = 3
    
    def __init__(self, image, *flags):
        Sprite.__init__(self)
        self.image = image
        self.flags = list(flags)
        