

class Node:
    def __init__(self, data=None, prev=None, nex=None):
        self.prev = prev
        self.next = nex
        self.data = data
    def remove(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev

class DLLIterator:
    def __init__(self, node: Node):
        self.current = node

    def __next__(self):
        if self.current:
            node = self.current
            self.current = node.next
            return node
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:
    def __init__(self, node=None):
        self.head = node
        self.tail = self.head

    def add_to_begin(self, node):
        if self.head:
            self.head.prev = node
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = node

    def add_data_to_begin(self, data):
        node = Node(data)
        self.add_to_begin(node)

    def __iter__(self):
        return DLLIterator(self.head)
