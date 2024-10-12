import unittest
from decimal import Decimal
# from algolabra.fringe.fringe_search import heuristics
from algolabra.common_search_utils.heuristics import heuristics


class HeuristicsTest(unittest.TestCase):

    def setUp(self):
        self.diag_cost = Decimal('2').sqrt()

    def test_heuristics_gives_right_cost_to_one_move(self):
        node = Node(x=1, y=1)

        self.assertEqual(heuristics(node, 0,1, self.diag_cost), 1)
        self.assertEqual(heuristics(node, 2, 1, self.diag_cost), 1)
        self.assertEqual(heuristics(node, 1, 0, self.diag_cost), 1)
        self.assertEqual(heuristics(node, 1, 2, self.diag_cost), 1)

        diag_cost = Decimal(2).sqrt()

        self.assertEqual(heuristics(node, 0,2, diag_cost), diag_cost)
        self.assertEqual(heuristics(node, 2, 2, diag_cost), diag_cost)
        self.assertEqual(heuristics(node, 2, 0, diag_cost), diag_cost)
        self.assertEqual(heuristics(node, 0, 0, diag_cost), diag_cost)


class Node:
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y
        self.prev = prev
        self.next = next
