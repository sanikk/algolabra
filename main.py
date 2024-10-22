from algolabra.ui.ui import UI
from algolabra.service.scenario_service import ScenarioService
from algolabra.service.search_service import SearchService

import sys
from PyQt6.QtWidgets import QApplication

def main():
    scenario_service = ScenarioService()
    search_service = SearchService(scenario_service=scenario_service)

    app = QApplication(sys.argv)

    ui = UI(scenario_service=scenario_service, search_service=search_service)
    ui.resize(800, 600)

    ui.setWindowTitle('Pathfinding on a Grid')
    ui.show()
    return sys.exit(app.exec())

if __name__=='__main__':
    main()