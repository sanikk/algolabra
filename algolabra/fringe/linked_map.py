from collections import OrderedDict

class Node:
    def __init__(self, x, y, left, right):
        self.x = x
        self.y = y
        self.left = left
        self.right = right

class LinkedMap(OrderedDict):
    """
    A linked map data structure built on OrderedDict.

    Gives O(1) removals
    """
    def __init__(self, start, start_node, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self[start] = start_node
        self.head = start_node or Node(None,None,None,right=start_node)
        self.tail = start_node

    def add_tail(self, x, y):
        if (x, y) in self.keys():
            node = self[(x,y)]
            self._cut_key_links(node)
            self.move_to_end((x,y))
        else:
            self[(x,y)] = node = Node(x, y, None, None)

        node.left = self.tail
        self.tail.right = node
        self.tail = node


    def remove_by_node(self, node):
        """
        ok this should be O(1) ?

        OrderedDict should access this by key, then use the dll structure underneath to actually remove it.
        My left,right things are just for iterator, they serve no purpose beyond that.

        """
        self._cut_key_links(node)
        del self[(node.x, node.y)]


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
        return LinkedMapIterator(self)

class LinkedMapIterator:
    def __init__(self, od: LinkedMap):
        self.od = od
        self.current_key = od.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_key is None:
            raise StopIteration
        prev = self.current_key
        self.current_key = self.current_key.right
        return prev
