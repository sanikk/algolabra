import logging
import unittest
from decimal import Decimal
from pathlib import Path

from algolabra.fileIO.read_files import read_map
from algolabra.common_search_utils.check_solution import handle_path
from algolabra.fringe.fringe_with_logging import fringe_search_with_logging


class TestFringeWithLogging(unittest.TestCase):
    def setUp(self):
        self.citymap = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')
        self.testfile = Path("./test-output-file.txt")




    # def test_logging(self):
    #     with self.assertLogs('test_logger', level='DEBUG') as lc:
    #         start = 0, 0
    #         goal = 2, 2
    #         m = [[".", "#", "."], [".", "#", "."], [".", "#", "."]]
    #
    #         logger = logging.getLogger('test_logger')
    #         fringe_search_with_logging(start, goal, m, self.diag_cost, 1, 1, 'test_logger', self.testfile)
    #
    #         self.assertTrue("path not found. exiting." in lc.output)


    def test_minimap_no_path(self):
        start = 0,0
        goal = 2,2
        m = [[".", "#", "."], [".", "#", "."], [".", "#", "."]]
        ret = fringe_search_with_logging(start, goal, m, self.diag_cost, 0, 0, 'test-logger', self.testfile)
        self.assertIsNone(ret)
        # with open(self.testfile) as f:
            # data = f.read()
        # self.assertTrue("path not found. exiting." in data)

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = fringe_search_with_logging(start, goal, self.citymap, self.diag_cost, 0, 0, 'test-logger', self.testfile)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)

    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = fringe_search_with_logging(start, goal, self.citymap, self.diag_cost, 1, 1, 'test-logger', self.testfile)
        self.assertEqual(len(ret), 4)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertLess(ret[0], 17.485282)
        self.assertGreater(ret[0], 17.485281)

    def test_longer_path_with_citymap(self):
        # 30	Boston_0_512.map	512	512	498	442	395	488	122.05382385
        start = 498, 442
        goal = 395, 488
        ret = fringe_search_with_logging(start, goal, self.citymap, self.diag_cost, 2, 2, 'test-logger', self.testfile)
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

    def tearDown(self):
        # if self.testfile.exists():
            # self.testfile.unlink()
        pass