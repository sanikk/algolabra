import unittest
from decimal import Decimal

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QCoreApplication, QEventLoop

from algolabra.fringe.fringe_thread import fringe_search
from algolabra.fileIO.read_files import read_map
from algolabra.common_search_utils.check_solution import handle_path
from algolabra.ui.search_signals import SearchSignals




class TestFringeThread(unittest.TestCase):
    def setUp(self):
        self.citymap = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')

    def test_minimap_no_path(self):
        start = 0,0
        goal = 2,2
        m = [[".", "#", "."], [".", "#", "."], [".", "#", "."]]
        ret = fringe_search(start, goal, m, self.diag_cost)
        self.assertIsNone(ret)

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)

    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertLess(ret[0], 17.485282)
        self.assertGreater(ret[0], 17.485281)

    def test_longer_path_with_citymap(self):
        # 30	Boston_0_512.map	512	512	498	442	395	488	122.05382385
        start = 498, 442
        goal = 395, 488
        ret = fringe_search(start, goal, self.citymap, self.diag_cost)
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

    def test_signals(self):
        obj = SearchSignals()
        handler = Mock()
        obj.node_visited.connect(handler.node_visited)
        obj.node_expanded.connect(handler.node_expanded)
        obj.flimit_set.connect(handler.flimit_change)

        start = 344, 85
        goal = 343, 85
        fringe_search(start, goal, self.citymap, self.diag_cost, signals=obj)

        QCoreApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents, 50)
        # QEventLoop.AllEvents
        # QEventLoop.ProcessEventsFlag.AllEvents

        self.assertEqual(handler.visited, 7)
        self.assertEqual(handler.expanded, 1)
        self.assertEqual(handler.flimit_change_count, 1)

class Mock(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.visited = 0
        self.expanded = 0
        self.flimit_change_count = 0

    @pyqtSlot(int, int)
    def node_visited(self, x, y):
        self.visited += 1

    @pyqtSlot(int, int)
    def node_expanded(self, x, y):
        self.expanded += 1

    @pyqtSlot(str)
    def flimit_change(self, new_flimit: str):
        self.flimit_change_count += 1

