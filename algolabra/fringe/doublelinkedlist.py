class Node:
    def __init__(self, prev=None, next=None, x=None, y=None):
        self.prev = prev
        self.next = next

        self.x = x
        self.y = y


class DLLIterator:
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
        if x and y:
            node = Node(x=x, y=y)
        self.head = node

    def add_node(self, x, y, node):
        new_node = Node(prev=node, next=node.next, x=x, y=y)
        if node.next:
            next_node = node.next
            next_node.prev = new_node
        node.next = new_node

    def remove_node(self, node):
        # so the iterator points at node n. we remove n. we get next from iterator.
        # as long as we don't alter the next of n we should be good.
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next

    def remove_at_xy(self, x, y):
        node = self.find_node_at_xy(x, y)
        if node:
            self.remove_node(node)

    def find_node_at_xy(self, x, y):
        for node in iter(self):
            if node.x == x and node.y == y:
                return node
    def removal_version(self, x, y):
        # TODO replace this with a doublelinkedlist function. do a search for (x,y), rm if found.
        pass

    def __iter__(self):
        return DLLIterator(self.head)

if __name__=='__main__':
    dll = DoubleLinkedList(data=1)