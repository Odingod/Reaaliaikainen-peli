import unittest
from main import *
from game import *
from tile import *
from block import *
from chunk import *
from world import *
from actor import *
from enemy import *
from events import *
from player import *
from pickup import *
from tileset import *
from platform import *
from character import *
from pickup_orb import *

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


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestPickup)
	unittest.TextTestRunner(verbosity=2).run(suite)
