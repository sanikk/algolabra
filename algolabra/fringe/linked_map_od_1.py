from collections import OrderedDict


class Linknode:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

class LinkedMapForFringe(OrderedDict):
    """
    A Linked Map structure, implemented here for the needs of Fringe search.

    This version is it, because:
    https://github.com/python/cpython/blob/main/Lib/collections/__init__.py#L83-L86

    dict uses an array for the keys so I can't leverage that in the same way. Removing a key moves all the other
    keys, and we end up with an O(n) operation with that.

    Also that naming is why Linknode is Linknode and not Link.
    """
    def __init__(self, start, *args, **kwargs):
        super().__init__(*args, **kwargs)

        linknode = Linknode(start, None, None)

        self[start] = linknode
        self.head = linknode
        self.tail = linknode

    def add_tail(self, value):
        if value in self.keys():
            linknode = self[value]
            self._cut_linknode_links(linknode)
            linknode.right = None

        else:
            linknode = Linknode(value, None, None)
            self[value] = linknode
        if not self.head:
            self.head = linknode
        linknode.left = self.tail
        self.tail.right = linknode
        self.tail = linknode


    def remove_pop(self, value):
        """
        This should throw an error
        :param value:
        :return:
        """
        self._cut_linknode_links(self.pop(value))

    def remove_del(self, value):
        self._cut_linknode_links(self[value])
        del self[value]


    def _cut_linknode_links(self, linknode):
        if linknode.right:
            linknode.right.left = linknode.left
        if linknode.left:
            linknode.left.right = linknode.right

        if self.tail == linknode:
            self.tail = linknode.left
        if self.head == linknode:
            self.head = linknode.right

    def __iter__(self):
        return LinkedMapForFringeIterator(self)

class LinkedMapForFringeIterator:
    def __init__(self, lm: LinkedMapForFringe):
        self.lm = lm
        self.current_key = lm.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_key is None:
            raise StopIteration
        prev = self.current_key.value
        self.current_key = self.current_key.right
        return prev
