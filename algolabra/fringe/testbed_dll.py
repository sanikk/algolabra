class Node:
    """
    Simple Node class for filling Doublelinked List.

    This has served it's use.
    """
    def __init__(self, x, y, left, right):
        self.x = x
        self.y = y
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node: ({self.x},{self.y})"


class DLLIterator:
    """
    Modified iterator for Doublelinked List.
    We point at previous node, resolve pointer only when asked for next, and then return next.
    """
    def __init__(self, node: Node):
        self.current = Node(None, None, None, node)

    def __next__(self):
        if self.current and self.current.right:
            self.current = self.current.right
            return self.current
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:
    def __init__(self, node):
        self.head = node
        self.tail = node
        self.on_fringe = {(node.x, node.y): node}

    def add_child(self, x, y, parent):
        # TODO testaa nopeus jos heittäis vaan tailiin.
        child = Node(x,y, parent, parent.right)
        if parent.right:
            parent.right.left = child
        parent.right = child

        bookkeeping = self.on_fringe.pop((child.x, child.y), None)
        if bookkeeping:
            self.remove_node(bookkeeping)
        self.on_fringe[(child.x, child.y)] = child

    def remove_node(self, node):
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left
        if self.head == node:
            self.head = node.right
        if self.tail == node:
            self.tail = node.left
        self.on_fringe.pop((node.x, node.y), None)


    def find_node(self, x, y):
        return self.on_fringe.get((x,y), None)

    def __iter__(self):
        """
        Returns iterator and duck types this as iterable.
        :return:
        """
        return DLLIterator(self.head)