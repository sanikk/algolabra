from PyQt6.QtCore import QObject, pyqtSignal

class SearchSignals(QObject):
    """
    flimit_set(str)
    node_visited(int, int)
    node_expanded(int, int)
    result_ready()
    path_step(int, int)
    """
    flimit_set = pyqtSignal(str)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)
    result_ready = pyqtSignal()
    path_step = pyqtSignal(int, int)
