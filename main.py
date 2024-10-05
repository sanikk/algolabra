from algolabra.ui.ui import UI

import sys
from PyQt6.QtWidgets import QApplication


app = QApplication(sys.argv)
ui = UI("algolabra/bostonmaps/Boston_0_512.map")
sys.exit(app.exec())
