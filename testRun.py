import unittest    #    .- -...-- +     .         . .       +     ...     .. . - .-.        ..        -     .         ... .        .     .
import os          #     -m  .  m.    .  ..         -     -       .     .   .   .-m           m.     .     .. .       .  -. .             .-
import pygame      #   ..             . -.        -.m   . -%      m.  . - .+ + .    .       . - -   %.     ..-. -     %.-- .   ....
from main import    * #---     .   . . .-  ..  ......-..   . - .  ..  ....-            . ___._._.  ..+       m  .  .  +.-.     . .. . ..  m-.
from    game import    * #\----         -.. .. -- m -.    .-. .  .  .  + -        .     /    .-  \  . .. +%-+  .  --. .++-.  .. m--.    . .
from       tile import    *   #\---        .   .  -. -.   - --.   ..-..     ..         --| \  ...  \    .. ++..  -.m..  -m-.-.....-. -.--..
from          block import    *   #\---- m ... ..  *- .  - ..m - m+ - .+..-  ..     --/  |  \  ...  \     . - .. -m-..  . . .-   ..  m .-.
from              chunk import    *    #\+--  +  .   .. . m .+++####+*.  -.- .-  --/ /+--X--+  ..... \     .       m+ . ..# . -.*. .-..  ..
from                  world import    *     #\----     . .  +%########m .  - -%-++-----/ |  /  ....  |    ...    . . - -...  . .--  m .. .  .
from                      actor import    *      #\----    .+%##########--+--+/+-\   |-\ | / --------|   .  -   . .. *   . .   ..--+- .- ..
from                           enemy import     *     #\--- .##########+-/-/       --+-----  . .. .. |   ....+-     --. .    ..  -*  +...
from                               events import    *    # \+#########%-    .        \  ... ........ /   ..+--------------------------------------+
from                                     player import    * ##%######+-    . .        \ ........... /   ..-|                                      |
from                                     pickup import    *  #+*+##+.+  .  .. .   ..  .\ ......... /     .-|______  _______ _______ _______ _     _
from                               tileset import    *   #  .   .       . . .         . -----------  .     ||     \ |______ |_____|    |    |_____|
from                        platform import    *   #--          -     .-  .   ....-  .      .         ..   ||_____/ |______ |     |    |    |     |
from                character import    *   #------/ .   .  .. .       . .  .  -. --m          .    -      |                                -     -
from       pickup_orb  import    *   #-------+--    .+   -.+. .m.       .-..%..  .-m-  .     -.+   . %     | _______ _______ _______  ______      |
from  events import       * #---------+/-          -..  .  .    ..     .+.-m  .   .  . .     +..    .. ..  | |______    |    |_____| |_____/      |
                    #                .   .               . .   ..       -.  . .  . .       .               |  ______|   |    |     | |    \_      |
#+-----------+      #                    ..        .-m- % .- +  .. + .  --m-  . .. -  + ... ..... . . +....|                                      |
#+------+           #                 .+.              +-   .    -+ .     .       .% .  .  .       . ..+  -+--------------------------------------+
#----------+        #                  . -.          .  . .   .-.-..    -        .              .      . . ..*...    .           . .
#                                      .            .                                                  .    .   .                   .
#testin tehnyt Miki Tolonen 222480    .
class TestPickup(unittest.TestCase):
	def setUp(self):
                self.pickup = Pickup(PICKUP_NAMES["double_jump"],500)

	def test_init(self):
		self.assertEqual(self.pickup.pickup_type,PICKUP_NAMES["double_jump"])
		self.assertEqual(self.pickup.duration,500)

	def test_update(self):
		self.pickup.update(250)
		self.assertEqual(self.pickup.duration,250)

	def test_dead(self):
	    self.assertTrue(self.pickup.alive())
	    self.pickup.update(500)
	    self.assertEqual(self.pickup.duration,0)
	    self.assertFalse(self.pickup.alive())

	def tearDown(self):
		pass

# Testin tehnyt William 'dnyarri' Linna 293639
class TestTileset(unittest.TestCase):
    def setUp(self):

        self.tilesetPath = os.path.join("media", "Tiles.png")
        self.testImage = pygame.image.load(self.tilesetPath)
        self.testWidth, self.testHeight = self.testImage.get_size()
        self.testWidth //= TILESIZE
        self.testHeight //= TILESIZE


    def test_load(self):
        tileset = Tileset()
        tileset.load(self.tilesetPath)
        # print "\nWidth should be:", tileset.width, ", It is:", self.testWidth
        # print "Height should be:", tileset.height, ", It is:", self.testHeight
        # self.assertEqual(tileset.image, self.testImage)
        self.assertEqual(tileset.width, self.testWidth)
        self.assertEqual(tileset.height, self.testHeight)


    def test_getTile(self):
        tileset = Tileset()
        tileset.load(self.tilesetPath)
        i = 1
        x = i % self.testWidth
        y = i // self.testWidth
        testTileTest = self.testImage.subsurface(pygame.Rect(TILESIZE * x, TILESIZE * y , TILESIZE * 1, TILESIZE * 1))
        testTileGame = tileset.getTile(i)

        # self.assertEqual(testTileGame, testTileTest)
        # Kuvien vertailu keskenaan on aika vaikeaa...

#testin tehnyt erika salmivaara
class TestPlayer(unittest.TestCase):

	def setUp(self):
                self.player = Player(Box2D.b2World( gravity=(0,40), doSleep=True), EventManager(), (0, 0))
                self.pickup = Pickup(PICKUP_NAMES["trampoline"],100)
                self.event = PickupEvent(self.pickup)

	def testNotify(self):
		self.assertEqual(len(self.player.pickups), 1)
		self.player.notify(self.event)
		self.assertEqual(self.player.pickups[1], self.pickup)
		self.assertEqual(self.player.score, 10)



#testin tehnyt Otto Tuominen 298647
class TestWorld(unittest.TestCase):

        def setUp(self):
                self.em = EventManager()
                self.game = Game(self.em)
                self.world = World(self.game, self.em)

        def testSetCameraPos(self):
                x = 5
                y = 6
                self.world.setCameraPos(x, y)
                self.assertEqual(x, self.game.viewport.topleft[0])
                self.assertEqual(y, self.game.viewport.topleft[1])

        def testSetCameraCenter(self):
                x = 10
                y = 15
                self.world.setCameraCenter(x, y)
                self.assertEqual(x, self.game.viewport.center[0])
                self.assertEqual(y, self.game.viewport.center[1])

if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPickup)
        unittest.TextTestRunner(verbosity=2).run(suite)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestTileset)
        unittest.TextTestRunner(verbosity=2).run(suite)
    	suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
     	unittest.TextTestRunner(verbosity=2).run(suite)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestWorld)
     	unittest.TextTestRunner(verbosity=2).run(suite)
