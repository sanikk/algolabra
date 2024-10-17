from decimal import Decimal

from PyQt6.QtCore import QObject, pyqtSignal

class FringeSignals(QObject):
    # flimit_set = pyqtSignal(Decimal)
    flimit_set = pyqtSignal(str)
    node_visited = pyqtSignal(int, int)
    node_expanded = pyqtSignal(int, int)
    result_ready = pyqtSignal(Decimal)
    phase_ready = pyqtSignal(str, list, list)

class GenericSearchSignals(QObject):
    result_ready = pyqtSignal(float)

class AstarSignals(QObject):
    signal_str = pyqtSignal(str)
    signal_int = pyqtSignal(int)