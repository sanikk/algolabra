from collections import OrderedDict


class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right


class LinkedMap(OrderedDict):
    """
    A linked map data structure built on OrderedDict.

    Gives O(1) removals
    """
    def __init__(self, start, *args, **kwargs):
        super().__init__(*args, **kwargs)

        start_node = Node(start, None, None)
        self[start] = start_node
        self.head = start_node
        self.tail = start_node


    def add_tail(self, value):
        if value in self:
            node = self[value]
            self._cut_key_links(node)
            node.right = None
        else:
            node = Node(value, None, None)
            self[value] = node

        node.left = self.tail
        self.tail.right = node
        self.tail = node


    def remove(self, key):
        """
        only remove a node that is being handled. so no checks.
        """
        self._cut_key_links(self.pop(key))



    def _cut_key_links(self, node):
        if node.right:
            node.right.left = node.left
        if node.left:
            node.left.right = node.right

        if self.head == node:
            self.head = node.right
        if self.tail == node:
            self.tail = node.left


    def __iter__(self):
        # return DirtyIterator(self)
        return LinkedMapIterator(self)


class LinkedMapIterator:
    def __init__(self, od: LinkedMap):
        self.od = od
        self.current_key = Node(None,None, od.head)


    def __iter__(self):
        return self


    def __next__(self):
        if self.current_key:
            self.current_key = self.current_key.right
            if self.current_key:
                return self.current_key.value
        raise StopIteration
