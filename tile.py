
TILESIZE = 32

class Tile():

    F_VISIBLE = 0
    F_SOLID = 1
    F_FIRE = 2
    F_AWESOME = 3
    
    def __init__(self, image, *flags):
        self.image = image
        self.flags = list(flags)
