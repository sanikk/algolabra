import unittest
from algolabra.fringe.doublelinkedlist import DoubleLinkedList


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoubleLinkedList(1, 1)

    def test_constructor_with_data_works(self):
        constructed = DoubleLinkedList(1, 1)
        self.assertEqual(travel_list(constructed), [(1, 1)])
        self.assertIsNotNone(constructed.head)

    def test_constructor_with_no_data_works(self):
        constructed = DoubleLinkedList()
        self.assertEqual(travel_list(constructed), [])
        self.assertIsNone(constructed.head)

    def test_single_insert_works(self):
        head = self.dll.head
        self.dll.add_node(2, 2, head)
        self.assertEqual([(node.x, node.y) for node in self.dll], [(1,1), (2,2)])

    def test_single_insert_does_not_change_head(self):
        head = self.dll.head
        self.dll.add_node(2, 2, head)
        self.assertEqual(self.dll.head, head)

    def test_10_inserts(self):
        [self.dll.add_node(i, i, self.dll.head) for i in range(10, 1, -1)]
        self.assertEqual(travel_list(self.dll), [(i, i) for i in range(1, 11)])

    def test_remove_node(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.x == 3]
        self.assertEqual(travel_list(self.dll), [(1, 1), (2, 2), (4, 4)])

    def test_remove_node_on_only_node_changes_head(self):
        [self.dll.remove_node(node) for node in self.dll if node.x == 1]
        self.assertIsNone(self.dll.head)

    def test_remove_node_on_head_changes_head(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.y == 1]
        self.assertIsNotNone(self.dll.head)
        self.assertEqual(self.dll.head.x, 2)
        self.assertEqual(self.dll.head.y, 2)

    def test_remove_node_not_on_head_does_not_change_head(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.x == 4]
        self.assertIsNotNone(self.dll.head)
        self.assertEqual(self.dll.head.x, 1)

    def test_iterator_order_works_when_adding_children_to_working_node(self):
        for node in self.dll:
            if node.x == 3:
                break
            self.dll.add_node(node.x + 1, node.x + 1, node)
        self.assertEqual(travel_list(self.dll), [(1, 1), (2, 2), (3, 3)])

    def test_find_node_with_data_finds_existing_data(self):
        fill_to_n(4, self.dll)

        node = self.dll.find_node_at_xy(1, 1)
        self.assertEqual(node.x, 1)
        self.assertEqual(node.y, 1)

        node3 = self.dll.find_node_at_xy(3, 3)
        self.assertEqual(node3.x, 3)
        self.assertEqual(node3.y, 3)

        node4 = self.dll.find_node_at_xy(4, 4)
        self.assertEqual(node4.x, 4)
        self.assertEqual(node4.y, 4)

    def test_find_node_with_data_does_not_find_nonexisting_data(self):
        fill_to_n(4, self.dll)

        self.assertIsNone(self.dll.find_node_at_xy(0,0))
        self.assertIsNone(self.dll.find_node_at_xy(1, 2))
        self.assertIsNone(self.dll.find_node_at_xy(0, 1))
        self.assertIsNone(self.dll.find_node_at_xy(2, 1))
        self.assertIsNone(self.dll.find_node_at_xy(5, 5))

    def test_remove_data_removes_right_node(self):
        fill_to_n(4, self.dll)
        self.dll.remove_at_xy(3, 3)

        self.assertEqual(travel_list(self.dll), [(1,1), (2,2), (4,4)])


def fill_to_n(n, dll):
    for i in range(n, 1, -1):
        dll.add_node(i, i, dll.head)

def travel_list(dll):
    return [(node.x, node.y) for node in dll]




