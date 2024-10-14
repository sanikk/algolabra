class Node:
    """
    Simple Node class for filling Doublelinked List.

    This has served it's use.
    """
    def __init__(self, x=None, y=None, prev=None, next=None):
        self.x = x
        self.y = y

        self.prev = prev
        self.next = next


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

    def add_child(self, x, y, parent):
        child = Node(x,y, parent, parent.next)
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