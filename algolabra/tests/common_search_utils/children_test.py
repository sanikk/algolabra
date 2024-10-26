import unittest
from decimal import Decimal

from algolabra.common_search_utils.children import children

# def children(nx, ny, citymap, diag_cost, map_size):

class TestChildren(unittest.TestCase):
    def setUp(self):
        self.le_map1 = [["#", "#", "#"], ["#", ".", "."], [".", ".", "."]]
        self.le_map2 = [["#", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.empty_map = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

        self.diag_cost = Decimal('1.4142135623730950488')

        self.list_of_all_neighbors = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
        self.list_of_corners = [(0,0), (2,0), (2,2), (0,2)]
        self.list_of_straights = [(1, 0), (2, 1), (1, 2), (0, 1)]

    def test_children_returns_all_on_empty_map(self):
        result = children(1, 1, self.empty_map, self.diag_cost, len(self.empty_map))
        self.assertEqual(len(result), 8)
        result.sort()
        self.assertEqual(result, sorted([(1, 2, 1), (2, 2, self.diag_cost), (2, 1, 1), (2, 0, self.diag_cost),
                                  (1, 0, 1), (0, 0, self.diag_cost), (0, 1, 1), (0, 2, self.diag_cost)]))
        result_coords = [(x, y) for x, y, z in result]

        self.assertTrue((1, 2) in result_coords)
        self.assertTrue((2, 2) in result_coords)
        self.assertTrue((2, 1) in result_coords)
        self.assertTrue((2, 0) in result_coords)
        self.assertTrue((1, 0) in result_coords)
        self.assertTrue((0, 0) in result_coords)
        self.assertTrue((0, 1) in result_coords)
        self.assertTrue((0, 2) in result_coords)

    def test_children_return_3_correctly(self):
        result = children(1, 1, self.le_map1, self.diag_cost, len(self.le_map1))
        self.assertEqual(len(result), 3)
        result_coords = [(x, y) for x, y, z in result]
        self.assertTrue((2, 1) in result_coords)
        self.assertTrue((2, 2) in result_coords)
        self.assertTrue((1, 2) in result_coords)

    def test_children_respects_x_bounds(self):
        result = children(0, 1, self.empty_map, self.diag_cost, len(self.empty_map))
        self.assertEqual(len(result), 5)
        result = children(2, 1, self.empty_map, self.diag_cost, len(self.empty_map))
        self.assertEqual(len(result), 5)

    def test_children_respects_y_bounds(self):
        result = children(1, 0, [[".", ".", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost, 3)
        self.assertEqual(len(result), 5)
        result = children(1, 2, [[".", ".", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost, 3)
        self.assertEqual(len(result), 5)

    def test_children_respects_xy_bounds(self):
        result = children(0, 2, [[".", ".", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost, 3)
        self.assertEqual(len(result), 3)

    def test_children_straight_obstacle_blocks_corners(self):
        result = children(1, 1, [[".", "#", "."], [".", ".", "."], [".", ".", "."]], self.diag_cost, 3)
        self.assertEqual(len(result), 5)
        coords = [child[:2] for child in result]
        self.assertEqual(coords, [(1, 2), (2, 2), (2, 1), (0, 1), (0, 2)])

        result = children(1, 1, [[".", ".", "."], [".", ".", "#"], [".", ".", "."]], self.diag_cost, 3)
        self.assertEqual(len(result), 5)
        result = children(1, 1, [[".", ".", "."], [".", ".", "."], [".", "#", "."]], self.diag_cost, 3)
        self.assertEqual(len(result), 5)

    def test_children_returns_the_right_7_on_one_blocked_corner(self):
        for pos in self.list_of_corners:
            m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
            m[pos[0]][pos[1]] = '#'
            ret = children(1, 1, m, self.diag_cost, 3)
            self.assertEqual(len(ret), 7)
            coords = [child[:2] for child in ret]
            self.assertFalse(pos in coords)
            coords.append(pos)
            coords.sort()
            self.assertEqual(coords, self.list_of_all_neighbors)

    def test_children_returns_the_right_5_on_one_blocked_north(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        m[0][1] = '#'
        ret = children(1, 1, m, self.diag_cost, 3)
        self.assertEqual(len(ret), 5)
        coords = [child[:2] for child in ret]
        self.assertFalse((1, 0) in coords)
        self.assertEqual(sorted([child[:2] for child in ret]), sorted([(2, 1), (2, 2), (1, 2), (2, 0), (0, 1)]))



    def test_children_returns_the_right_5_on_one_blocked_west(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        m[1][0] = '#'
        ret = children(1, 1, m, self.diag_cost, 3)
        self.assertEqual(len(ret), 5)
        coords = [child[:2] for child in ret]
        self.assertFalse((0, 1) in coords)
        self.assertEqual(sorted(coords), sorted([(0, 0), (1, 0), (2, 0), (2, 1), (0, 1)]))



    def test_children_returns_the_right_5_on_one_blocked_south(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        m[2][1] = '#'
        ret = children(1, 1, m, self.diag_cost, 3)
        self.assertEqual(len(ret), 5)
        coords = [child[:2] for child in ret]
        coords.sort()
        self.assertFalse((1, 2) in coords)
        self.assertEqual(sorted(coords), sorted([(0, 0), (1, 0),(1, 2), (0, 2), (0, 1)]))



    def test_children_returns_the_right_5_on_one_blocked_east(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        m[1][2] = '#'
        ret = children(1, 1, m, self.diag_cost, 3)
        self.assertEqual(len(ret), 5)
        coords = [child[:2] for child in ret]
        self.assertFalse((2, 1) in coords)
        self.assertEqual(sorted(coords),  [(0, 0), (0, 1), (1, 0), (1, 2), (2, 0)])


class Node:
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y

        self.prev = prev
        self.next = next
