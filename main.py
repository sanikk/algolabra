from algolabra.ui.ui import UI
from algolabra.service.search_service import SearchService

import sys
from PyQt6.QtWidgets import QApplication


search_service = SearchService()
app = QApplication(sys.argv)
ui = UI(map_path="algolabra/bostonmaps/Boston_0_512.map", search_service=search_service)
sys.exit(app.exec())
