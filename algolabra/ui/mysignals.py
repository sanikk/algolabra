from decimal import Decimal

from PyQt6.QtCore import QObject, pyqtSignal

class FringeSignals(QObject):
    """
    flimit_set, node_visited, node_expanded, result_ready, path_step
    """
    flimit_set = pyqtSignal(str)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)
    result_ready = pyqtSignal()
    path_step = pyqtSignal(int, int)
