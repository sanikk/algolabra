import unittest
# from unittest.mock import mock_open, patch
from decimal import Decimal

from algolabra.service.scenario_service import ScenarioService
from algolabra.service.search_service import SearchService


class TestSearchService(unittest.TestCase):
    def setUp(self):
        self.search_service = SearchService()

    def test_one(self):
        """ ok i suddenly have no idea what to test here """
        pass
