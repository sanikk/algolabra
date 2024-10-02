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
        return f"Node:{self.x=}, {self.y=}"

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
    def __init__(self, x=None, y=None, node=None):
        if x and y and not node:
            node = Node(x, y)
        self.head = node
        self.on_fringe = {}
        if node:
            self.on_fringe[(node.x, node.y)] = node

    def add_child_xy(self, x, y, parent):
        child = Node(x, y)
        self.add_child(child, parent)

    # if F contains s: Remove s from F
    # insert s into F after n
    def add_child(self, child, parent):
        child.next = parent.next
        if child.next:
            child.next.prev = child
        parent.next = child
        child.prev = parent

        if previous_entry := self.on_fringe.pop((child.x, child.y), None):
            self.remove_node(previous_entry)
        self.on_fringe[(child.x, child.y)] = child

    # remove n from F
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

    def remove_xy(self, x, y):
        if node := self.find_node(x, y):
            self.remove_node(node)

    # iterate over nodes
    def __iter__(self):
        """
        Returns iterator and duck types this as iterable.
        :return:
        """
        return DLLIterator(self.head)


if __name__=='__main__':
    # dll = DoubleLinkedList(data=1)
    pass