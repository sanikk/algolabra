from decimal import Decimal

from PyQt6.QtCore import QObject, pyqtSignal

class FringeSignals(QObject):
    flimit_set = pyqtSignal(Decimal)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)
    result_ready = pyqtSignal(Decimal)

class GenericSearchSignals(QObject):
    result_ready = pyqtSignal(float)

class AstarSignals(QObject):
    signal_str = pyqtSignal(str)
    signal_int = pyqtSignal(int)