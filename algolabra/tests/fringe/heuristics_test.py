import unittest
from math import sqrt

from algolabra.fringe.doublelinkedlist import Node
from algolabra.fringe.fringe_search import heuristics


class HeuristicsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_heuristics_gives_right_cost_to_one_move(self):
        node = Node(x=1, y=1)

        self.assertEqual(heuristics(node, 0,1), 1)
        self.assertEqual(heuristics(node, 2, 1), 1)
        self.assertEqual(heuristics(node, 1, 0), 1)
        self.assertEqual(heuristics(node, 1, 2), 1)

        diag_cost = sqrt(2)

        self.assertEqual(heuristics(node, 0,2), diag_cost)
        self.assertEqual(heuristics(node, 2, 2), diag_cost)
        self.assertEqual(heuristics(node, 2, 0), diag_cost)
        self.assertEqual(heuristics(node, 0, 0), diag_cost)
