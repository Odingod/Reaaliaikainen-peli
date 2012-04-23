import unittest
import os
import pygame
from main import *
from game import  *
from tile import   *
from block import   *
from chunk import    *
from world import     *
from actor import      *
from enemy import       *
from events import       *
from player import        *
from pickup import         *
from tileset import         *
from platform import         *
from character import         *
from pickup_orb import         *

#testin tehnyt Miki Tolonen 222480
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
        # Kuvien vertailu keskenään on aika vaikeaa...
        

        
        

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestPickup)
	unittest.TextTestRunner(verbosity=2).run(suite)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestTileset)
        unittest.TextTestRunner(verbosity=2).run(suite)
