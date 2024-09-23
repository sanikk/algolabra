import unittest
from algolabra.fringe.doublelinkedlist import DoubleLinkedList


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoubleLinkedList(data=1)

    def test_constructor_with_data_works(self):
        constructed = DoubleLinkedList(data=1)
        self.assertEqual(travel_list(constructed), [1])
        self.assertIsNotNone(constructed.head)
        self.assertIsNotNone(constructed.tail)
        self.assertEqual(constructed.head, constructed.tail)

    def test_single_insert_works(self):
        head = self.dll.head
        self.dll.add_data_after_node(2, head)
        self.assertEqual([node.data for node in self.dll], [1, 2])

    def test_single_insert_changes_tail_not_head(self):
        head = self.dll.head
        self.dll.add_data_after_node(2, head)
        self.assertEqual(self.dll.head, head)
        self.assertNotEqual(self.dll.tail, self.dll.head)


    def test_10_inserts(self):
        [self.dll.add_data_after_node(i, self.dll.head) for i in range(10, 1, -1)]
        self.assertEqual(travel_list(self.dll), [i for i in range(1, 11)])

    def test_remove_node(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.data == 3]
        self.assertEqual(travel_list(self.dll), [1, 2, 4])

    def test_remove_node_changes_head_and_tail(self):
        [self.dll.remove_node(node) for node in self.dll if node.data == 1]
        self.assertEqual(self.dll.head, self.dll.tail)
        self.assertIsNone(self.dll.head)

    def test_remove_node_changes_head(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.data == 1]
        self.assertIsNotNone(self.dll.head)
        self.assertEqual(self.dll.head.data, 2)

    def test_remove_node_changes_tail(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.data == 4]
        self.assertIsNotNone(self.dll.tail)
        self.assertEqual(self.dll.tail.data, 3)

    def test_iterator_works_when_handling_tail_and_adding_children(self):
        for node in self.dll:
            if node.data == 3:
                break
            self.dll.add_data_after_node(node.data + 1, node)
        self.assertEqual(travel_list(self.dll), [1, 2, 3])
        self.assertEqual(self.dll.tail.data, 3)

    def test_find_node_with_data_finds_existing_data(self):
        fill_to_n(4, self.dll)

        self.assertEqual(self.dll.find_node_with_data(1).data, 1)
        self.assertEqual(self.dll.find_node_with_data(3).data, 3)
        self.assertEqual(self.dll.find_node_with_data(4).data, 4)

    def test_find_node_with_data_does_not_find_nonexisting_data(self):
        fill_to_n(4, self.dll)

        self.assertIsNone(self.dll.find_node_with_data(0))
        self.assertIsNone(self.dll.find_node_with_data(5))

    def test_remove_data_removes_right_node(self):
        fill_to_n(4, self.dll)
        self.dll.remove_data(3)

        self.assertEqual(travel_list(self.dll), [1, 2, 4])

def fill_to_n(n, dll):
    for i in range(n, 1, -1):
        dll.add_data_after_node(i, dll.head)

def travel_list(dll):
    return [node.data for node in dll]




