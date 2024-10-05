from algolabra.ui.ui import TabWindow
from algolabra.service.search_service import SearchService

import sys
from PyQt6.QtWidgets import QApplication

def main():
    search_service = SearchService()
    app = QApplication(sys.argv)

    ui = TabWindow(map_path="algolabra/bostonmaps/Boston_0_512.map", search_service=search_service)

    ui.resize(800, 600)

    ui.setWindowTitle('Pathfinding on a Grid')
    ui.show()
    return sys.exit(app.exec())

if __name__=='__main__':
    main()