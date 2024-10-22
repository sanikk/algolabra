from collections import OrderedDict


class LastUpdatedOrderedDict(OrderedDict):
    """
    From python docs https://docs.python.org/3/library/collections.html#ordereddict-examples-and-recipes
    """
    'Store items in the order the keys were last added'
    def pass_node(self):
        # print(f"pass_node {self.peek_last()=}")
        self.move_to_end(self.peek_last(), last=False)

    def peek_last(self):
        # print(f"peek_last {next(reversed(self))=}")
        return next(reversed(self))

    def peek_first(self):
        return next(iter(self))

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)

    # def __iter__(self):
    #     return MyIterator(self)

class MyIterator:
    def __init__(self, iterable: LastUpdatedOrderedDict):
        self.iterable = iterable

    def __next__(self):
        """
        this should never be empty.

        :return:
        """
        ret = self.iterable.popitem()
        if ret:
            return ret
        raise StopIteration
    def __iter__(self):
        return self
