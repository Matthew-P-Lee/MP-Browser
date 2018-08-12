import unittest
import warnings
from MPAPI_classes import *

class TestMPAPI(unittest.TestCase):
	
	def setUp(self):
		warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>") 
	
	def test_GetUser(self):
		profile = MPAPI().get_profile(112244155)
		print(profile)
		self.assertTrue(profile)

	def test_GetRoute(self):
		route = MPAPI().get_route(105721759)
		print(route)
		self.assertTrue(route)

	def test_GetTicks(self):
		ticks = MPAPI().get_ticks(112244155)
		print(ticks)
		self.assertTrue(ticks)



if __name__ == '__main__':
    unittest.main()
