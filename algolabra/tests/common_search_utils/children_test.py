import unittest
from algolabra.common_search_utils.children import children


class Node:
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y

        self.prev = prev
        self.next = next

class TestChildren(unittest.TestCase):
    def setUp(self):
        self.le_map1 = [["#", "#", "#"], ["#", ".", "."], [".", ".", "."]]
        self.le_map2 = [["#", ".", "."], [".", ".", "."], [".", ".", "."]]

    def test_children_returns_all_on_empty_map(self):
        result = children(Node(1, 1), [[".", ".", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 8)
        self.assertEqual(result, [(1, 2, 1), (2, 2, 1.4142135623730951), (2, 1, 1), (2, 0, 1.4142135623730951),
                                  (1, 0, 1), (0, 0, 1.4142135623730951), (0, 1, 1), (0, 2, 1.4142135623730951)])

    def test_children_returns_the_right_7_on_one_blocked_corner(self):
        result = children(Node(1, 1), self.le_map2)
        self.assertEqual(len(result), 7)
        coords = [child[:2] for child in result]
        self.assertEqual(coords, [(1, 2), (2, 2), (2, 1), (2, 0),
                                  (1, 0), (0, 1), (0, 2)])

    def test_children_return_3_correctly(self):
        result = children(Node(1, 1), self.le_map1)
        self.assertEqual(len(result), 3)

    def test_children_respects_x_bounds(self):
        result = children(Node(0, 1), [[".", ".", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 5)
        result = children(Node(2, 1), [[".", ".", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 5)

    def test_children_respects_y_bounds(self):
        result = children(Node(1, 0), [[".", ".", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 5)
        result = children(Node(1, 2), [[".", ".", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 5)

    def test_children_respects_xy_bounds(self):
        result = children(Node(0, 2), [[".", ".", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 3)

    def test_children_straight_obstacle_blocks_corners(self):
        result = children(Node(1, 1), [[".", "#", "."], [".", ".", "."], [".", ".", "."]])
        self.assertEqual(len(result), 5)
        coords = [child[:2] for child in result]
        self.assertEqual(coords, [(1, 2), (2, 2), (2, 1), (0, 1), (0, 2)])


        result = children(Node(1, 1), [[".", ".", "."], [".", ".", "#"], [".", ".", "."]])
        self.assertEqual(len(result), 5)
        result = children(Node(1, 1), [[".", ".", "."], [".", ".", "."], [".", "#", "."]])
        self.assertEqual(len(result), 5)