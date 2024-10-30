import unittest
from algolabra.fringe.linked_dict import LinkedDict

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.d = LinkedDict((5,5))

    def test_constructor_worked(self):
        self.assertIsNotNone(self.d)
        linknode = self.d.head
        self.assertEqual(self.d.get((5,5)), linknode)

    def test_constructor_set_head_and_tail(self):
        linknode = self.d.get((5,5))
        self.assertEqual(self.d.head, linknode)
        self.assertEqual(self.d.tail, linknode)

    def test_getitem_works(self):
        self.assertEqual(self.d[(5,5)].value, (5, 5))

    def test_few_additions_works(self):
        self.d.add_tail((1,1))
        self.assertEqual(self.d[(1,1)].value, (1,1))

        self.d.add_tail((2,2))
        self.assertEqual(self.d[(1, 1)].value, (1, 1))
        self.assertEqual(self.d[(2, 2)].value, (2, 2))

        self.d.add_tail((3,3))
        self.assertEqual(self.d[(1, 1)].value, (1, 1))
        self.assertEqual(self.d[(2, 2)].value, (2, 2))
        self.assertEqual(self.d[(3, 3)].value, (3, 3))

    def test_iterator_outputs_whole_list(self):
        self.d.add_tail((1,1))
        self.d.add_tail((2,2))
        self.d.add_tail((3,3))

        self.assertEqual(list(iter(self.d)), [(5, 5), (1, 1), (2, 2), (3, 3)])


    def second_add_moves_first(self):
        self.d.add_tail((1,1))
        linknode = self.d.get((1,1))

        self.d.add_tail((2,2))
        self.d.add_tail((3,3))
        self.d.add_tail((1,1))

        self.assertEqual(list(iter(self.d)), [(5, 5), (2, 2), (3, 3), (1, 1)])
        self.assertIs(self.d[(1,1)], linknode)


    def third_add_still_works_with_the_tail(self):
        self.d.add_tail((1, 1))
        self.d.add_tail((2, 2))
        self.d.add_tail((3, 3))
        self.d.add_tail((1, 1))
        self.d.add_tail((1, 1))

        self.assertEqual(list(iter(self.d)), [(5, 5), (2, 2), (3, 3), (1, 1)])



    # removal

    def test_remove_middle(self):
        self.d.add_tail((1, 1))
        self.d.add_tail((2, 2))
        self.d.add_tail((3, 3))

        self.d.remove((2,2))
        self.assertEqual(list(iter(self.d)), [(5, 5), (1, 1), (3, 3)])


    def test_remove_head(self):
        self.d.add_tail((1, 1))
        self.d.add_tail((2, 2))
        self.d.add_tail((3, 3))

        self.d.remove((5, 5))
        self.assertEqual(list(iter(self.d)), [(1, 1), (2, 2), (3, 3)])
        self.assertEqual(self.d.head.value, (1,1))

    def test_remove_tail(self):
        self.d.add_tail((1, 1))
        self.d.add_tail((2, 2))
        self.d.add_tail((3, 3))

        self.d.remove((3, 3))

        self.assertEqual(list(iter(self.d)), [(5, 5), (1, 1), (2, 2)])
        self.assertEqual(self.d.tail.value, (2, 2))


    # iterate


    # exceptions
    def test_empty_raises_stop_iteration(self):
        pass


