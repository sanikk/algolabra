class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.data = data


class DLLIterator:
    def __init__(self, node: Node):
        self.previous = None
        self.current = node

    def __next__(self):
        if self.current:
            self.previous = self.current
            self.current = self.current.next
            return self.previous
        if self.previous and self.previous.next:
            # this happens when handling tail and moving to first of it's children
            self.previous = self.previous.next
            self.current = self.previous.next
            return self.previous
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:

    def __init__(self, node=None, data=None):
        if data:
            node = Node(data=data)
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

    def add_data_after_node(self, data, node):
        new_node = Node(prev=node, next=node.next, data=data)
        if node.next:
            node.next.prev = new_node
        node.next = new_node
        if self.tail == node:
            self.tail = new_node

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev

    def remove_data(self, data):
        node = self.find_node_with_data(data)
        self.remove_node(node)

    def find_node_with_data(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next

    def __iter__(self):
        return DLLIterator(self.head)
