import logging
import unittest
from decimal import Decimal
from io import StringIO
from pathlib import Path

from algolabra.fileIO.read_files import read_map
from algolabra.common_search_utils.check_solution import handle_path
from algolabra.fringe.fringe_with_logging import fringe_search_with_logging


class TestFringeWithLogging(unittest.TestCase):
    def setUp(self):
        self.citymap = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')

        self.log_stream = StringIO()
        self.log_handler = logging.StreamHandler(self.log_stream)
        self.logger = logging.getLogger('fringe_logger')
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)

    def test_fringe_search_logging(self):
        start, goal = (0, 0), (2, 2)
        citymap = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

        fringe_search_with_logging(start, goal, citymap, self.diag_cost, -1, -1, logger=self.logger)

        self.log_handler.flush()
        log_output = self.log_stream.getvalue()

        self.assertIn("Running Fringe for scenario -1-1\n", log_output)


    def test_fringe_no_path_logging(self):
        start, goal = (0, 0), (2, 2)
        citymap = [['.', '#', '.'], ['.', '#', '.'], ['.', '#', '.']]

        fringe_search_with_logging(start, goal, citymap, self.diag_cost, -1, -1, logger=self.logger)

        self.log_handler.flush()
        log_output = self.log_stream.getvalue()

        self.assertIn("path not found. exiting.\n", log_output)

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = fringe_search_with_logging(start, goal, self.citymap, self.diag_cost, 0, 0, logger=self.logger)

        self.log_handler.flush()
        log_output = self.log_stream.getvalue()

        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)
        self.assertIn("visit(1) - expand(1) (344, 85):",log_output)

    def test_longer_path_with_citymap(self):
        start = 498, 442
        goal = 395, 488
        ret = fringe_search_with_logging(start, goal, self.citymap, self.diag_cost, 2, 2, self.logger)

        self.log_handler.flush()
        log_output = self.log_stream.getvalue()

        self.assertEqual(len(ret), 4)

        # shortest path is made of d diagonal and s straigth steps so exact cost should be
        # d * diag_cost + straight

        steps, straight, diagonal = handle_path(ret[1])
        correct_answer = diagonal * self.diag_cost + straight

        self.assertEqual(ret[0], correct_answer)

        self.assertIn("visit(1) - expand(1) (498, 442):", log_output)
        self.assertIn(f"found goal with cost {correct_answer}", log_output)

        # This returns Inexact = True, Rounded = True values
        # but the costs are correct. So seems to be test context related.

        # backup tests in case things change:
        self.assertLess(ret[0], 122.05382387)
        self.assertGreater(ret[0], 122.05382385)


    def tearDown(self):
        self.logger.removeHandler(self.log_handler)
        self.log_stream.close()
