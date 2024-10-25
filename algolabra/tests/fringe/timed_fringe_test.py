import unittest
from decimal import Decimal

from algolabra.fringe.timed_fringe import fringe_search
from algolabra.fileIO.read_files import read_map
from algolabra.common_search_utils.check_solution import handle_path

# fringe_search(
#   start: tuple[int, int],
#   goal: tuple[int, int],
#   citymap: list,
#   diag_cost
#   )
#
# return found_cost, route, rounded, inexact

class TestBasicFringe(unittest.TestCase):
    def setUp(self):
        self.citymap = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)

    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertLess(ret[0], 17.485282)
        self.assertGreater(ret[0], 17.485281)

    def test_longer_path_with_citymap(self):
        # 30	Boston_0_512.map	512	512	498	442	395	488	122.05382385
        start = 498, 442
        goal = 395, 488
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)

        # shortest path is made of d diagonal and s straigth steps so exact cost should be
        # d * diag_cost + straight


        steps, straight, diagonal = handle_path(ret[1])
        correct_answer = diagonal * self.diag_cost + straight

        self.assertEqual(ret[0], correct_answer)

        # This returns Inexact = True, Rounded = True values
        # but the costs are correct. So seems to be test context related.

        self.assertLess(ret[0], 122.05382387)
        self.assertGreater(ret[0], 122.05382385)
