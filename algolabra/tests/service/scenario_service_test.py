import unittest
# from unittest.mock import mock_open, patch
from decimal import Decimal

from algolabra.service.scenario_service import ScenarioService


class TestScenarioService(unittest.TestCase):
    def setUp(self):
        self.scenario_service = ScenarioService()
        self.scenario_service.read_scenarios()
        self.diag_cost = self.scenario_service.diag_cost

    def test_scenario_service_default_diag_cost(self):
        """
        it starts and does something. i'm not getting deep into this right now.

        :return:
        """
        self.assertEqual(self.scenario_service.diag_cost, Decimal('1.4142135623730950488'))
