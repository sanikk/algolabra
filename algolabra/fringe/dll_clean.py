class Node:
    """
    Used as dll link. Light.

    Other choice would be to use nodes as cache, but then we'd have to save all the data.
    if remove_node_from_fringe would save the data to a dict that might work... but not enough data to
    justify that.

    holds g, parent, h
    """
    def __init__(self, x=None, y=None, left=None, right=None):
        self.x = x
        self.y = y

        self.left = left
        self.right = right

    def __str__(self):
        return f"Node: ({self.x},{self.y}), left={self.left}, right={self.right}"

class DLLIterator:
    """
    on __next__: moves pointer and returns value.
    self.current.right is checked when __next__ is called.
    """
    def __init__(self, node: Node):
        self.current = Node(right=node)


    def __next__(self):
        if self.current and self.current.right:
            self.current = self.current.right
            return self.current
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:
    """


    """
    def __init__(self, node):
        self.head = node
        self.tail = node
        self.on_fringe = {(node.x, node.y): node}

    def add_child(self, x, y):
        # TODO time these
        if (x, y) in self.on_fringe:
            child = self.on_fringe.pop((x, y))
            self._cut_node_links(child)
            child.left = self.tail
            child.right = None
        else:
            child = Node(x, y, self.tail, None)

        self.tail.right = child
        self.tail = child
        self.on_fringe[(x, y)] = child
        return


    def add_child_to_tail(self, x, y):
        """
        new version of add tail that creates new node
        :param x:
        :param y:
        :return:
        """
        child = Node(x, y, self.tail, None)
        self.tail.right = child
        self.tail = child
        self.on_fringe[(x, y)] = child

    def move_child_to_tail(self, child):
        """
        new add tail for reusing old nodes.

        :param child:
        :return:
        """
        self._cut_node_links(child)
        child.left = self.tail
        child.right = None
        self.tail.right = child
        self.tail = child
        self.on_fringe[(child.x, child.y)] = child

    def remove_by_node(self, node):
        """
        remove node from Fringe

        removes node from fringe dict
        cuts links, the node is now loose

        :param node:
        :return:
        """
        self.on_fringe.pop((node.x, node.y), None)
        self._cut_node_links(node)


    def _cut_node_links(self, node):
        """
        cuts the links of node:
        left, right, head, tail

        :param node:
        :return:
        """
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left
        if self.head == node:
            self.head = node.right
        if self.tail == node:
            self.tail = node.left

    def __iter__(self):
        """
        Returns iterator and duck types this as iterable.
        :return:
        """
        return DLLIterator(self.head)

    def __bool__(self):
        if self.head is None:
            return False
        return True
