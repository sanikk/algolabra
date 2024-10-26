import unittest
from decimal import Decimal
# from algolabra.fringe.fringe_search import heuristics
from algolabra.common_search_utils.heuristics import heuristics_with_node


class HeuristicsTest(unittest.TestCase):

    def setUp(self):
        self.diag_cost = Decimal('1.4142135623730950488')

    def test_heuristics_gives_right_cost_to_one_move(self):
        node = Node(x=1, y=1)
        diff = self.diag_cost - Decimal(1)
        self.assertEqual(heuristics_with_node(node, 0, 1, diff, self.diag_cost), 1)
        self.assertEqual(heuristics_with_node(node, 2, 1, diff, self.diag_cost), 1)
        self.assertEqual(heuristics_with_node(node, 1, 0, diff, self.diag_cost), 1)
        self.assertEqual(heuristics_with_node(node, 1, 2, diff, self.diag_cost), 1)

        self.assertEqual(heuristics_with_node(node, 0, 2, diff, self.diag_cost), self.diag_cost)
        self.assertEqual(heuristics_with_node(node, 2, 2, diff, self.diag_cost), self.diag_cost)
        self.assertEqual(heuristics_with_node(node, 2, 0, diff, self.diag_cost), self.diag_cost)
        self.assertEqual(heuristics_with_node(node, 0, 0, diff, self.diag_cost), self.diag_cost)


class Node:
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y
        self.prev = prev
        self.next = next
