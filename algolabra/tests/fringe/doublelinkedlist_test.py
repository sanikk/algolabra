import unittest
from algolabra.fringe.doublelinkedlist import DoubleLinkedList


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoubleLinkedList()

    def test_single_insert(self):
        self.dll.add_data_to_begin(1)
        self.assertEqual(travel_list(self.dll), [1])

    def test_single_insert_changes_head_and_tail(self):
        self.dll.add_data_to_begin(1)
        self.assertIsNotNone(self.dll.head)
        self.assertIsNotNone(self.dll.tail)
        self.assertEqual(self.dll.head, self.dll.tail)

    def test_10_inserts(self):
        # do_n_inserts(10, self.dll)
        [self.dll.add_data_to_begin(i) for i in range(1, 11)]
        self.assertEqual(travel_list(self.dll), [i for i in range(10, 0, -1)])

    def test_removal(self):
        do_n_inserts(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.data == 3]
        self.assertEqual(travel_list(self.dll), [4, 2, 1])

    def test_removal_changes_head_and_tail(self):
        do_n_inserts(1, self.dll)
        [self.dll.remove_node(node) for node in self.dll if node.data == 1]
        self.assertEqual(self.dll.head, self.dll.tail)
        self.assertIsNone(self.dll.head)

    def test_removal_changes_head(self):
        do_n_inserts(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.data == 4]
        self.assertIsNotNone(self.dll.head)
        self.assertEqual(self.dll.head.data, 3)

    def test_removal_changes_tail(self):
        do_n_inserts(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.data == 1]
        self.assertIsNotNone(self.dll.tail)
        self.assertEqual(self.dll.tail.data, 2)

def do_n_inserts(n, dll):
    for i in range(1, n+1):
        dll.add_data_to_begin(i)

def travel_list(dll):
    return [node.data for node in dll]


