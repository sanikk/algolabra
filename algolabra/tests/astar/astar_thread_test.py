import unittest
from decimal import Decimal

from PyQt6.QtCore import QObject, pyqtSlot, QEventLoop, QCoreApplication

from algolabra.ui.search_signals import SearchSignals
from algolabra.astar.astar_thread import astar, reconstruct_path
from algolabra.fileIO.read_files import read_map

class TestAstarThread(unittest.TestCase):
    def setUp(self):
        self.citymap = read_map("algolabra/bostonmaps/Boston_0_512.map")
        self.diag_cost = Decimal('1.4142135623730950488')

    def test_open_minimap(self):
        m = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        start = 0, 0
        goal = 2, 2
        ret = astar(start, goal, m, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 2 * self.diag_cost)

    def test_alley_minimap(self):
        m = [[".", ".", "."], [".", "#", "."], [".", "#", "."]]
        start = 0,2
        goal = 2,2
        ret = astar(start, goal, m, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], Decimal(6))

    def test_one_step_path_with_citymap(self):
        start = 344, 85
        goal = 343, 85
        ret = astar(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(ret[0], 1)
        self.assertEqual(ret[2], False)
        self.assertEqual(ret[3], False)

    def test_short_path_with_citymap(self):
        start = 352, 438
        goal = 346, 423
        ret = astar(start, goal, self.citymap, self.diag_cost)
        self.assertEqual(len(ret), 4)
        self.assertEqual(type(ret[0]), Decimal)
        self.assertLess(ret[0], 17.4852814)
        self.assertGreater(ret[0], 17.4852813)
        self.assertEqual(ret[2], False)
        self.assertEqual(ret[3], False)

    def test_no_path(self):
        start = 0,0
        goal = 2,2
        m = [[".", "#", "."], [".", "#", "."], [".", "#", "."]]
        ret = astar(start, goal, m, self.diag_cost)
        self.assertIsNone(ret)

    def test_reconstruct_path_function(self):
        camefrom = {(344,85): (343,85)}
        start = 343,85
        goal = 344,85
        ret = reconstruct_path(start, goal, camefrom)
        self.assertEqual(ret, [(344, 85), (343, 85)])

    def test_signals(self):
        obj = SearchSignals()
        handler = Mock()
        obj.node_visited.connect(handler.node_visited)
        obj.node_expanded.connect(handler.node_expanded)
        obj.flimit_set.connect(handler.flimit_change)

        start = 344, 85
        goal = 343, 85
        astar(start, goal, self.citymap, self.diag_cost, signals=obj)

        QCoreApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents, 50)

        self.assertEqual(handler.visited, 8)
        self.assertEqual(handler.expanded, 2)
        self.assertGreater(handler.flimit_change_count, 0)
        self.assertEqual(handler.elist, [start,goal])
        self.assertTrue(goal in handler.vlist)


class Mock(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.visited = 0
        self.vlist = []
        self.expanded = 0
        self.elist = []
        self.flimit_change_count = 0
        self.flist = []

    @pyqtSlot(int, int)
    def node_visited(self, x, y):
        self.visited += 1
        self.vlist.append((x,y))

    @pyqtSlot(int, int)
    def node_expanded(self, x, y):
        self.expanded += 1
        self.elist.append((x,y))

    @pyqtSlot(str)
    def flimit_change(self, new_flimit: str):
        self.flimit_change_count += 1
        self.flist.append(new_flimit)

