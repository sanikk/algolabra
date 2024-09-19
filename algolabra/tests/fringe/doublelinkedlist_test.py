import unittest
from algolabra.fringe.doublelinkedlist import DoubleLinkedList


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoubleLinkedList()

    def test_single_insert(self):
        self.dll.add_data_to_begin(1)
        self.assertEqual(travel_list(self.dll), [1])

    def test_10_inserts(self):
        [self.dll.add_data_to_begin(i) for i in range(1, 11)]
        self.assertEqual(travel_list(self.dll), [i for i in range(10, 0, -1)])

    def test_removal(self):
        # TODO test removal
        pass

def do_n_inserts(n, dll):
    for i in range(1, n+1):
        dll.add_data_to_begin(i)

def travel_list(dll):
    return [node.data for node in dll]


