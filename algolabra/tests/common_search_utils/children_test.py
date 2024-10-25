import unittest
from decimal import Decimal

from algolabra.common_search_utils.children import children_with_node


class TestChildren(unittest.TestCase):
    def setUp(self):
        self.le_map1 = [["#", "#", "#"], ["#", ".", "."], [".", ".", "."]]
        self.le_map2 = [["#", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.empty_map = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.diag_cost = Decimal('2').sqrt()

    def test_children_returns_all_on_empty_map(self):
        result = children_with_node(Node(1, 1), self.empty_map, self.diag_cost)
        self.assertEqual(len(result), 8)
        self.assertEqual(result, [(1, 2, 1), (2, 2, self.diag_cost), (2, 1, 1), (2, 0, self.diag_cost),
                                  (1, 0, 1), (0, 0, self.diag_cost), (0, 1, 1), (0, 2, self.diag_cost)])
        result_coords = [(x, y) for x, y, z in result]
        self.assertTrue((1, 2) in result_coords)

        self.assertTrue((2, 2) in result_coords)
        self.assertTrue((2, 1) in result_coords)
        self.assertTrue((2, 0) in result_coords)
        self.assertTrue((1, 0) in result_coords)
        self.assertTrue((0, 0) in result_coords)
        self.assertTrue((0, 1) in result_coords)
        self.assertTrue((0, 2) in result_coords)


    def test_children_returns_the_right_7_on_one_blocked_corner(self):
        result = children_with_node(Node(1, 1), self.le_map2, self.diag_cost)
        self.assertEqual(len(result), 7)
        coords = [child[:2] for child in result]
        self.assertEqual(coords, [(1, 2), (2, 2), (2, 1), (2, 0),
                                  (1, 0), (0, 1), (0, 2)])

    def test_children_return_3_correctly(self):
        result = children_with_node(Node(1, 1), self.le_map1, self.diag_cost)
        self.assertEqual(len(result), 3)

    def test_children_respects_x_bounds(self):
        result = children_with_node(Node(0, 1), self.empty_map, self.diag_cost)
        self.assertEqual(len(result), 5)
        result = children_with_node(Node(2, 1), self.empty_map, self.diag_cost)
        self.assertEqual(len(result), 5)

    def test_children_respects_y_bounds(self):
        result = children_with_node(Node(1, 0), [[".", ".", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost)
        self.assertEqual(len(result), 5)
        result = children_with_node(Node(1, 2), [[".", ".", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost)
        self.assertEqual(len(result), 5)

    def test_children_respects_xy_bounds(self):
        result = children_with_node(Node(0, 2), [[".", ".", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost)
        self.assertEqual(len(result), 3)

    def test_children_straight_obstacle_blocks_corners(self):
        result = children_with_node(Node(1, 1), [[".", "#", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost)
        self.assertEqual(len(result), 5)
        coords = [child[:2] for child in result]
        self.assertEqual(coords, [(1, 2), (2, 2), (2, 1), (0, 1), (0, 2)])


        result = children_with_node(Node(1, 1), [[".", ".", "."], [".", ".", "#"], [".", ".", "."]], self.diag_cost)
        self.assertEqual(len(result), 5)
        result = children_with_node(Node(1, 1), [[".", ".", "."], [".", ".", "."], [".", "#", "."]], self.diag_cost)
        self.assertEqual(len(result), 5)


class Node:
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y

        self.prev = prev
        self.next = next
