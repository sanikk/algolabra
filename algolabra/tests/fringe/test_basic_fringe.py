import unittest
from decimal import Decimal

from algolabra.fringe.basic_fringe import fringe_search
from algolabra.fileIO.read_files import read_map

class TestBasicFringe(unittest.TestCase):
    def setUp(self):
        self.citymap = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')

    def test_simple_map_no_obstacles(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        ret = fringe_search((0,0), (2,2), m, self.diag_cost)

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)
        pass

    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertLess(ret[0], 17.485282)
        self.assertGreater(ret[0], 17.485281)