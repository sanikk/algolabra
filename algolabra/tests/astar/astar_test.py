import unittest
from decimal import Decimal

from algolabra.astar.astar import astar
# from algolabra.common_search_utils.children import children
from algolabra.fileIO.read_files import read_map

class TestChildren(unittest.TestCase):
    def setUp(self):
        self.dummy_open = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.dummy_alley = [[".", ".", "."], [".", "#", "."], [".", "#", "."]]
        self.city_map = read_map("algolabra/bostonmaps/Boston_0_512.map")

    # def test_one_step_path_

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = astar(start, goal, self.city_map)
        self.assertEqual(len(ret), 2)
        self.assertEqual(ret[0], 1)
        pass

    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = astar(start, goal, self.city_map)
        self.assertEqual(len(ret), 2)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertEqual(str(ret[0]), '17.48528137423857029281013233')
