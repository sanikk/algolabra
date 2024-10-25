import unittest
from decimal import Decimal

from algolabra.astar.astar import astar
from algolabra.fileIO.read_files import read_map

class TestChildren(unittest.TestCase):
    def setUp(self):
        self.dummy_open = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.dummy_alley = [[".", ".", "."], [".", "#", "."], [".", "#", "."]]
        self.city_map = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')


    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = astar(start, goal, self.city_map, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)
        self.assertEqual(ret[2], False)
        self.assertEqual(ret[3], False)


    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = astar(start, goal, self.city_map, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertLess(ret[0], 17.4852814)
        self.assertGreater(ret[0], 17.4852813)
        self.assertEqual(ret[2], False)
        self.assertEqual(ret[3], False)
