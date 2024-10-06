import unittest
from algolabra.fringe.doublelinkedlist import DoubleLinkedList, Node


class TestDoubleLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoubleLinkedList(1, 1)

    def test_constructor_with_xy_works(self):
        constructed = DoubleLinkedList(1, 1)
        self.assertEqual(travel_list(constructed), [(1, 1)])
        self.assertIsNotNone(constructed.head)

        points = (2, 2)
        constructed = DoubleLinkedList(*points)
        self.assertEqual(travel_list(constructed), [(2, 2)])

    def test_constructor_with_no_data_works(self):
        constructed = DoubleLinkedList()
        self.assertEqual(travel_list(constructed), [])
        self.assertIsNone(constructed.head)

    def test_add_child_adds_child(self):
        self.dll.add_child(2, 2, self.dll.head)
        self.assertEqual([(node.x, node.y) for node in self.dll], [(1,1), (2,2)])

    def test_add_child_does_not_change_head(self):
        self.dll.add_child(2, 2, self.dll.head)
        self.assertNotEqual(self.dll.head.y, 2)
        self.assertNotEqual(self.dll.head.x, 2)

    def test_add_child_10_times_in_row(self):
        [self.dll.add_child(i, i, self.dll.head) for i in range(10, 1, -1)]
        self.assertEqual(travel_list(self.dll), [(i, i) for i in range(1,11)])

    def test_add_child_makes_dict_mark(self):
        self.assertIsNone(self.dll.on_fringe.get((2,2), None))
        self.dll.add_child(2, 2, self.dll.head)
        self.assertIsNotNone(self.dll.on_fringe.get((2, 2), None))

    def test_add_child_twice_replaces_dict_mark(self):
        self.dll.add_child(2, 2, self.dll.head)
        first_child = self.dll.on_fringe.get((2,2), None)
        self.assertIsNotNone(first_child)

        self.dll.add_child(2, 2, self.dll.head)
        second_child = self.dll.on_fringe.get((2,2), None)
        self.assertIsNotNone(second_child)

        self.assertIsNot(first_child, second_child)

    def test_add_child_twice_removes_other_child_and_moves_mark(self):
        self.dll.add_child(2, 2, self.dll.head)
        first_child = self.dll.on_fringe.get((2, 2), None)

        self.dll.add_child(3, 3, first_child)
        second_child = self.dll.on_fringe.get((3, 3), None)

        self.assertEqual(travel_list(self.dll), [(1, 1), (2, 2), (3, 3)])


        self.dll.add_child(2,2, second_child)
        self.assertEqual(travel_list(self.dll), [(1, 1), (3, 3), (2, 2)])

    def test_remove_node(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.x == 3]
        self.assertEqual(travel_list(self.dll), [(1, 1), (2, 2), (4, 4)])

    def test_remove_node_on_only_node_changes_head(self):
        [self.dll.remove_node(node) for node in self.dll if node.x == 1]
        self.assertIsNone(self.dll.head)

    def test_remove_node_on_head_changes_head(self):
        fill_to_n(3, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.y == 1]
        self.assertIsNotNone(self.dll.head)
        self.assertEqual(self.dll.head.x, 2)
        self.assertEqual(self.dll.head.y, 2)

    def test_remove_node_not_on_head_does_not_change_head(self):
        fill_to_n(4, self.dll)
        [self.dll.remove_node(nro) for nro in self.dll if nro.x == 4]
        self.assertIsNotNone(self.dll.head)
        self.assertEqual(self.dll.head.x, 1)

    def test_remove_node_removes_dict_mark(self):
        fill_to_n(4, self.dll)
        self.assertIsNotNone(self.dll.on_fringe.get((1, 1), None))
        self.dll.remove_node(self.dll.head)
        self.assertIsNone(self.dll.on_fringe.get((1, 1), None))

    def test_iterator_order_works_when_adding_children_to_working_node(self):
        previous = self.dll.head
        for node in self.dll:
            if node.x == 3:
                break
            self.dll.add_child(node.x + 1, node.y + 1, previous)
            previous = self.dll.find_node(node.x + 1, node.y + 1)
        self.assertEqual(travel_list(self.dll), [(1, 1), (2, 2), (3, 3)])

    def test_find_node_with_data_finds_existing_data(self):
        fill_to_n(5, self.dll)

        node = self.dll.find_node(1, 1)
        self.assertEqual(node.x, 1)
        self.assertEqual(node.y, 1)

        node3 = self.dll.find_node(3, 3)
        self.assertEqual(node3.x, 3)
        self.assertEqual(node3.y, 3)

        node5 = self.dll.find_node(5, 5)
        self.assertEqual(node5.x, 5)
        self.assertEqual(node5.y, 5)

    def test_find_node_with_data_does_not_find_nonexisting_data(self):
        fill_to_n(4, self.dll)

        self.assertIsNone(self.dll.find_node(0,0))
        self.assertIsNone(self.dll.find_node(1, 2))
        self.assertIsNone(self.dll.find_node(0, 1))
        self.assertIsNone(self.dll.find_node(2, 1))
        self.assertIsNone(self.dll.find_node(5, 5))

    def test_remove_data_removes_right_node(self):
        fill_to_n(4, self.dll)
        node = self.dll.find_node(3, 3)
        self.dll.remove_node(node)

        self.assertEqual(travel_list(self.dll), [(1,1), (2,2), (4,4)])


def fill_to_n(n, dll):
    for i in range(n, 1, -1):
        dll.add_child(i, i, dll.head)

def travel_list(dll):
    return [(node.x, node.y) for node in dll]




