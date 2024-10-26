import unittest
from decimal import Decimal

from algolabra.common_search_utils.children import children

def get_coords(result):
    return [(x, y) for x, y, z in result]

class TestChildren(unittest.TestCase):
    def setUp(self):
        self.m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.diag_cost = Decimal('1.4142135623730950488')
        self.d1 = d1 = Decimal('1')
        self.diag = diag = 1.414
            #   2 1 8
            #   3   7
            #   4 5 6
        self.full_list = [(1, 0, d1), (0, 0, diag), (0, 1, d1), (0, 2, diag), (1, 2, d1), (2, 2, diag), (2, 1, d1),
                              (2, 0, diag)]

    def test_1_0_with_empty_map(self):
        ret = children(1, 0, self.m, self.diag, 3)
        self.assertEqual(len(ret), 5)

    def test_corners_on_empty_minimap(self):
        d1 = Decimal('1')
        diag = 1.414

        ret = children(0, 0, self.m, diag, 3)
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret, [(0,1,d1), (1,1, diag), (1,0,d1)])

        ret = children(2, 0, self.m, 1.414, 3)
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret, [(1,0, d1), (1,1, diag), (2,1, d1)])

        ret = children(2, 2, self.m, 1.414, 3)
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret, [(2,1,d1),(1,1, diag),(1, 2, d1)])

        ret = children(2, 0, self.m, 1.414, 3)
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret, [(1,0,d1), (1,1,diag),(2,1,d1)])

    def test_1_1_with_empty_map(self):
        ret = children(1, 1, self.m, 1.414, 3)
        self.assertEqual(len(ret), 8)
        self.assertEqual(ret, self.full_list)

    def test_1_0_with_north_blocked(self):
        self.m[1][1] = '#'
        diag = self.diag
        d1 = self.d1
        ret = children(1, 0, self.m, diag, 3)
        self.assertEqual(len(ret), 2)
        self.assertEqual(ret, [(0,0, d1), (2,0, d1)])

    # Used here for naming:
    #
    #   2 1 8
    #   3   7
    #   4 5 6
    #

    def test_1_1_with_1_blocked(self):

        self.m[0][1] = "#"
        d1 = self.d1
        diag = self.diag
        ret = children(1,1,self.m, diag, 3)
        self.assertEqual(len(ret), 5)

        self.assertEqual(ret, self.full_list[2:7])

    def test_1_1_with_2_blocked(self):
        self.m[0][0] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 7)
        self.assertEqual(ret[0], self.full_list[0])
        self.assertEqual(ret[1:], self.full_list[2:])

    def test_1_1_with_3_blocked(self):
        self.m[1][0] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 5)
        self.assertEqual(ret[0], self.full_list[0])
        self.assertEqual(ret[1:], self.full_list[4:])

    def test_1_1_with_4_blocked(self):
        self.m[2][0] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 7)
        self.assertEqual(ret[:3], self.full_list[:3])
        self.assertEqual(ret[3:], self.full_list[4:])

    def test_1_1_with_5_blocked(self):
        self.m[2][1] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 5)
        self.assertEqual(ret[:3], self.full_list[:3])
        self.assertEqual(ret[3:], self.full_list[6:])

    def test_1_1_with_6_blocked(self):
        self.m[2][2] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 7)
        self.assertEqual(ret[:5], self.full_list[:5])
        self.assertEqual(ret[6], self.full_list[7])

    def test_1_1_with_7_blocked(self):
        self.m[1][2] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 5)
        self.assertEqual(ret[:5], self.full_list[:5])


    def test_1_1_with_8_blocked(self):
        self.m[0][2] = "#"

        ret = children(1,1,self.m, self.diag, 3)
        self.assertEqual(len(ret), 7)
        self.assertEqual(ret, self.full_list[:7])
