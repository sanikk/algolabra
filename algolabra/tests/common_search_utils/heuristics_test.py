import unittest
from decimal import Decimal
from algolabra.common_search_utils.heuristics import heuristics


class HeuristicsTest(unittest.TestCase):

    def setUp(self):
        self.diag_cost = Decimal('1.4142135623730950488')
        self.diff = self.diag_cost - Decimal(2)

    def test_heuristics_gives_right_cost_to_one_move(self):
        self.assertEqual(heuristics(1, 1, 0, 1, self.diff), 1)
        self.assertEqual(heuristics(1, 1, 2, 1, self.diff), 1)
        self.assertEqual(heuristics(1, 1, 1, 0, self.diff), 1)
        self.assertEqual(heuristics(1, 1, 1, 2, self.diff), 1)

        self.assertEqual(heuristics(1, 1, 0, 2, self.diff), self.diag_cost)
        self.assertEqual(heuristics(1, 1, 2, 2, self.diff), self.diag_cost)
        self.assertEqual(heuristics(1, 1, 2, 0, self.diff), self.diag_cost)
        self.assertEqual(heuristics(1, 1, 0, 0, self.diff), self.diag_cost)

    def test_heuristics_with_multiples_of_7(self):
        diff = self.diff
        diag_cost = self.diag_cost
        self.assertEqual(heuristics(14, 13, 7, 13, diff), 7)
        self.assertEqual(heuristics(23,11, 16, 4, diff), Decimal(7) * diag_cost)
        self.assertEqual(heuristics(53166, 215123, 53159, 215123, diff), 7)
        self.assertEqual(heuristics(354, 214, 347, 221, diff), Decimal(7) * diag_cost)

    def test_heuristics_uses_octile_not_euclidean(self):
        self.assertEqual(heuristics(600,600, 900, 800, self.diff), Decimal(200) * self.diag_cost + Decimal(100) )
        pass


