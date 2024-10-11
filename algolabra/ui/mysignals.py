from PyQt6.QtCore import QObject, pyqtSignal

class FringeSignals(QObject):
    flimit_set = pyqtSignal(float)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)
    result_ready = pyqtSignal(float)

    # flimit_set = pyqtSignal(float)
    # node_visited = pyqtSignal(int, int)
    # node_expanded = pyqtSignal(int, int)
    # result_ready = pyqtSignal(float)

class GenericSearchSignals(QObject):
    result_ready = pyqtSignal(float)

class AstarSignals(QObject):
    signal_str = pyqtSignal(str)
    signal_int = pyqtSignal(int)