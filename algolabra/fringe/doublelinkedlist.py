class Node:
    """
    Simple Node class for filling Doublelinked List.
    """
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y

        self.prev = prev
        self.next = next


    # TODO for debug purposes, remove this
    def __repr__(self):
        return f"{self.x=}, {self.y=}"

class DLLIterator:
    """
    Modified iterator for Doublelinked List.
    We point at previous node, resolve pointer only when asked for next, and then return next.
    """
    def __init__(self, node: Node):
        self.previous = Node(next=node)

    def __next__(self):
        if self.previous and self.previous.next:
            self.previous = self.previous.next
            return self.previous
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:
    """
    Simple Doublelinked List structure for Fringe.
    """
    def __init__(self, x=None, y=None, node=None):
        """
        Constructor takes node OR x,y
        :param x:
        :param y:
        :param node:
        """
        if x and y:
            node = Node(x=x, y=y)
        self.head = node

    def add_node(self, x, y, node):
        """
        Add node on list placing it after the node provided at parameter.
        :param x: for new node
        :param y: for new node
        :param node: parent node the new node will be placed under.
        :return: None
        """
        new_node = Node(prev=node, next=node.next, x=x, y=y)
        if node.next:
            next_node = node.next
            next_node.prev = new_node
        node.next = new_node

    def remove_node(self, node):
        """
        Removes the provided node from list. next should still point at next node if it gets popped.
        :param node: Node to remove
        :return: None
        """
        # so the iterator points at node n. we remove n. we get next from iterator.
        # as long as we don't alter the next of n we should be good.
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next

    def remove_at_xy(self, x, y):
        """
        Removes node with given x,y coordinates from list.
        Fails silently, but should never fail.

        :param x:
        :param y:
        :return:
        """
        node = self.find_node_at_xy(x, y)
        if node:
            self.remove_node(node)

    def find_node_at_xy(self, x, y):
        """
        Find and return the Node with given x,y coordinates.
        :param x:
        :param y:
        :return:
        """
        for node in iter(self):
            if node.x == x and node.y == y:
                return node

    def __iter__(self):
        """
        Returns iterator and duck types this as iterable.
        :return:
        """
        return DLLIterator(self.head)

class DoubleLinkedListWithDict:
    def __init__(self, x=None, y=None, node=None):
        if x and y and not node:
            node = Node(x, y)
        self.head = node
        self.on_fringe = {}
        if node:
            self.on_fringe[(node.x, node.y)] = node

    def add_child_xy(self, x, y, parent):
        child = Node(x, y, parent, parent.next)
        self.add_child(child, parent)


    def add_child(self, child, parent):
        if parent.next:
            parent.next.prev = child
        parent.next = child

        bookkeeping = self.on_fringe.pop((child.x, child.y), None)
        if bookkeeping:
            self.remove_node(bookkeeping)
        self.on_fringe[(child.x, child.y)] = child

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next
        self.on_fringe.pop((node.x, node.y), None)


    def find_node(self, x, y):
        return self.on_fringe.get((x,y), None)

    def __iter__(self):
        """
        Returns iterator and duck types this as iterable.
        :return:
        """
        return DLLIterator(self.head)


if __name__=='__main__':
    # dll = DoubleLinkedList(data=1)
    pass