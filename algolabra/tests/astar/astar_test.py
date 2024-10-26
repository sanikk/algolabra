import unittest
from decimal import Decimal

from algolabra.astar.astar import astar
from algolabra.fileIO.read_files import read_map

class TestAstar(unittest.TestCase):
    def setUp(self):
        self.city_map = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')

    def test_open_minimap(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        ret = astar((0,0), (2,2), m, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], Decimal(2) * self.diag_cost)

    def test_alley_minimap(self):
        m = [[".", ".", "."], [".", "#", "."], [".", "#", "."]]
        ret = astar((0, 0), (2, 2), m, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 4)


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

    def test_medium_path_with_citymap_one(self):
        # 35	Boston_0_512.map	512	512	47	482	25	352	142.42640686
        start = 47, 482
        goal = 25, 352
        self.basic_case(start, goal, Decimal('142.4264068711928514640'))

    def test_bad_case_one(self):
        # 30    Boston_0_512.map        512     512     498     442     395     488     122.05382385
        self.basic_case((498, 442),(395, 488), 122.05382385)
        pass

    def basic_case(self, start, goal, result):
        ret = astar(start, goal, self.city_map, self.diag_cost)
        self.assertEqual(len(ret), 4)

        self.assertEqual(ret[2], False)
        self.assertEqual(ret[3], False)

        self.assertEqual(ret[0], result)

